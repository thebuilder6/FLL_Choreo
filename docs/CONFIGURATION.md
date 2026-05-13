# Configuration Guide

This guide explains how to configure the robot parameters and waypoints for the FLL Trajectory Optimizer.

## Robot Configuration File Format

The optimizer uses a Choreo-style JSON configuration file (`.chor` extension). The file contains robot physical parameters in a specific structure.

## Required Parameters

### Mass (`config.mass`)

Robot mass in kilograms.

```json
"mass": {
  "exp": "0.8 kg",
  "val": 0.8
}
```

**How to measure:**

- Weigh your robot on a scale
- Typical FLL robot: 0.5 - 1.5 kg

**Impact:**

- Affects acceleration limits (heavier = slower acceleration)
- Affects traction limit calculation

---

### Rotational Inertia (`config.inertia`)

Rotational moment of inertia in kg·m².

```json
"inertia": {
  "exp": "1e-6 kg m ^ 2",
  "val": 0.000001
}
```

**How to estimate:**

- For a rectangular robot: `I = mass * (width² + length²) / 12`
- Typical FLL robot: 1e-6 to 1e-4 kg·m²
- If unknown, start with 1e-6 (very small value has minimal impact)

**Impact:**

- Affects how much torque is needed for rotation
- Higher inertia = slower turns

---

### Track Width (`config.differentialTrackWidth`)

Distance between the centers of the left and right wheels in meters.

```json
"differentialTrackWidth": {
  "exp": "96.5 mm",
  "val": 0.0965
}
```

**How to measure:**

- Measure from center of left wheel to center of right wheel
- Typical FLL robot: 0.08 - 0.15 m (8 - 15 cm)

**Impact:**

- Affects turning kinematics
- Wider track width = slower angular velocity for same wheel speed difference

---

### Wheel Radius (`config.radius`)

Radius of the drive wheels in meters.

```json
"radius": {
  "exp": "56 mm",
  "val": 0.056
}
```

**How to measure:**

- Measure from wheel center to outer edge
- Typical LEGO wheel: 0.028 - 0.056 m (28 - 56 mm)

**Impact:**

- Affects speed conversion between wheel RPM and linear velocity
- Larger wheels = higher linear speed at same motor RPM

---

### Motor No-Load Speed (`config.vmax`)

Motor no-load angular velocity in radians/second.

```json
"vmax": {
  "exp": "150 RPM",
  "val": 15.707963267948966
}
```

**How to find:**

- Check motor datasheet
- For LEGO motors:
  - EV3 Large Motor: ~150-170 RPM
  - EV3 Medium Motor: ~240-260 RPM
  - Spike Prime Large Motor: ~175 RPM
- Convert RPM to rad/s: `rad/s = RPM * 2π / 60`

**Impact:**

- Maximum possible wheel speed
- Directly limits maximum robot speed

---

### Motor Stall Torque (`config.tmax`)

Motor stall torque in Newton-meters.

```json
"tmax": {
  "exp": "0.04 N * m",
  "val": 0.04
}
```

**How to find:**

- Check motor datasheet
- For LEGO motors:
  - EV3 Large Motor: ~0.04 N·m
  - EV3 Medium Motor: ~0.02 N·m
  - Spike Prime Large Motor: ~0.05 N·m
- Can be measured with a torque wrench

**Impact:**

- Maximum force the motor can apply
- Directly affects acceleration capability
- Higher torque = faster acceleration

---

### Gear Ratio (`config.gearing`)

Gear ratio between motor and wheel.

```json
"gearing": {
  "exp": "1",
  "val": 1.0
}
```

**How to determine:**

- Direct drive (motor connected directly to wheel): 1.0
- Geared down (wheel turns slower than motor): > 1.0
- Geared up (wheel turns faster than motor): < 1.0
- Calculate: `gear_ratio = motor_RPM / wheel_RPM`

**Impact:**

- Multiplies torque and divides speed (or vice versa)
- Affects both force limits and maximum speed

---

### Coefficient of Friction (`config.cof`)

Coefficient of friction between wheels and field surface.

```json
"cof": {
  "exp": "1.5",
  "val": 1.5
}
```

**How to estimate:**

- FLL field mat: ~1.0 - 1.5
- Smooth tile: ~0.5 - 0.8
- Carpet: ~0.8 - 1.2
- Can be measured with inclined plane test

**Impact:**

- Maximum traction force before wheel slip
- Higher friction = more acceleration possible without slipping

---

### Torque Headroom (`config.torqueHeadroom`)

Safety margin for motor torque limits. Multiplier applied to maximum motor force to ensure the Ramsete controller has reserve torque for path corrections.

```json
"torqueHeadroom": {
  "exp": "0.85",
  "val": 0.85
}
```

**How to set:**

- Default: 0.85 (15% headroom)
- Range: 0.70 - 0.95 (5-30% headroom)
- Lower values = more conservative, slower trajectories
- Higher values = more aggressive, less headroom for corrections

**Impact:**

- Reduces effective motor torque limit during optimization and validation
- Ensures Ramsete controller can correct tracking errors without saturating motors
- Accounts for real-world factors: battery voltage sag, gear backlash, discrete control loop
- Recommended: 0.85 for typical FLL robots (leaves 15% torque for corrections)

**Why this matters:**

The validator checks if the reference trajectory exceeds your motor limits. However, if a path requires 95% of max torque, the robot has almost no torque left for corrections. When the robot inevitably gets slightly off-path (due to bumps, backlash, or battery sag), the Ramsete controller may request 110% torque to correct, which gets clamped to 100%, preventing error correction until the curve ends. The torque headroom ensures the optimizer leaves performance on the table so the controller can fight real-world chaos.

---

### Speed Headroom (`config.speedHeadroom`)

Safety margin for wheel speed limits. Multiplier applied to maximum wheel speed to ensure the Ramsete controller has reserve speed for path corrections.

```json
"speedHeadroom": {
  "exp": "0.90",
  "val": 0.90
}
```

**How to set:**

- Default: 0.90 (10% headroom)
- Range: 0.80 - 0.95 (5-20% headroom)
- Lower values = more conservative, slower trajectories
- Higher values = more aggressive, less headroom for corrections

**Impact:**

- Reduces effective wheel speed limit during optimization and validation
- Ensures Ramsete controller can correct tracking errors without saturating speed
- Accounts for real-world factors: battery voltage sag, discrete control loop lag
- Recommended: 0.90 for typical FLL robots (leaves 10% speed for corrections)

**Why this matters:**

Similar to torque headroom, this ensures the optimizer doesn't push the robot to its absolute speed limits. The real-world robot runs at a discrete control loop (~5.7ms) rather than the continuous-time RK4 integration used by the validator. This lag, combined with battery voltage sag as the battery drains, means the physical robot may not achieve the theoretical maximum speeds. The speed headroom provides a buffer for these real-world effects.

---

## Optional Parameters

### Bumper Dimensions (`config.bumper`)

Robot bumper dimensions for collision checking (currently unused).

```json
"bumper": {
  "front": {
    "exp": "60 mm",
    "val": 0.06
  },
  "side": {
    "exp": "50 mm",
    "val": 0.05
  },
  "back": {
    "exp": "80 mm",
    "val": 0.08
  }
}
```

**Note:** These parameters are read but not used by the current optimizer. They are kept for Choreo compatibility and future obstacle avoidance features.

---

### Wheel Positions (`config.frontLeft`, `config.backLeft`)

Wheel positions relative to robot center (currently unused).

```json
"frontLeft": {
  "x": {
    "exp": "11 in",
    "val": 0.2794
  },
  "y": {
    "exp": "11 in",
    "val": 0.2794
  }
}
```

**Note:** These parameters are read but not used by the current optimizer (which assumes differential drive with wheels on the centerline). They are kept for Choreo compatibility.

---

## Example Configuration Files

### Minimal Configuration

```json
{
  "name": "my_robot",
  "version": 2,
  "type": "Differential",
  "config": {
    "mass": { "val": 0.8 },
    "inertia": { "val": 0.000001 },
    "differentialTrackWidth": { "val": 0.0965 },
    "radius": { "val": 0.056 },
    "vmax": { "val": 15.7 },
    "tmax": { "val": 0.04 },
    "gearing": { "val": 1.0 },
    "cof": { "val": 1.5 }
  }
}
```

### Full Choreo-Compatible Configuration

```json
{
  "name": "fll_robot",
  "version": 2,
  "type": "Differential",
  "variables": {
    "expressions": {},
    "poses": {}
  },
  "config": {
    "frontLeft": {
      "x": { "exp": "11 in", "val": 0.2794 },
      "y": { "exp": "11 in", "val": 0.2794 }
    },
    "backLeft": {
      "x": { "exp": "-11 in", "val": -0.2794 },
      "y": { "exp": "11 in", "val": 0.2794 }
    },
    "mass": { "exp": "0.8 kg", "val": 0.8 },
    "inertia": { "exp": "1e-6 kg m ^ 2", "val": 0.000001 },
    "gearing": { "exp": "1", "val": 1.0 },
    "radius": { "exp": "56 mm", "val": 0.056 },
    "vmax": { "exp": "150 RPM", "val": 15.707963267948966 },
    "tmax": { "exp": "0.04 N * m", "val": 0.04 },
    "cof": { "exp": "1.5", "val": 1.5 },
    "bumper": {
      "front": { "exp": "60 mm", "val": 0.06 },
      "side": { "exp": "50 mm", "val": 0.05 },
      "back": { "exp": "80 mm", "val": 0.08 }
    },
    "differentialTrackWidth": { "exp": "96.5 mm", "val": 0.0965 }
  },
  "generationFeatures": [],
  "codegen": {
    "root": "path/to/output",
    "genVars": true,
    "genTrajData": true,
    "useChoreoLib": true
  }
}
```

---

## Tuning Tips

### If robot is too slow on actual field

1. **Increase `vmax`**: Check if motor no-load speed is correct
2. **Check `gearing`**: Verify gear ratio calculation
3. **Increase `tmax`**: Check if motor torque specification is accurate

### If robot wheels slip during turns

1. **Decrease `cof`**: Lower friction coefficient
2. **Increase `mass`**: Verify robot weight (heavier = more normal force = more traction)
3. **Use `--accuracy-weight`**: Add smoothness penalty to reduce aggressive accelerations

### If robot overshoots waypoints

1. **Increase `--accuracy-weight`**: Add smoothness penalty (try 0.5 - 2.0)
2. **Decrease `vmax`**: Limit maximum speed
3. **Decrease `tmax`**: Limit maximum acceleration

### If optimization fails to converge

1. **Check parameter units**: Ensure all values are in SI units (meters, kg, radians, seconds)
2. **Verify `vmax` and `tmax`**: Inconsistent values can create infeasible constraints
3. **Increase `--samples`**: More collocation points can help convergence
4. **Simplify waypoints**: Start with 2-3 waypoints, then add more

---

## Common Mistakes

### Wrong Units

- **Incorrect:** `radius: 56` (interpreted as 56 meters!)
- **Correct:** `radius: 0.056` (56 mm in meters)

### Confusing RPM with rad/s

- **Incorrect:** `vmax: 150` (150 rad/s = 1432 RPM!)
- **Correct:** `vmax: 15.7` (150 RPM in rad/s)

### Forgetting Gear Ratio

- If your wheels are geared down 3:1, set `gearing: 3.0`, not `1.0`

### Unrealistic Friction

- `cof: 10.0` is physically impossible (most materials < 2.0)
- Typical FLL mat: 1.0 - 1.5

---

## Waypoint File Format

Waypoints are specified in a JSON file (`.json` extension). Each waypoint can include position, heading, and an optional stop constraint.

### Basic Waypoint Format

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0 },
  { "x": 1.0, "y": 0.5, "heading": 0.5 },
  { "x": 2.0, "y": 1.0, "heading": 1.0 }
]
```

### Waypoint Fields

- `x` (float, required): X position in meters
- `y` (float, required): Y position in meters
- `heading` (float|optional): Heading in radians
  - If omitted or `null`, heading is unconstrained at that waypoint
  - If specified, robot must face that direction at the waypoint
- `stop` (boolean, optional): Whether robot must come to complete rest at this waypoint
  - Default: `false`
  - If `true`, robot velocity is constrained to zero (vl=0, vr=0) at this waypoint
  - Useful for multi-segment missions where robot needs to pause between maneuvers
- `event` (string, optional): Event name to trigger at this waypoint
  - Default: none
  - If specified, the event name is embedded in the trajectory output at this waypoint
  - Used for FLL mission actions (e.g., "lower_arm", "release", "intake")
  - Events are preserved in controller export for on-robot execution

### Waypoints with Stops

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0, "stop": true },
  { "x": 0.5, "y": 0.0, "heading": 0.0, "stop": false },
  { "x": 0.5, "y": 0.3, "heading": 1.57, "stop": true },
  { "x": 1.0, "y": 0.3, "heading": 1.57, "stop": false },
  { "x": 1.0, "y": 0.0, "heading": 0.0, "stop": true }
]
```

In this example:

- Robot starts at rest at (0, 0)
- Moves to (0.5, 0) without stopping
- Comes to complete stop at (0.5, 0.3)
- Moves to (1.0, 0.3) without stopping
- Comes to complete stop at final waypoint (1.0, 0)

### Waypoints with Events

```json
[
  { "x": 0.0, "y": 0.0, "heading": 0.0 },
  { "x": 0.5, "y": 0.3, "heading": 0.5, "event": "lower_arm" },
  { "x": 1.0, "y": 0.0, "heading": 0.0 },
  { "x": 1.5, "y": 0.3, "heading": 0.0, "event": "release" }
]
```

In this example:

- Robot triggers "lower_arm" event at waypoint 1 (0.5, 0.3)
- Robot triggers "release" event at waypoint 3 (1.5, 0.3)
- Events are embedded in the trajectory output and preserved in controller export
- The robot controller reads the event field and executes the corresponding action

**CLI Override:**

You can also specify events via the CLI flag, which overrides JSON events:

```bash
python main.py -c fll_choreo.chor -w waypoints.json --events "2:lower_arm,5:release"
```

Format: `--events "index:event,index:event,..."` where index is the 0-based waypoint index.

### Alternative List Format

Waypoints can also be specified as a list of lists:

```json
[
  [0.0, 0.0, 0.0],
  [1.0, 0.5, 0.5],
  [2.0, 1.0, null]
]
```

Format: `[x, y, heading]` where heading can be `null` for unconstrained.

**Note:** The list format does not support the `stop` field. Use the object format for stop constraints.

---

## Parameter Calibration Procedure

This section provides a step-by-step procedure for measuring and calibrating robot parameters for accurate trajectory optimization.

### Step 1: Measure Physical Dimensions

**Mass:**

- Weigh the complete robot (including batteries, motors, and any attachments)
- Use a kitchen scale or precision balance
- Typical FLL robot: 0.5 - 1.5 kg

**Track Width:**

- Measure the distance between the centers of the left and right wheels
- For differential drive, this is the wheelbase
- Measure from wheel center to wheel center, not from tire edges
- Typical FLL robot: 80 - 120 mm

**Wheel Radius:**

- Measure the wheel diameter and divide by 2
- For wheels with tires, measure to the outer edge of the tire
- Account for tire compression under load (slightly smaller than unloaded)
- Typical FLL wheel: 20 - 60 mm

**Bumper Dimensions:**

- Measure from wheel center to front, side, and back bumpers
- These define the robot's footprint for collision checking
- Measure to the furthest point of the bumper/attachment

### Step 2: Determine Motor Specifications

**Motor No-Load Speed (vmax):**

- Check motor datasheet for no-load RPM
- Convert to rad/s: `vmax_rad_s = RPM * 2π / 60`
- If datasheet unavailable, measure by running motor at full voltage and measuring wheel speed
- Typical LEGO EV3 large motor: 150-170 RPM (no-load)

**Motor Stall Torque (tmax):**

- Check motor datasheet for stall torque
- If datasheet unavailable, use a torque wrench or spring scale to measure
- Apply force at wheel radius until motor stalls
- `tmax = force * wheel_radius`
- Typical LEGO EV3 large motor: 0.04 - 0.06 N·m

**Gearing:**

- Count teeth on input and output gears
- `gearing = output_teeth / input_teeth`
- For direct drive (no gears), use 1.0
- For gear reduction (slower output), use > 1.0
- For gear increase (faster output), use < 1.0

### Step 3: Estimate Moment of Inertia

**Simplified Calculation:**

- For a rectangular robot: `I = mass * (length² + width²) / 12`
- For a cylindrical robot: `I = mass * radius² / 2`

**More Accurate Method:**

- Use CAD software to calculate moment of inertia
- Or use the pendulum test: suspend robot from a pivot, measure oscillation period
- `I = mass * g * d * T² / (4π²)` where d is pivot distance, T is period

**Typical Values:**

- Small FLL robot: 1e-6 to 1e-4 kg·m²
- Larger robots: 1e-4 to 1e-3 kg·m²

### Step 4: Measure Coefficient of Friction

**Static Friction Test:**

1. Place robot on the actual competition surface (FLL mat)
2. Gradually incline the surface until robot starts sliding
3. Measure the angle: `cof = tan(angle)`
4. Repeat 3-5 times and average

**Pull Test:**

1. Use a spring scale to pull the robot horizontally
2. Measure the force required to start sliding
3. `cof = pull_force / (mass * gravity)`
4. Repeat in different directions

**Typical Values:**

- FLL mat with LEGO tires: 0.8 - 1.2
- FLL mat with rubber tires: 1.0 - 1.5
- Smooth surfaces: 0.3 - 0.6

### Step 5: Calibrate Using Trajectory Validation

**Initial Test:**

1. Generate a simple straight-line trajectory
2. Run validation: `python main.py -c config.chor -w test.json -o test.traj --validate`
3. Check constraint violations

**Adjust Motor Limits:**

- If motor force violations are high, reduce `vmax` or `tmax`
- If violations are consistently zero, you may be too conservative
- Target: < 5% of samples with minor violations (< 0.01 N)

**Adjust Friction:**

- If traction violations occur, increase `cof`
- If robot slips in real-world tests, decrease `cof`
- Target: No traction violations with realistic acceleration

**Adjust Inertia:**

- If robot turns faster than predicted, decrease `inertia`
- If robot turns slower than predicted, increase `inertia`
- This affects turning dynamics more than straight-line motion

### Step 6: Real-World Validation

**Test Trajectory:**

1. Generate a test trajectory with stops and turns
2. Export for controller: `--export-format controller`
3. Run on actual robot
4. Measure actual vs. planned positions

**Position Error Check:**

- Measure final position error (should be < 10 mm for typical FLL missions)
- If error is consistent in one direction, check wheel radius calibration
- If error varies, check friction or motor limits

**Time Check:**

- Compare planned vs. actual execution time
- If actual is slower, motor may be weaker than specified
- If actual is faster, motor may be stronger than specified

**Iterative Refinement:**

1. Adjust one parameter at a time
2. Re-test with same trajectory
3. Document changes and results
4. Repeat until errors are acceptable

### Step 7: Document Final Configuration

**Save Configuration:**

- Keep a copy of your calibrated config file
- Document measurement methods and dates
- Note any assumptions or approximations

**Version Control:**

- Use different config files for different robot builds
- Name them descriptively (e.g., `robot_v1.chor`, `robot_v2_with_arm.chor`)
- Track changes over time

### Common Calibration Mistakes

**Using Unloaded Wheel Radius:**

- Measure wheel radius with robot's full weight on it
- Tires compress under load, reducing effective radius
- Error: 2-5% if using unloaded radius

**Ignoring Gear Efficiency:**

- Gears have friction losses (typically 85-95% efficient)
- If using geared motors, reduce effective `tmax` by gear efficiency
- Error: 10-15% if ignoring losses

**Wrong Friction Surface:**

- Always test on the actual competition surface
- Different mats have different friction coefficients
- Error: 20-50% if using wrong surface

**Incorrect Inertia:**

- Don't forget to include attachments (arms, intakes) in inertia calculation
- Moving parts significantly affect rotational inertia
- Error: 50-200% if ignoring attachments

**Motor Specs at Wrong Voltage:**

- Motor specs are typically at rated voltage
- If running at different voltage, adjust specs proportionally
- Error: 10-30% if voltage mismatch

### Quick Calibration Checklist

- [ ] Weigh robot with all attachments
- [ ] Measure track width (wheel center to wheel center)
- [ ] Measure wheel radius under load
- [ ] Verify motor no-load speed (RPM → rad/s)
- [ ] Verify motor stall torque (N·m)
- [ ] Calculate gear ratio
- [ ] Estimate moment of inertia
- [ ] Measure coefficient of friction on actual surface
- [ ] Run validation test trajectory
- [ ] Adjust parameters based on validation results
- [ ] Test on real robot and measure errors
- [ ] Document final configuration

---

## Export Formats

The optimizer supports multiple export formats for trajectory consumption:

### Controller Export (JSON)

Exports a fixed-timestep trajectory for robot controllers:

```bash
python main.py -c config.chor -w waypoints.json -o output.traj \
  --export-format controller \
  --controller-dt 0.02
```

Output: `output_controller.json` with samples at fixed 20ms intervals.

### Python Export

Exports trajectory samples as a Python file for direct import:

```bash
python main.py -c config.chor -w waypoints.json -o output.traj \
  --export-format python
```

Output: `output.py` with a `samples` list containing trajectory data:

```python
samples = [
    {"t": 0.0, "x": 0.0, "y": 0.0, "heading": 0.0, "vl": 0.0, "vr": 0.0, "omega": 0.0},
    {"t": 0.02, "x": 0.01, "y": 0.0, "heading": 0.0, "vl": 0.5, "vr": 0.5, "omega": 0.0},
    # ... more samples
]
```

**Use case:** Direct integration with Python-based robot controllers or analysis scripts.

---

## Validation

After creating a configuration file, validate it by:

```bash
python main.py -c your_config.chor -w test_waypoints.json -o test.traj --validate
```

Check that:

- Optimization converges (no error messages)
- Constraint violations are zero
- Forward integration error is small (< 0.01 m)
