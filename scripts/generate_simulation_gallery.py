"""Generate refreshed simulation gallery figures with tactile Renaissance aesthetics."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

OUTPUT_DIR = Path(__file__).resolve().parents[1] / "docs" / "images"
RNG = np.random.default_rng(1492)

plt.style.use("dark_background")
plt.rcParams.update(
    {
        "font.family": "DejaVu Sans",
        "axes.edgecolor": "#B3B6BB",
        "axes.labelcolor": "#F2F5F8",
        "xtick.color": "#D8DBDF",
        "ytick.color": "#D8DBDF",
        "figure.facecolor": "#1B1E23",
        "axes.facecolor": "#1F2329",
    }
)


def _ensure_output_dir() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def _save(fig: plt.Figure, name: str) -> None:
    path = OUTPUT_DIR / name
    fig.savefig(path, dpi=220, bbox_inches="tight")
    plt.close(fig)


def ornithopter_lift() -> None:
    time = np.linspace(0, 30, 600)
    climb_profile = 120 * np.log1p(time / 10) + 15 * np.sin(0.35 * time) + RNG.normal(0, 2.0, len(time))
    lift_mean = 1500 + 180 * np.sin(2.5 * time)
    lift_variation = 90 + 20 * np.sin(0.5 * time + 0.6)
    weight = np.full_like(time, 1350)

    fig, axes = plt.subplots(2, 1, figsize=(7, 6), sharex=True)

    axes[0].plot(time, climb_profile, color="#6EC5FF", linewidth=2.2, label="Altitude")
    axes[0].set_ylabel("Altitude (m)")
    axes[0].set_title("Ornithopter Flapping Campaign")
    axes[0].grid(alpha=0.2)

    axes[1].plot(time, lift_mean, color="#FDB57D", label="Instantaneous lift")
    axes[1].fill_between(
        time,
        lift_mean - lift_variation,
        lift_mean + lift_variation,
        alpha=0.25,
        color="#FDB57D",
        label="95% flutter band",
    )
    axes[1].plot(time, weight, color="#A3ADC2", linestyle="--", label="Gross weight")
    axes[1].set_ylabel("Force (N)")
    axes[1].set_xlabel("Time (s)")
    axes[1].grid(alpha=0.2)
    axes[1].legend(loc="upper right")

    _save(fig, "ornithopter_lift.png")


def parachute_descent() -> None:
    time = np.linspace(0, 35, 350)
    altitude = 400 - 11.5 * time + RNG.normal(0, 6.5, len(time)).cumsum() / 20
    velocity = -11.5 + RNG.normal(0, 0.6, len(time))
    drag = np.linspace(100, 900, 100)
    lift = drag * 0.82 + RNG.normal(0, 25, len(drag))

    fig, axes = plt.subplots(2, 2, figsize=(8, 6))
    fig.suptitle("Leonardo Pyramid Parachute Trial", fontsize=13)

    axes[0, 0].plot(time, np.clip(altitude, a_min=0, a_max=None), color="#7FDBFF")
    axes[0, 0].set_ylabel("Altitude (m)")
    axes[0, 0].grid(alpha=0.2)
    axes[0, 0].set_title("Descent Profile")

    axes[0, 1].plot(time, -velocity, color="#FFDC73")
    axes[0, 1].set_ylabel("Speed (m/s)")
    axes[0, 1].set_title("Descent Speed")
    axes[0, 1].grid(alpha=0.2)

    axes[1, 0].plot(drag, lift, color="#B4FF9F")
    axes[1, 0].set_xlabel("Drag (N)")
    axes[1, 0].set_ylabel("Lift (N)")
    axes[1, 0].set_title("Drag Polar")
    axes[1, 0].grid(alpha=0.2)

    base = np.array([0, 1, 2, 1, 0])
    radius = np.array([0.0, 0.9, 0.0, -0.9, 0.0])
    axes[1, 1].plot(base, 2.2 + radius, color="#93E5D4", linewidth=2.3)
    axes[1, 1].fill_between(base, 2.2 + radius, 0, alpha=0.25, color="#93E5D4")
    axes[1, 1].scatter([1], [0.1], color="#F5A9B8", marker="o", s=60)
    axes[1, 1].text(1.05, 0.25, "Pilot", color="#F5F5F5")
    axes[1, 1].set_xlim(-0.2, 2.2)
    axes[1, 1].set_ylim(-0.2, 2.6)
    axes[1, 1].axis("off")
    axes[1, 1].set_title("Planform & Center of Mass")

    for ax in axes.flat:
        ax.set_facecolor("#20242A")

    fig.tight_layout(rect=[0, 0, 1, 0.96])
    _save(fig, "parachute_descent.png")


def aerial_screw_performance() -> None:
    rpm = np.linspace(10, 160, 250)
    lift = 0.00035 * rpm**3 + RNG.normal(0, 0.05, len(rpm))
    required = 0.0028 * rpm**2
    power = 0.00018 * rpm**3

    fig, ax1 = plt.subplots(figsize=(6.8, 4.2))
    ax2 = ax1.twinx()
    ax1.plot(rpm, lift, color="#8EE6D8", linewidth=2.0, label="Generated lift")
    ax1.plot(rpm, required, color="#FF8F87", linestyle="--", linewidth=1.8, label="Required lift")
    ax1.set_xlabel("Rotor speed (RPM)")
    ax1.set_ylabel("Lift (kN)")
    ax1.grid(alpha=0.2)

    ax2.plot(rpm, power, color="#FFD966", linewidth=2.0, label="Power demand")
    ax2.set_ylabel("Power (kW)")

    ax1.set_title("Aerial Screw Power Envelope")
    ax1.legend(loc="upper left")
    ax2.legend(loc="upper right")

    _save(fig, "aerial_screw_performance.png")


def cart_motion() -> None:
    time = np.linspace(0, 25, 250)
    distance = 5.0 * np.sqrt(time) + 0.8 * np.sin(0.6 * time) + RNG.normal(0, 0.1, len(time))
    speed = np.gradient(distance, time)
    spring_force = 320 * np.exp(-time / 12) * np.cos(0.7 * time)

    fig, axes = plt.subplots(2, 1, figsize=(6.8, 5.5), sharex=True)

    axes[0].plot(time, distance, color="#6AA4FF", linewidth=2.1)
    axes[0].set_ylabel("Distance (m)")
    axes[0].set_title("Self-Propelled Cart Progress")
    axes[0].grid(alpha=0.2)

    axes[1].plot(time, speed, color="#F6B26B", linewidth=2.0, label="Speed")
    axes[1].plot(time, spring_force / 80, color="#A2F5B5", linestyle="--", linewidth=1.5, label="Spring force / 80")
    axes[1].set_ylabel("Speed (m/s)")
    axes[1].set_xlabel("Time (s)")
    axes[1].legend(loc="upper right")
    axes[1].grid(alpha=0.2)

    _save(fig, "cart_motion.png")


def odometer_error() -> None:
    sectors = np.arange(0, 360, 10)
    nominal = sectors / 360 * 1000
    wobble = 1.6 * np.sin(np.radians(sectors * 3))
    measured = nominal + wobble + RNG.normal(0, 0.8, len(sectors))

    fig, ax = plt.subplots(subplot_kw={"projection": "polar"}, figsize=(6, 5.6))
    theta = np.radians(sectors)
    ax.plot(theta, measured, color="#FEE191", linewidth=2.2, label="Measured distance")
    ax.plot(theta, nominal, color="#AEB8FE", linestyle="--", linewidth=1.5, label="Ideal distance")
    ax.fill_between(theta, nominal, measured, color="#FDD692", alpha=0.3)
    ax.set_title("Mechanical Odometer Sector Error", pad=20)
    ax.set_facecolor("#20242A")
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1))
    _save(fig, "odometer_error.png")


def main() -> None:
    _ensure_output_dir()
    ornithopter_lift()
    parachute_descent()
    aerial_screw_performance()
    cart_motion()
    odometer_error()


if __name__ == "__main__":
    main()
