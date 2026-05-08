import numpy as np

class RobotConfig:
    def __init__(self, config_dict):
        # Extract from Choreo-like config
        cfg = config_dict.get("config", {})
        self.mass = cfg.get("mass", {}).get("val", 0.8)
        self.inertia = cfg.get("inertia", {}).get("val", 0.001)
        self.track_width = cfg.get("differentialTrackWidth", {}).get("val", 0.0965)
        self.wheel_radius = cfg.get("radius", {}).get("val", 0.028) # Default if missing
        
        # Motor specs
        self.v_max_rad_s = cfg.get("vmax", {}).get("val", 15.7) # RPM to rad/s
        self.t_max_nm = cfg.get("tmax", {}).get("val", 0.04)
        self.gearing = cfg.get("gearing", {}).get("val", 1.0)
        
        # Friction
        self.cof = cfg.get("cof", {}).get("val", 1.5)
        self.g = 9.81

    def get_max_force_at_velocity(self, v_wheel):
        """
        Calculates max force magnitude a motor can apply at a given wheel velocity.
        Uses a linear motor curve (symmetric braking/driving limit).
        """
        omega = (v_wheel / self.wheel_radius) * self.gearing
        torque = self.t_max_nm * (1.0 - abs(omega) / self.v_max_rad_s)
        torque = max(0, torque)
        force = (torque / self.wheel_radius) * self.gearing
        return force

    @property
    def max_linear_speed(self):
        """No-load linear speed of the wheel (m/s)."""
        return self.v_max_rad_s * self.wheel_radius

class DifferentialDriveModel:
    def __init__(self, config: RobotConfig):
        self.cfg = config

    def get_dynamics(self, vl, vr, al, ar):
        """
        Returns required forces and moments for given velocities and accelerations.
        """
        # Linear acceleration: a = (al + ar) / 2
        # Angular acceleration: alpha = (ar - al) / track_width
        a = (al + ar) / 2.0
        alpha = (ar - al) / self.cfg.track_width
        
        # F_total = m * a
        # M_total = I * alpha
        f_total = self.cfg.mass * a
        m_total = self.cfg.inertia * alpha
        
        # f_total = fl + fr
        # m_total = (fr - fl) * (w / 2)
        # Solve for fl, fr:
        # fr - fl = 2 * m_total / w
        # 2*fr = f_total + 2 * m_total / w
        fr = (f_total + (2.0 * m_total / self.cfg.track_width)) / 2.0
        fl = f_total - fr
        
        return fl, fr

    def check_constraints(self, vl, vr, al, ar):
        """
        Checks if the state/control is physically possible.
        Returns a list of violations (negative if OK, positive if violating).
        """
        fl, fr = self.get_dynamics(vl, vr, al, ar)
        
        # 1. Motor limits
        max_fl = self.cfg.get_max_force_at_velocity(vl)
        max_fr = self.cfg.get_max_force_at_velocity(vr)
        
        violations = [
            abs(fl) - max_fl,
            abs(fr) - max_fr
        ]
        
        # 2. Traction limit (Simplified: total force <= mu * m * g)
        # More accurately: each wheel force <= mu * N_wheel
        # For simplicity in FLL (where robots are often unbalanced):
        # abs(fl) + abs(fr) <= mu * m * g
        f_traction_max = self.cfg.cof * self.cfg.mass * self.cfg.g
        violations.append(abs(fl) + abs(fr) - f_traction_max)
        
        return violations
