# Snowbotics Pybricks Template

Starting point for FLL robotics teams using Pybricks on the LEGO Spike Prime Hub.

---

## Quick Start

**Step 1 — Install Pybricks firmware on your Hub**
Go to [code.pybricks.com](https://code.pybricks.com/), connect your Hub, and follow the on-screen instructions to install the firmware.

**Step 2 — Set your motor and sensor ports**
Open `robot_config.py`. Find the `HARDWARE DEFINITIONS` section and change the port letters to match where your motors and sensors are physically plugged in on your robot.

**Step 3 — Run the robot**
Open `robot.py` in the Pybricks IDE and click **Run**. Use the **Left/Right** buttons on the Hub to scroll through mission numbers and the **Center** button to select one.

That's it! You're running code on the robot.

---

## Tutorials

Work through these in order. Each one builds on the last.

| Guide | What you'll learn |
|---|---|
| [**01 - Setup**](./TUTORIAL_01_SETUP.md) | How to configure `robot_config.py` for your specific robot. |
| [**02 - Hub Menu**](./TUTORIAL_02_HUB_MENU.md) | How to add and run missions from the Hub's built-in menu. |
| [**03 - Missions & Movement**](./TUTORIAL_03_MISSIONS.md) | The basic movement commands and how to make the robot do multiple things at once. |
| [**04 - Speed & Accuracy**](./TUTORIAL_04_SPEED_AND_ACCURACY.md) | Advanced techniques to save time and regain accuracy mid-match. |

---

## File Structure

```
.
├── robot.py                        # START HERE. The Hub menu — run this file!
├── robot_config.py                 # Hardware definitions (motors, sensors, drivebase)
│
├── mission_template.py             # Blank template — copy this to start a new mission
├── mission_1_simple.py             # Example: basic step-by-step movement
├── mission_2_async.py              # Example: doing multiple things at the same time
├── mission_3_advanced.py           # Example: full competitive run with all techniques
│
├── TUTORIAL_01_SETUP.md
├── TUTORIAL_02_HUB_MENU.md
├── TUTORIAL_03_MISSIONS.md
└── TUTORIAL_04_SPEED_AND_ACCURACY.md
```

---

## Resources
- [Pybricks Documentation](https://docs.pybricks.com/en/stable/)
- [Pybricks IDE](https://code.pybricks.com/)
