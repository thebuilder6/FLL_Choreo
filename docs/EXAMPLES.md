# Usage Examples

This document provides practical examples for using the FLL Trajectory Optimizer.

## Basic Examples

### Example 1: Simple Two-Point Path

Generate a straight-line trajectory from (0, 0) to (1, 0):

**waypoints.json:**
```json
[
  {"x": 0.0, "y": 0.0, "heading": 0.0},
  {"x": 1.0, "y": 0.0, "heading": 0.0}
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
  {"x": 0.0, "y": 0.0, "heading": 0.0},
  {"x": 0.5, "y": 0.5, "heading": 0.785},
  {"x": 1.0, "y": 0.0, "heading": 0.0}
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
  {"x": 0.0, "y": 0.0, "heading": 0.0},
  {"x": 1.0, "y": 1.0, "heading": null},
  {"x": 2.0, "y": 0.0, "heading": 0.0}
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

### Example 4: Accuracy Weighting

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

### Example 5: Controller Export

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

### Example 6: Varying Sample Density

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

### Example 7: Complex FLL Mission Path

Generate a trajectory for a typical FLL mission:

**mission_waypoints.json:**
```json
[
  {"x": 0.0, "y": 0.0, "heading": 0.0},
  {"x": 0.3, "y": 0.2, "heading": 0.5},
  {"x": 0.6, "y": 0.4, "heading": 1.0},
  {"x": 0.9, "y": 0.3, "heading": 0.8},
  {"x": 1.2, "y": 0.5, "heading": 0.0}
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

### Example 8: Using the Optimizer Directly

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

### Example 9: Validating a Trajectory

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

### Example 10: Exporting for Controller

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
print(f"Last sample: {ctrl_data['samples'][-1]}")
```

---

### Example 11: Comparing Accuracy Weights

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

### Example 12: Debugging Optimization Failure

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
- Conflicting constraints (e.g., sharp turn at high speed)
- Incorrect config parameters (wrong units, unrealistic values)

---

### Example 13: Checking Constraint Violations

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

### Example 14: Batch Processing Multiple Paths

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

### Example 15: Generating Comparison Plots

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
