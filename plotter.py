import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

def plot_trajectory(samples, waypoints=None, title="Robot Trajectory"):
    """
    samples:   list of trajectory sample dicts (from optimizer output)
    waypoints: optional list of (x, y, heading_or_None) tuples to overlay
    """
    t  = [s['t'] for s in samples]
    x  = [s['x'] for s in samples]
    y  = [s['y'] for s in samples]
    h  = [s['heading'] for s in samples]
    vl = [s['vl'] for s in samples]
    vr = [s['vr'] for s in samples]
    fl = [s['fl'] for s in samples]
    fr = [s['fr'] for s in samples]

    fig, axs = plt.subplots(2, 2, figsize=(13, 10))
    fig.suptitle(title, fontsize=14, fontweight='bold')

    # ── 1. Top-Down Path ──────────────────────────────────────────────────────
    ax = axs[0, 0]

    # Colour path by speed so fast/slow sections are obvious
    v_lin = np.array([(s['vl'] + s['vr']) / 2 for s in samples])
    points = np.array([x, y]).T.reshape(-1, 1, 2)
    segments = np.concatenate([points[:-1], points[1:]], axis=1)

    from matplotlib.collections import LineCollection
    from matplotlib.cm import ScalarMappable
    from matplotlib.colors import Normalize

    norm  = Normalize(vmin=v_lin.min(), vmax=v_lin.max())
    lc    = LineCollection(segments, cmap='plasma', norm=norm, linewidth=2.5)
    lc.set_array(v_lin[:-1])
    ax.add_collection(lc)
    plt.colorbar(ScalarMappable(norm=norm, cmap='plasma'),
                 ax=ax, label='Speed (m/s)', shrink=0.8)

    # Small heading arrows along the path
    step = max(1, len(x) // 12)
    for i in range(0, len(x), step):
        ax.annotate('', xy=(x[i] + 0.06*np.cos(h[i]), y[i] + 0.06*np.sin(h[i])),
                    xytext=(x[i], y[i]),
                    arrowprops=dict(arrowstyle='->', color='steelblue', lw=1.5))

    # ── Waypoint overlays ─────────────────────────────────────────────────────
    if waypoints:
        arrow_len = 0.12   # metres
        for idx, wp in enumerate(waypoints):
            wx, wy = wp[0], wp[1]
            wh     = wp[2] if len(wp) > 2 else None

            # Star marker
            ax.plot(wx, wy, marker='*', markersize=18,
                    color='gold', markeredgecolor='darkorange',
                    markeredgewidth=1.2, zorder=5)

            # Heading arrow (only if constrained)
            if wh is not None:
                ax.annotate('', xy=(wx + arrow_len*np.cos(wh),
                                    wy + arrow_len*np.sin(wh)),
                            xytext=(wx, wy),
                            arrowprops=dict(arrowstyle='->', color='darkorange',
                                            lw=2.5),
                            zorder=6)

            # Label (offset slightly above the star)
            ax.text(wx, wy + 0.05, f'W{idx}', ha='center', va='bottom',
                    fontsize=9, fontweight='bold', color='darkorange', zorder=7)

        # Legend entries
        star_patch  = mpatches.Patch(color='gold',      label='Waypoint')
        arrow_patch = mpatches.Patch(color='darkorange', label='Target heading')
        ax.legend(handles=[star_patch, arrow_patch], fontsize=8, loc='best')

    ax.autoscale()
    ax.set_xlabel('X (m)')
    ax.set_ylabel('Y (m)')
    ax.set_title('Top-Down Path (colour = speed)')
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.5)

    # ── 2. Velocity Profile ───────────────────────────────────────────────────
    axs[0, 1].plot(t, vl, color='tomato',      label='Left wheel')
    axs[0, 1].plot(t, vr, color='mediumseagreen', label='Right wheel')
    axs[0, 1].plot(t, v_lin, 'k--', linewidth=1.5, label='Linear')
    if waypoints:
        # Mark the approximate timestamp for each waypoint using nearest x/y
        wp_xs = [wp[0] for wp in waypoints]
        wp_ys = [wp[1] for wp in waypoints]
        for idx, (wx, wy) in enumerate(zip(wp_xs, wp_ys)):
            dists = [(x[i]-wx)**2 + (y[i]-wy)**2 for i in range(len(x))]
            ni = int(np.argmin(dists))
            axs[0, 1].axvline(t[ni], color='darkorange', linestyle=':', alpha=0.7)
            axs[0, 1].text(t[ni], axs[0,1].get_ylim()[0] if axs[0,1].get_ylim()[0] != 0 else 0,
                           f'W{idx}', color='darkorange', fontsize=8, rotation=90,
                           va='bottom', ha='right')
    axs[0, 1].set_xlabel('Time (s)')
    axs[0, 1].set_ylabel('Velocity (m/s)')
    axs[0, 1].set_title('Velocity Profiles')
    axs[0, 1].legend(fontsize=8)
    axs[0, 1].grid(True, linestyle='--', alpha=0.5)

    # ── 3. Wheel Forces ───────────────────────────────────────────────────────
    axs[1, 0].plot(t, fl, color='tomato',       label='Left force')
    axs[1, 0].plot(t, fr, color='mediumseagreen', label='Right force')
    axs[1, 0].axhline(0, color='black', linewidth=0.8)
    axs[1, 0].set_xlabel('Time (s)')
    axs[1, 0].set_ylabel('Force (N)')
    axs[1, 0].set_title('Wheel Forces')
    axs[1, 0].legend(fontsize=8)
    axs[1, 0].grid(True, linestyle='--', alpha=0.5)

    # ── 4. Heading over time ──────────────────────────────────────────────────
    axs[1, 1].plot(t, h, color='steelblue')
    if waypoints:
        for idx, wp in enumerate(waypoints):
            if len(wp) > 2 and wp[2] is not None:
                wp_xs2 = wp[0]
                dists  = [(x[i]-wp[0])**2 + (y[i]-wp[1])**2 for i in range(len(x))]
                ni     = int(np.argmin(dists))
                axs[1, 1].axvline(t[ni], color='darkorange', linestyle=':', alpha=0.7)
                axs[1, 1].plot(t[ni], wp[2], marker='*', color='gold',
                               markeredgecolor='darkorange', markersize=12, zorder=5)
                axs[1, 1].text(t[ni], wp[2], f' W{idx}', fontsize=8,
                               color='darkorange', va='bottom')
    axs[1, 1].set_xlabel('Time (s)')
    axs[1, 1].set_ylabel('Heading (rad)')
    axs[1, 1].set_title('Heading Profile')
    axs[1, 1].grid(True, linestyle='--', alpha=0.5)

    plt.tight_layout(rect=[0, 0.02, 1, 0.95])
    plt.show()


if __name__ == "__main__":
    import sys, json
    if len(sys.argv) > 1:
        traj_file = sys.argv[1]
        wp_file   = sys.argv[2] if len(sys.argv) > 2 else None
        with open(traj_file, 'r') as f:
            data = json.load(f)
        wps = None
        if wp_file:
            with open(wp_file, 'r') as f:
                raw = json.load(f)
            wps = [(w['x'], w['y'], w.get('heading')) for w in raw]
        plot_trajectory(data['trajectory']['samples'], waypoints=wps,
                        title=traj_file)
