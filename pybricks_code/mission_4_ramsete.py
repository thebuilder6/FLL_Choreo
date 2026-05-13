"""
MISSION 4: RAMSETE TRAJECTORY
-----------------------------
Runs the optimized path imported from complex_mission.py
"""

from robot_config import *
from complex_mission import samples as mission_samples
from complex_mission import config as mission_config

async def main():
    print("Starting Ramsete Mission...")
    
    # Optional: Reset gyro or set initial position if needed
    # initial_h = mission_samples[0]['heading']
    # hub.imu.reset_heading(math.degrees(initial_h))
    
    # Follow the optimized trajectory with physical constraints
    await follow_trajectory(drivebase, mission_samples, config=mission_config, debug=True, b=3.0, zeta=0.8)
    
    print("Mission Complete!")

if __name__ == "__main__" or __name__ == "mission_4_ramsete":
    run_task(main())
