# Configuration Guide

This guide explains how to configure the robot parameters for the FLL Trajectory Optimizer.

## Configuration File Format

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
    "mass": {"val": 0.8},
    "inertia": {"val": 0.000001},
    "differentialTrackWidth": {"val": 0.0965},
    "radius": {"val": 0.056},
    "vmax": {"val": 15.7},
    "tmax": {"val": 0.04},
    "gearing": {"val": 1.0},
    "cof": {"val": 1.5}
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
      "x": {"exp": "11 in", "val": 0.2794},
      "y": {"exp": "11 in", "val": 0.2794}
    },
    "backLeft": {
      "x": {"exp": "-11 in", "val": -0.2794},
      "y": {"exp": "11 in", "val": 0.2794}
    },
    "mass": {"exp": "0.8 kg", "val": 0.8},
    "inertia": {"exp": "1e-6 kg m ^ 2", "val": 0.000001},
    "gearing": {"exp": "1", "val": 1.0},
    "radius": {"exp": "56 mm", "val": 0.056},
    "vmax": {"exp": "150 RPM", "val": 15.707963267948966},
    "tmax": {"exp": "0.04 N * m", "val": 0.04},
    "cof": {"exp": "1.5", "val": 1.5},
    "bumper": {
      "front": {"exp": "60 mm", "val": 0.06},
      "side": {"exp": "50 mm", "val": 0.05},
      "back": {"exp": "80 mm", "val": 0.08}
    },
    "differentialTrackWidth": {"exp": "96.5 mm", "val": 0.0965}
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

## Validation

After creating a configuration file, validate it by:

```bash
python main.py -c your_config.chor -w test_waypoints.json -o test.traj --validate
```

Check that:
- Optimization converges (no error messages)
- Constraint violations are zero
- Forward integration error is small (< 0.01 m)
