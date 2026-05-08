# API Documentation: robot_model.py

Defines robot configuration and differential-drive kinematics/dynamics for trajectory optimization.

## Classes

### `RobotConfig`

Encapsulates physical robot parameters parsed from Choreo-style configuration files.

#### Constructor

```python
RobotConfig(config_dict: dict)
```

**Parameters:**
- `config_dict` (dict): Configuration dictionary with a `"config"` key containing robot parameters

**Extracted Parameters:**
- `mass` (float): Robot mass in kg (default: 0.8)
- `inertia` (float): Rotational inertia in kg·m² (default: 0.001)
- `track_width` (float): Distance between wheel centers in m (default: 0.0965)
- `wheel_radius` (float): Wheel radius in m (default: 0.028)
- `v_max_rad_s` (float): Motor no-load speed in rad/s (default: 15.7)
- `t_max_nm` (float): Motor stall torque in N·m (default: 0.04)
- `gearing` (float): Gear ratio (default: 1.0)
- `cof` (float): Coefficient of friction (default: 1.5)
- `g` (float): Gravitational acceleration (9.81 m/s²)

#### Methods

##### `get_max_force_at_velocity(v_wheel: float) -> float`

Calculates the maximum force magnitude a motor can apply at a given wheel velocity.

Uses a linear motor curve model where torque decreases linearly with speed until zero at no-load speed.

**Parameters:**
- `v_wheel` (float): Wheel linear velocity in m/s

**Returns:**
- (float): Maximum force in Newtons

**Model:**
```
omega = (v_wheel / wheel_radius) * gearing
torque = t_max * (1 - |omega| / v_max_rad_s)
torque = max(0, torque)  # No braking force above no-load speed
force = (torque / wheel_radius) * gearing
```

##### `max_linear_speed` (property)

Returns the no-load linear speed of the wheel in m/s.

**Returns:**
- (float): `v_max_rad_s * wheel_radius`

---

### `DifferentialDriveModel`

Implements differential-drive kinematics and dynamics for force calculations.

#### Constructor

```python
DifferentialDriveModel(config: RobotConfig)
```

**Parameters:**
- `config` (RobotConfig): Robot configuration object

#### Methods

##### `get_dynamics(vl: float, vr: float, al: float, ar: float) -> tuple[float, float]`

Computes the required wheel forces to achieve given velocities and accelerations.

**Parameters:**
- `vl` (float): Left wheel velocity in m/s
- `vr` (float): Right wheel velocity in m/s
- `al` (float): Left wheel acceleration in m/s²
- `ar` (float): Right wheel acceleration in m/s²

**Returns:**
- (tuple): `(fl, fr)` - Left and right wheel forces in Newtons

**Derivation:**
```
Linear acceleration: a = (al + ar) / 2
Angular acceleration: alpha = (ar - al) / track_width

Total force: F_total = mass * a
Total moment: M_total = inertia * alpha

Solve for wheel forces:
  F_total = fl + fr
  M_total = (fr - fl) * (track_width / 2)

  fr = (F_total + 2 * M_total / track_width) / 2
  fl = F_total - fr
```

##### `check_constraints(vl: float, vr: float, al: float, ar: float) -> list[float]`

Checks if a state/control is physically feasible.

**Parameters:**
- `vl` (float): Left wheel velocity in m/s
- `vr` (float): Right wheel velocity in m/s
- `al` (float): Left wheel acceleration in m/s²
- `ar` (float): Right wheel acceleration in m/s²

**Returns:**
- (list): Violation magnitudes (negative if OK, positive if violating)
  - Index 0: Left motor force violation (N)
  - Index 1: Right motor force violation (N)
  - Index 2: Traction limit violation (N)

**Constraints Checked:**
1. Motor limits: `|fl| <= max_force_at_velocity(vl)`
2. Motor limits: `|fr| <= max_force_at_velocity(vr)`
3. Traction limit: `|fl| + |fr| <= cof * mass * g`

**Usage Example:**
```python
from robot_model import RobotConfig, DifferentialDriveModel

config_dict = {
    "config": {
        "mass": {"val": 0.8},
        "inertia": {"val": 0.001},
        "differentialTrackWidth": {"val": 0.0965},
        # ... other parameters
    }
}

config = RobotConfig(config_dict)
model = DifferentialDriveModel(config)

# Check if a state is feasible
violations = model.check_constraints(vl=0.5, vr=0.6, al=1.0, ar=1.2)
if all(v <= 0 for v in violations):
    print("State is feasible")
else:
    print(f"Violations: {violations}")
```
