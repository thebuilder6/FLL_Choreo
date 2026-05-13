# Making It Yours: Configuring `robot_config.py`

Every mission in this project imports from one central file: **`robot_config.py`**. This file describes your robot's physical hardware to Pybricks — which ports your motors are in, how big your wheels are, and where your sensors are plugged in.

**You configure this once. Every mission picks it up automatically.**

Open `robot_config.py` and work through the checklist below.

---

## Checklist: What You Need to Change

### 1. Drive Motor Ports

Find these lines and update the port letters to match your robot:

```python
motorLeft  = Motor(Port.F, Direction.COUNTERCLOCKWISE)
motorRight = Motor(Port.B, Direction.CLOCKWISE)
```

The ports are labeled **A – F** on the side of the Spike Prime Hub. Trace the cable from your left drive wheel to the Hub to find its port letter.

> [!TIP]
> Not sure which motor is "left"? Stand behind the robot facing the same direction it faces. Left is on your left.

**Why is the left motor `COUNTERCLOCKWISE`?**  
The left and right drive motors are mounted facing opposite directions. Reversing the left motor's direction in code means both motors spin "forward" when given a positive speed.

📖 [Motor docs](https://docs.pybricks.com/en/stable/pupdevices/motor.html)

---

### 2. Attachment Motor Ports

```python
motorFront = Motor(Port.C, Direction.CLOCKWISE)
motorBack  = Motor(Port.D, Direction.CLOCKWISE)
```

Update port letters to match your attachment motors.  
**If you don't have an attachment motor, comment that line out:**

```python
# motorBack = Motor(Port.D, Direction.CLOCKWISE)
```

---

### 3. Sensor Ports

```python
colorSensorLeft  = ColorSensor(Port.E)
colorSensorRight = ColorSensor(Port.A)
```

Update the port letters to match your sensors.  
**If you don't have a sensor, comment it out** — otherwise the program will crash looking for hardware that isn't there.

📖 [ColorSensor docs](https://docs.pybricks.com/en/stable/pupdevices/colorsensor.html)

---

### 4. Wheel Measurements

Find the `DriveBase` line and enter your robot's measurements:

```python
drivebase = DriveBase(motorLeft, motorRight, wheel_diameter=56, axle_track=96.5)
```

| Parameter | What to measure | Unit |
|---|---|---|
| `wheel_diameter` | The diameter of one drive wheel | mm |
| `axle_track` | The distance between the **center** of the left tire and the **center** of the right tire | mm |

> [!IMPORTANT]
> These two numbers directly control how far the robot thinks it has traveled. Even 1mm of error in `wheel_diameter` will cause every movement to consistently overshoot or undershoot.
>
> **Tip:** After setting these, write a quick test mission that drives 500mm forward and 500mm back. If the robot doesn't land exactly where it started, adjust your measurements.

📖 [DriveBase docs & calibration tips](https://docs.pybricks.com/en/stable/robotics.html)

---

## Confirming It Works

Run `robot.py`. As soon as the Hub starts, it will print to the Pybricks console:

```
Battery Voltage: 8234 mV
```

If you see this, `robot_config.py` is loading correctly. If the Hub warns you the voltage is below 8000mV, **charge or swap your battery** before running — a weak battery causes inconsistent motor behavior.

📖 [PrimeHub docs](https://docs.pybricks.com/en/stable/hubs/primehub.html)

---

## Advanced: Hub Orientation (Non-Flat Mounting Only)

> [!NOTE]
> **Skip this if your Hub is mounted flat** — screen facing up, USB port facing the front of the robot. That is the default orientation and requires no changes.

If your Hub is mounted on its side or at an angle, you must tell Pybricks which direction is "up" and which is "forward" so the built-in gyroscope reads correctly. Look for the tiny **X, Y, Z arrows** molded into the Hub's casing:

```python
hub = PrimeHub(top_side=Axis.Y, front_side=Axis.X)
```

- `top_side` — which axis arrow points straight up toward the ceiling?
- `front_side` — which axis arrow points toward the front of the robot?

Standard flat mounting: `top_side=Axis.Z, front_side=Axis.Y`

📖 [PrimeHub orientation docs](https://docs.pybricks.com/en/stable/hubs/primehub.html#pybricks.hubs.PrimeHub)

---

**Next Up:** [02 - Running Your Missions](./TUTORIAL_02_HUB_MENU.md)
