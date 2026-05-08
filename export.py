import json
import numpy as np


def resample_to_fixed_dt(samples, target_dt: float = 0.02, track_width: float = 0.0965):
    """
    Linearly resample a variable-timestep trajectory to a fixed controller dt.

    Returns a list of dicts with keys:
        t, x, y, heading, vl, vr, v, omega
    """
    if not samples:
        return []

    t_src = np.array([s["t"] for s in samples])
    x_src = np.array([s["x"] for s in samples])
    y_src = np.array([s["y"] for s in samples])
    h_src = np.array([s["heading"] for s in samples])
    vl_src = np.array([s["vl"] for s in samples])
    vr_src = np.array([s["vr"] for s in samples])

    total_t = t_src[-1]
    num_steps = int(np.floor(total_t / target_dt)) + 1
    target_times = np.arange(num_steps) * target_dt

    def lerp(t_query, t_arr, val_arr):
        if t_query <= t_arr[0]:
            return float(val_arr[0])
        if t_query >= t_arr[-1]:
            return float(val_arr[-1])
        idx = int(np.searchsorted(t_arr, t_query)) - 1
        idx = max(0, min(idx, len(t_arr) - 2))
        t0, t1 = t_arr[idx], t_arr[idx + 1]
        frac = (t_query - t0) / (t1 - t0)
        return float(val_arr[idx] + (val_arr[idx + 1] - val_arr[idx]) * frac)

    out = []
    for t in target_times:
        if t > total_t:
            break
        vl = lerp(t, t_src, vl_src)
        vr = lerp(t, t_src, vr_src)
        v = (vl + vr) / 2.0
        omega = (vr - vl) / track_width
        out.append(
            {
                "t": round(float(t), 6),
                "x": round(lerp(t, t_src, x_src), 6),
                "y": round(lerp(t, t_src, y_src), 6),
                "heading": round(lerp(t, t_src, h_src), 6),
                "vl": round(vl, 6),
                "vr": round(vr, 6),
                "v": round(v, 6),
                "omega": round(omega, 6),
            }
        )
    return out


def export_controller_json(samples, target_dt: float = 0.02, track_width: float = 0.0965):
    """Return a JSON-serializable dict with controller-ready samples."""
    resampled = resample_to_fixed_dt(samples, target_dt, track_width)
    return {
        "format": "controller_profile",
        "version": 1,
        "dt": target_dt,
        "num_samples": len(resampled),
        "samples": resampled,
    }


def write_controller_file(
    input_traj_file: str, output_file: str, target_dt: float = 0.02, track_width: float = 0.0965
):
    with open(input_traj_file, "r") as f:
        traj_data = json.load(f)

    samples = traj_data["trajectory"]["samples"]
    ctrl = export_controller_json(samples, target_dt, track_width)

    with open(output_file, "w") as f:
        json.dump(ctrl, f, indent=1)

    print(f"Exported {ctrl['num_samples']} controller samples at dt={target_dt}s to {output_file}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 3:
        print("Usage: python export.py <input.traj> <output.json> [target_dt]")
        sys.exit(1)
    dt = float(sys.argv[3]) if len(sys.argv) > 3 else 0.02
    write_controller_file(sys.argv[1], sys.argv[2], dt)
