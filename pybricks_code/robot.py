"""
MAIN ENTRY POINT (HUB MENU)
---------------------------
This script acts as the "brain" for the robot. When you run this file, 
it opens a menu on the Hub's screen (1-9, 0). 
Pressing the hub buttons selects a mission to run.
"""

from pybricks.tools import hub_menu
# We import the hub from our config so we can check the battery
from robot_config import hub

print("Starting Robot...")
print(f"Battery: {hub.battery.voltage()}mV <- This value should be at least 8000 to run.")

# `hub_menu` creates an interactive menu on the hub.
# Use the Left/Right buttons to scroll through 1, 2, 3... and the Center button to select.
mission_selection = hub_menu(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
print(f"Selected Mission: {mission_selection}")

# Below is a routing table. Based on the selected number, we import or run 
# the corresponding mission file. 
# Importing a file automatically runs any code inside it unless protected by 
# `if __name__ == "__main__":`

if mission_selection == 1:
    import mission_1_simple
elif mission_selection == 2:
    import mission_2_async
elif mission_selection == 3:
    import mission_3_advanced
elif mission_selection == 4:
    import mission_4_ramsete
elif mission_selection == 5:
    import mission_5_lambdas
# elif mission_selection == 3:
#     import missions.mission_3_advanced
