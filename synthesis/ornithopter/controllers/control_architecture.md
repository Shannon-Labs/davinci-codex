# Ornithopter Control Architecture

## PX4 Mixer Layout
- **Main rotor outputs (CH1/CH2):** Differential flapping amplitude via 350 Nm servo actuators.
- **Tailplane pitch (CH3):** ±15° elevator for trim and flare.
- **Airspeed vane (CH4 input):** Provides feedback for amplitude scaling.
- **IMU fusion:** CubeOrange-class autopilot with RTK GNSS for attitude hold.

### Control Laws
1. **Roll loop:** `Δstroke = Kp_roll * φ_err + Kd_roll * p_rate` (limited to ±0.18 rad).
2. **Pitch loop:** `tail_cmd = Kp_pitch * θ_err + Ki_pitch * ∫θ_err dt`.
3. **Energy management:** Reduces flapping frequency when battery SoC < 30%.

## Sensors
- Dual IMUs (inboard/outboard) for vibration isolation.
- Differential pressure sensors mounted at wing roots for dynamic pressure feedback.
- Tailplane load cell to monitor structural saturation.

## Safety & Failsafes
- Automatic transition to glide mode if servo current > 90 A for longer than 4 s.
- Ballistic parachute deployment triggered on persistent negative lift margin.
- Manual takeover via tethered remote retains authority on CH1/CH3.
