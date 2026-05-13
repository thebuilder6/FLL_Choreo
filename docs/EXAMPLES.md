# Usage Examples

This document provides practical examples for using the FLL Trajectory Optimizer.

## Basic Examples

### Example 1: Simple Two-Point Path

Generate a straight-line trajectory from (0, 0) to (1, 0):

**waypoints.json:**

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0 },
  { "x": 1.0, "y": 0.0, "heading": 0.0 }
]
```

**Command:**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o straight.traj --plot
```

**Expected output:**

- Optimization converges in ~67 ms
- Robot accelerates from rest, cruises at max speed, decelerates to rest
- Total time depends on robot max speed (typically 1-2 seconds for 1m)

---

### Example 2: Three-Point Turn

Generate a trajectory with a turn:

**waypoints.json:**

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0 },
  { "x": 0.5, "y": 0.5, "heading": 0.785 },
  { "x": 1.0, "y": 0.0, "heading": 0.0 }
]
```

**Command:**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o turn.traj --plot
```

**Expected output:**

- Robot follows curved path through middle waypoint
- Heading is constrained at all three waypoints
- Slower than straight line due to turn

---

### Example 3: Unconstrained Heading

Generate a path where only positions matter, not heading:

**waypoints.json:**

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0 },
  { "x": 1.0, "y": 1.0, "heading": null },
  { "x": 2.0, "y": 0.0, "heading": 0.0 }
]
```

**Command:**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o arc.traj --plot
```

**Expected output:**

- Start and end headings are fixed
- Middle waypoint heading is free (optimizer chooses optimal heading)
- Results in smooth arc through middle point

---

## Advanced Examples

### Example 4: Intermediate Stops

Generate a trajectory with stops at specific waypoints:

**waypoints_with_stops.json:**

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0, "stop": true },
  { "x": 0.5, "y": 0.0, "heading": 0.0, "stop": false },
  { "x": 0.5, "y": 0.3, "heading": 1.57, "stop": true },
  { "x": 1.0, "y": 0.3, "heading": 1.57, "stop": false },
  { "x": 1.0, "y": 0.0, "heading": 0.0, "stop": true }
]
```

**Command:**

```bash
python main.py -c fll_choreo.chor -w waypoints_with_stops.json -o stops.traj --plot
```

**Expected output:**

- Robot starts at rest at (0, 0)
- Moves to (0.5, 0) without stopping
- Comes to complete stop at (0.5, 0.3)
- Moves to (1.0, 0.3) without stopping
- Comes to complete stop at final waypoint (1.0, 0)

**Use case:** Multi-segment FLL missions where robot needs to pause between maneuvers (e.g., to wait for a mechanism to complete, to align precisely, or to execute an action).

---

### Example 5: Event Markers

Generate a trajectory with mission event markers:

**waypoints_with_events.json:**

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0 },
  { "x": 0.5, "y": 0.3, "heading": 0.5, "event": "lower_arm" },
  { "x": 1.0, "y": 0.0, "heading": 0.0 },
  { "x": 1.5, "y": 0.3, "heading": 0.0, "event": "release" }
]
```

**Command:**

```bash
python main.py -c fll_choreo.chor -w waypoints_with_events.json -o events.traj \
  --export-format controller \
  --controller-dt 0.02
```

**Expected output:**

- Trajectory file contains `"event"` field at waypoint samples
- Controller export preserves events at nearest timestep
- Robot controller reads events and triggers actions (arm, intake, release)

**CLI Override:**

You can also specify events via CLI flag:

```bash
python main.py -c fll_choreo.chor -w waypoints.json --events "2:lower_arm,5:release"
```

**Use case:** FLL missions where robot needs to execute specific actions at waypoints (lower arm to pick up object, release to drop object, intake to collect pieces).

---

### Example 6: Accuracy Weighting

Compare time-optimal vs. smooth trajectories:

**Time-optimal (default):**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o fast.traj -a 0.0 --validate
```

**Balanced smoothness:**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o smooth.traj -a 1.0 --validate
```

**Very smooth:**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o very_smooth.traj -a 5.0 --validate
```

**Comparison:**

- `a=0.0`: Fastest time, highest jerk, may overshoot on real robot
- `a=1.0`: ~3-5% time cost, ~35% less jerk, better tracking
- `a=5.0`: Significant time cost, very smooth, minimal overshoot

---

### Example 7: Controller Export

Generate a trajectory and export for on-robot execution:

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o traj.traj \
  --validate \
  --export-format controller \
  --controller-dt 0.02
```

**Output files:**

- `traj.traj`: Full variable-timestep trajectory (for analysis)
- `traj_controller.json`: Fixed 20ms timestep (for robot controller)

**Controller file format:**

```json
{
  "format": "controller_profile",
  "version": 1,
  "dt": 0.02,
  "num_samples": 150,
  "samples": [
    {"t": 0.0, "x": 0.0, "y": 0.0, "heading": 0.0, "vl": 0.0, "vr": 0.0, "v": 0.0, "omega": 0.0},
    {"t": 0.02, "x": 0.001, "y": 0.0, "heading": 0.0, "vl": 0.1, "vr": 0.1, "v": 0.1, "omega": 0.0},
    ...
  ]
}
```

---

### Example 8: Varying Sample Density

Compare different sample densities:

**Low density (fast, less accurate):**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o low_res.traj -s 5
```

**Medium density (default):**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o med_res.traj -s 10
```

**High density (slower, more accurate):**

```bash
python main.py -c fll_choreo.chor -w waypoints.json -o high_res.traj -s 20
```

**Tradeoffs:**

- `-s 5`: Faster optimization, but may miss sharp turns
- `-s 10`: Good balance for most FLL paths
- `-s 20`: Slower optimization, smoother curves, better for complex paths

---

### Example 9: Complex FLL Mission Path

Generate a trajectory for a typical FLL mission:

**mission_waypoints.json:**

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0 },
  { "x": 0.3, "y": 0.2, "heading": 0.5 },
  { "x": 0.6, "y": 0.4, "heading": 1.0 },
  { "x": 0.9, "y": 0.3, "heading": 0.8 },
  { "x": 1.2, "y": 0.5, "heading": 0.0 }
]
```

**Command:**

```bash
python main.py -c fll_choreo.chor -w mission_waypoints.json -o mission.traj \
  -s 10 \
  -a 0.5 \
  --validate \
  --export-format controller \
  --controller-dt 0.02 \
  --plot
```

**Expected output:**

- Optimization time: ~300-500 ms
- Constraint violations: 0
- Forward integration error: < 0.01 m
- Controller samples: ~200-400 at 20ms dt

---

## Python API Examples

### Example 10: Using the Optimizer Directly

```python
from robot_model import RobotConfig
from optimizer import TrajectoryOptimizer
import json

# Load configuration
with open('fll_choreo.chor', 'r') as f:
    config_data = json.load(f)

robot_cfg = RobotConfig(config_data)
optimizer = TrajectoryOptimizer(robot_cfg)

# Define waypoints
waypoints = [
    (0.0, 0.0, 0.0),
    (1.0, 0.5, 0.5),
    (2.0, 1.0, 1.0)
]

# Solve with accuracy weighting
samples = optimizer.solve(
    waypoints,
    num_samples_per_segment=10,
    accuracy_weight=1.0
)

# Print results
print(f"Total time: {samples[-1]['t']:.3f}s")
print(f"Max speed: {max(s['vl'] + s['vr'] for s in samples) / 2:.3f} m/s")
```

---

### Example 11: Validating a Trajectory

```python
from validator import validate_trajectory

# Run validation
metrics, audit, errors = validate_trajectory('output.traj', 'fll_choreo.chor')

print("\n=== Metrics ===")
for k, v in metrics.items():
    print(f"{k}: {v:.4f}")

print("\n=== Constraint Audit ===")
print(f"Violating samples: {audit['num_violating_samples']}")
if audit['num_violating_samples'] > 0:
    print(f"Max left motor violation: {audit['left_motor_force']:.6f} N")
    print(f"Max right motor violation: {audit['right_motor_force']:.6f} N")
    print(f"Max traction violation: {audit['traction_total']:.6f} N")

print("\n=== Forward Integration Errors ===")
print(f"Max position error: {errors['max_pos_error_m']:.6f} m")
print(f"Final position error: {errors['final_pos_error_m']:.6f} m")

# Check if trajectory is safe
is_safe = (
    errors['max_pos_error_m'] < 0.01 and
    errors['final_pos_error_m'] < 0.01 and
    audit['num_violating_samples'] == 0
)
print(f"\nTrajectory is {'SAFE' if is_safe else 'UNSAFE'}")
```

---

### Example 12: Exporting for Controller

```python
from export import write_controller_file

# Export with 20ms timestep
write_controller_file(
    'output.traj',
    'controller_profile.json',
    target_dt=0.02,
    track_width=0.0965
)

# Load and inspect
with open('controller_profile.json', 'r') as f:
    ctrl_data = json.load(f)

print(f"Controller profile: {ctrl_data['num_samples']} samples at {ctrl_data['dt']}s dt")
print(f"First sample: {ctrl_data['samples'][0]}")
```

---

### Example 13: Comparing Accuracy Weights

```python
from robot_model import RobotConfig
from optimizer import TrajectoryOptimizer
from validator import compute_metrics
import json

# Load config
with open('fll_choreo.chor', 'r') as f:
    config_data = json.load(f)

robot_cfg = RobotConfig(config_data)
optimizer = TrajectoryOptimizer(robot_cfg)

waypoints = [
    (0.0, 0.0, 0.0),
    (1.0, 0.5, 0.5),
    (2.0, 1.0, 0.0)
]

# Test different accuracy weights
weights = [0.0, 0.5, 1.0, 2.0, 5.0]

print("Accuracy Weight | Time (s) | Max Accel (m/s²) | Max Jerk (m/s³)")
print("-" * 65)

for w in weights:
    samples = optimizer.solve(waypoints, num_samples_per_segment=10, accuracy_weight=w)
    metrics = compute_metrics(samples)
    print(f"{w:14.1f} | {metrics['total_time_s']:7.3f} | {metrics['max_accel_m_s2']:15.3f} | {metrics['max_jerk_m_s3']:13.3f}")
```

**Typical output:**

```
Accuracy Weight | Time (s) | Max Accel (m/s²) | Max Jerk (m/s³)
-----------------------------------------------------------------
           0.0 |   2.345 |           1.850 |        12.500
           0.5 |   2.412 |           1.420 |         8.300
           1.0 |   2.478 |           1.100 |         6.200
           2.0 |   2.623 |           0.850 |         4.800
           5.0 |   2.987 |           0.620 |         3.500
```

---

## Troubleshooting Examples

### Example 14: Debugging Optimization Failure

If optimization fails or times out:

```bash
# First, try with fewer samples
python main.py -c fll_choreo.chor -w waypoints.json -o test.traj -s 5

# If that works, gradually increase
python main.py -c fll_choreo.chor -w waypoints.json -o test.traj -s 10
python main.py -c fll_choreo.chor -w waypoints.json -o test.traj -s 15
```

Check for:

- Infeasible waypoints (too far apart for robot speed)
- Incorrect config parameters (wrong units, unrealistic values)

---

### Example 15: Checking Constraint Violations

If validation shows constraint violations:

```bash
# Run validation to see details
python validator.py output.traj fll_choreo.chor
```

**Output interpretation:**

- `left_motor_force > 0`: Left wheel force exceeds motor capability
- `right_motor_force > 0`: Right wheel force exceeds motor capability
- `traction_total > 0`: Total force exceeds friction limit

**Fixes:**

- Reduce `vmax` or `tmax` in config
- Increase `cof` (friction coefficient)
- Add accuracy weight to smooth trajectory
- Increase sample density for better resolution

---

## Integration Examples

### Example 16: Batch Processing Multiple Paths

```python
import os
import json
from robot_model import RobotConfig
from optimizer import TrajectoryOptimizer

# Load config once
with open('fll_choreo.chor', 'r') as f:
    config_data = json.load(f)
robot_cfg = RobotConfig(config_data)
optimizer = TrajectoryOptimizer(robot_cfg)

# Process multiple waypoint files
waypoint_files = [
    'mission1_waypoints.json',
    'mission2_waypoints.json',
    'mission3_waypoints.json'
]

for wp_file in waypoint_files:
    with open(wp_file, 'r') as f:
        wp_data = json.load(f)

    waypoints = [(w['x'], w['y'], w.get('heading')) for w in wp_data]

    samples = optimizer.solve(waypoints, num_samples_per_segment=10, accuracy_weight=0.5)

    output_file = wp_file.replace('waypoints.json', 'traj.traj')
    result = {
        "name": os.path.basename(output_file).split('.')[0],
        "version": 3,
        "trajectory": {
            "config": config_data.get("config", {}),
            "samples": samples
        }
    }

    with open(output_file, 'w') as f:
        json.dump(result, f, indent=1)

    print(f"Generated {output_file}")
```

---

### Example 17: Generating Comparison Plots

```python
from plotter import plot_trajectory
import json

# Load trajectory
with open('output.traj', 'r') as f:
    traj_data = json.load(f)

samples = traj_data['trajectory']['samples']

# Load waypoints
with open('waypoints.json', 'r') as f:
    wp_data = json.load(f)

waypoints = [(w['x'], w['y'], w.get('heading')) for w in wp_data]

# Plot with waypoints overlay
plot_trajectory(samples, waypoints=waypoints, title="FLL Mission Trajectory")
```

---

### Example 18: Complete FLL Mission (All Features)

Generate a comprehensive trajectory using all available features: stops, events, accuracy weighting, validation, controller export, and plotting.

**complete_mission.json:**

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0, "stop": true },
  { "x": 0.4, "y": 0.2, "heading": 0.5, "event": "lower_arm" },
  { "x": 0.8, "y": 0.4, "heading": 0.8, "stop": true },
  { "x": 1.2, "y": 0.3, "heading": 0.0, "event": "release" },
  { "x": 1.5, "y": 0.0, "heading": -0.5, "stop": false },
  { "x": 1.8, "y": 0.2, "heading": 0.5, "event": "intake" },
  { "x": 2.0, "y": 0.5, "heading": 1.57, "stop": true },
  { "x": 1.8, "y": 0.8, "heading": 3.14, "event": "deposit" },
  { "x": 1.5, "y": 0.5, "heading": -1.57, "stop": false },
  { "x": 1.2, "y": 0.3, "heading": 0.0, "stop": true }
]
```

**Command:**

```bash
python main.py -c fll_choreo.chor -w complete_mission.json -o complete_mission.traj \
  -a 1.0 \
  -n 15 \
  --validate \
  --export-format controller \
  --controller-dt 0.02 \
  --plot
```

**Features demonstrated:**

- **Stops**: Robot comes to rest at waypoints 0, 2, 6, and 9 (indices with `"stop": true`)
- **Events**: Mission actions triggered at waypoints 1 (lower_arm), 3 (release), 5 (intake), and 7 (deposit)
- **Accuracy weighting**: `-a 1.0` balances time-optimality with smoothness for better tracking
- **Sample density**: `-n 15` provides high resolution for complex path
- **Validation**: `--validate` checks constraint violations and forward integration errors
- **Controller export**: `--export-format controller` resamples to 20ms timestep for robot
- **Plotting**: `--plot` visualizes the trajectory with waypoints overlay

**Expected output:**

```
Loading config from fll_choreo.chor...
Loading waypoints from complete_mission.json...
Optimizing trajectory through 10 waypoints (accuracy_weight=1.0)...
Stop waypoints at indices: [0, 2, 6, 9]
Optimization converged. Total time: 15.2341s
Successfully saved trajectory to complete_mission.traj

=== Validation Report: complete_mission.traj ===
Samples: 136 | Config: fll_choreo.chor

-- Metrics --
  total_time_s: 15.2341
  path_length_m: 3.2456
  max_linear_speed_m_s: 0.6523
  max_wheel_speed_m_s: 0.7891
  max_accel_m_s2: 0.8934
  max_jerk_m_s3: 4.1234

-- Constraint Audit --
  Violating samples: 0
  Max left_motor_force violation: 0.000000 N
  Max right_motor_force violation: 0.000000 N
  Max traction_total violation: 0.000000 N

-- Forward Integration (1 ms RK4) --
  max_pos_error_m: 0.005234
  rms_pos_error_m: 0.002123
  max_heading_error_rad: 0.003456
  final_pos_error_m: 0.001234
  final_heading_error_rad: 0.000000

PASS — trajectory is safe to run.

Exported 762 controller samples at dt=0.02s to complete_mission_controller.json
```

**Output files:**

- `complete_mission.traj`: Full variable-timestep trajectory with events
- `complete_mission_controller.json`: Fixed 20ms timestep for robot controller with events

**Use case:** Complete FLL mission with multiple segments, stops for precision, events for mechanism control, and validation for safety.

```python
from plotter import plot_trajectory
import json

# Load trajectory
with open('output.traj', 'r') as f:
    traj_data = json.load(f)

samples = traj_data['trajectory']['samples']

# Load waypoints
with open('waypoints.json', 'r') as f:
    wp_data = json.load(f)

waypoints = [(w['x'], w['y'], w.get('heading')) for w in wp_data]

# Plot with waypoints overlay
plot_trajectory(samples, waypoints=waypoints, title="FLL Mission Trajectory")
```
