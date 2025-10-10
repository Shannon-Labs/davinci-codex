"""
Mechanical Programming Logic for Leonardo's Mechanical Lion
Complete control system coordination and sequential logic

Historical Context:
- First programmable automation controller in history
- Leonardo's cam-based mechanical computer system
- 16th century breakthrough in sequential control
- Foundation of modern automation and robotics

Engineering Innovation:
- Multi-channel mechanical coordination
- Sequential event programming
- State machine implementation with cams
- Theatrical timing and synchronization
"""

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

import matplotlib.pyplot as plt
import numpy as np


class MechanicalState(Enum):
    """Mechanical system states for the lion automaton"""
    IDLE = "idle"
    INITIALIZING = "initializing"
    WALKING = "walking"
    PAUSING = "pausing"
    CHEST_OPENING = "chest_opening"
    LILY_PRESENTING = "lily_presenting"
    ROYAL_DISPLAY = "royal_display"
    RESETTING = "resetting"
    EMERGENCY_STOP = "emergency_stop"

@dataclass
class MechanicalChannel:
    """Individual mechanical control channel"""
    name: str
    channel_id: int
    current_position: float = 0.0  # 0.0 to 1.0
    target_position: float = 0.0
    current_state: MechanicalState = MechanicalState.IDLE
    cam_profile: Optional[str] = None
    mechanical_system: str = ""
    dependencies: Set[int] = field(default_factory=set)
    dependents: Set[int] = field(default_factory=set)
    safety_limits: Tuple[float, float] = (0.0, 1.0)
    emergency_stop: bool = False

@dataclass
class ControlEvent:
    """Control event in the programming sequence"""
    event_id: str
    trigger_time: float
    trigger_condition: str  # "time", "state", "position", "external"
    trigger_value: any
    target_channels: List[int]
    target_states: List[MechanicalState]
    target_positions: List[float]
    duration: float
    priority: int  # 1=highest, 10=lowest
    safety_interlocks: List[str] = field(default_factory=list)

@dataclass
class SystemStatus:
    """Current status of the mechanical system"""
    overall_state: MechanicalState
    channel_states: Dict[int, MechanicalState]
    performance_time: float
    active_events: List[str]
    completed_events: List[str]
    safety_status: str
    error_conditions: List[str]
    performance_metrics: Dict[str, float]

class MechanicalProgrammingController:
    """
    Complete mechanical programming controller for Leonardo's Mechanical Lion

    This class implements the first programmable automation controller,
    using cam-based programming to coordinate multiple mechanical systems
    in a theatrical performance sequence.
    """

    def __init__(self):
        # System parameters
        self.total_performance_time = 26.5  # seconds
        self.num_channels = 8
        self.clock_frequency = 10.0  # Hz (mechanical clock speed)
        self.safety_check_interval = 0.1  # seconds

        # Initialize mechanical channels
        self.channels = self._initialize_channels()

        # Programming sequence
        self.control_events = []
        self.current_time = 0.0
        self.system_status = SystemStatus(
            overall_state=MechanicalState.IDLE,
            channel_states=dict.fromkeys(range(self.num_channels), MechanicalState.IDLE),
            performance_time=0.0,
            active_events=[],
            completed_events=[],
            safety_status="safe",
            error_conditions=[],
            performance_metrics={}
        )

        # Safety systems
        self.emergency_stop_triggered = False
        self.safety_interlocks = {
            "chest_collision": False,
            "leg_collision": False,
            "overextension": False,
            "power_failure": False,
            "mechanical_jam": False
        }

        # Performance monitoring
        self.performance_log = []
        self.error_log = []

        # Create control programming
        self._create_performance_program()

    def _initialize_channels(self) -> Dict[int, MechanicalChannel]:
        """Initialize all mechanical control channels"""
        channels = {}

        # Channel definitions for the lion automaton
        channel_specs = {
            0: {"name": "front_left_leg", "system": "walking_mechanism"},
            1: {"name": "front_right_leg", "system": "walking_mechanism"},
            2: {"name": "rear_left_leg", "system": "walking_mechanism"},
            3: {"name": "rear_right_leg", "system": "walking_mechanism"},
            4: {"name": "tail_actuator", "system": "tail_mechanism"},
            5: {"name": "chest_mechanism", "system": "chest_reveal"},
            6: {"name": "lily_platform", "system": "lily_presentation"},
            7: {"name": "master_timing", "system": "timing_controller"}
        }

        for channel_id, specs in channel_specs.items():
            channels[channel_id] = MechanicalChannel(
                name=specs["name"],
                channel_id=channel_id,
                mechanical_system=specs["system"],
                safety_limits=(0.0, 1.0)
            )

        # Set up channel dependencies
        # Chest and lily depend on walking completion
        channels[5].dependencies.add(0)  # chest depends on front left leg
        channels[5].dependencies.add(1)  # chest depends on front right leg
        channels[5].dependencies.add(2)  # chest depends on rear left leg
        channels[5].dependencies.add(3)  # chest depends on rear right leg

        channels[6].dependencies.add(5)  # lily depends on chest

        # Set up dependents
        for channel_id, channel in channels.items():
            for dep_id in channel.dependencies:
                if dep_id in channels:
                    channels[dep_id].dependents.add(channel_id)

        return channels

    def _create_performance_program(self) -> None:
        """
        Create the complete performance programming sequence

        This function generates the control events that program the
        mechanical lion's complete 26.5-second theatrical performance.
        """
        self.control_events = []

        # EVENT 1: Initialize position (0.0 - 2.0 seconds)
        self.control_events.append(ControlEvent(
            event_id="initial_position",
            trigger_time=0.0,
            trigger_condition="time",
            trigger_value=0.0,
            target_channels=[0, 1, 2, 3, 4, 5, 6, 7],
            target_states=[MechanicalState.INITIALIZING] * 8,
            target_positions=[0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0],
            duration=2.0,
            priority=1,
            safety_interlocks=["no_leg_collision", "chest_closed"]
        ))

        # EVENT 2: Begin walking sequence (2.0 - 10.0 seconds)
        # Three complete walking cycles
        for step in range(3):
            step_start = 2.0 + step * 2.67

            # Step up phase
            self.control_events.append(ControlEvent(
                event_id=f"step_{step+1}_lift",
                trigger_time=step_start,
                trigger_condition="time",
                trigger_value=step_start,
                target_channels=[0, 1, 2, 3, 4],
                target_states=[MechanicalState.WALKING] * 5,
                target_positions=[
                    np.sin(np.pi * (step + 0.5)),   # front left leg
                    np.sin(np.pi * step),           # front right leg
                    np.sin(np.pi * step),           # rear left leg
                    np.sin(np.pi * (step + 0.5)),   # rear right leg
                    0.3 + 0.2 * np.sin(4 * np.pi * (step + 0.25))  # tail
                ],
                duration=0.8,
                priority=2,
                safety_interlocks=["leg_clearance", "tail_clearance"]
            ))

            # Step down phase
            self.control_events.append(ControlEvent(
                event_id=f"step_{step+1}_place",
                trigger_time=step_start + 0.8,
                trigger_condition="time",
                trigger_value=step_start + 0.8,
                target_channels=[0, 1, 2, 3, 4],
                target_states=[MechanicalState.WALKING] * 5,
                target_positions=[
                    np.sin(np.pi * (step + 1.5)),   # front left leg
                    np.sin(np.pi * (step + 1.0)),   # front right leg
                    np.sin(np.pi * (step + 1.0)),   # rear left leg
                    np.sin(np.pi * (step + 1.5)),   # rear right leg
                    0.3 + 0.2 * np.sin(4 * np.pi * (step + 0.75))  # tail
                ],
                duration=0.8,
                priority=2,
                safety_interlocks=["leg_ground_contact", "stability_check"]
            ))

            # Pause phase
            self.control_events.append(ControlEvent(
                event_id=f"step_{step+1}_pause",
                trigger_time=step_start + 1.6,
                trigger_condition="time",
                trigger_value=step_start + 1.6,
                target_channels=[0, 1, 2, 3, 4],
                target_states=[MechanicalState.PAUSING] * 5,
                target_positions=[0.0, 0.0, 0.0, 0.0, 0.4 + 0.1 * np.sin(2 * np.pi * (step + 0.5))],
                duration=1.07,
                priority=3,
                safety_interlocks=["system_stable"]
            ))

        # EVENT 3: Prepare for reveal (10.0 - 12.0 seconds)
        self.control_events.append(ControlEvent(
            event_id="stopping_position",
            trigger_time=10.0,
            trigger_condition="time",
            trigger_value=10.0,
            target_channels=[0, 1, 2, 3, 4, 7],
            target_states=[MechanicalState.PAUSING] * 6,
            target_positions=[0.0, 0.0, 0.0, 0.0, 0.2, 0.0],
            duration=2.0,
            priority=2,
            safety_interlocks=["all_stable", "chest_locked"]
        ))

        # EVENT 4: Chest opening sequence (12.0 - 15.5 seconds)
        self.control_events.append(ControlEvent(
            event_id="chest_opening",
            trigger_time=12.0,
            trigger_condition="time",
            trigger_value=12.0,
            target_channels=[5, 7],
            target_states=[MechanicalState.CHEST_OPENING, MechanicalState.CHEST_OPENING],
            target_positions=[1.0, 1.0],
            duration=3.5,
            priority=1,
            safety_interlocks=["chest_clear", "lily_retracted"]
        ))

        # EVENT 5: Lily presentation (15.5 - 17.5 seconds)
        self.control_events.append(ControlEvent(
            event_id="lily_presentation",
            trigger_time=15.5,
            trigger_condition="state",
            trigger_value=MechanicalState.CHEST_OPENING,
            target_channels=[6, 7],
            target_states=[MechanicalState.LILY_PRESENTING, MechanicalState.LILY_PRESENTING],
            target_positions=[1.0, 1.0],
            duration=2.0,
            priority=1,
            safety_interlocks=["chest_open", "platform_clear"]
        ))

        # EVENT 6: Royal display (17.5 - 22.5 seconds)
        self.control_events.append(ControlEvent(
            event_id="royal_display",
            trigger_time=17.5,
            trigger_condition="time",
            trigger_value=17.5,
            target_channels=[4, 5, 6, 7],
            target_states=[MechanicalState.ROYAL_DISPLAY] * 4,
            target_positions=[0.25, 1.0, 1.0, 0.5],
            duration=5.0,
            priority=2,
            safety_interlocks=["display_stable"]
        ))

        # EVENT 7: Reset sequence (22.5 - 26.5 seconds)
        self.control_events.append(ControlEvent(
            event_id="reset_sequence",
            trigger_time=22.5,
            trigger_condition="time",
            trigger_value=22.5,
            target_channels=[0, 1, 2, 3, 4, 5, 6, 7],
            target_states=[MechanicalState.RESETTING] * 8,
            target_positions=[0.0, 0.0, 0.0, 0.0, 0.1, 0.0, 0.0, 0.0],
            duration=4.0,
            priority=1,
            safety_interlocks=["safe_reset"]
        ))

        # Sort events by trigger time and priority
        self.control_events.sort(key=lambda e: (e.trigger_time, e.priority))

    def execute_performance_cycle(self, dt: float) -> SystemStatus:
        """
        Execute one cycle of the performance control logic

        This function processes control events, updates channel states,
        and monitors safety conditions during the performance.
        """
        # Update system time
        self.current_time += dt
        self.system_status.performance_time = self.current_time

        # Check safety conditions
        self._perform_safety_checks()

        # Process triggered events
        self._process_triggered_events()

        # Update channel positions and states
        self._update_channel_states(dt)

        # Check for event completion
        self._check_event_completion()

        # Update system status
        self._update_system_status()

        # Log performance metrics
        self._log_performance_metrics()

        return self.system_status

    def _process_triggered_events(self) -> None:
        """Process control events that should be triggered"""
        for event in self.control_events:
            if event.event_id in self.system_status.completed_events:
                continue  # Already completed

            if event.event_id in self.system_status.active_events:
                continue  # Already active

            # Check trigger condition
            should_trigger = False

            if event.trigger_condition == "time":
                should_trigger = self.current_time >= event.trigger_time
            elif event.trigger_condition == "state":
                # Check if any channel is in the required state
                for channel_id in range(self.num_channels):
                    if self.channels[channel_id].current_state == event.trigger_value:
                        should_trigger = True
                        break

            if should_trigger:
                # Check safety interlocks
                if self._check_safety_interlocks(event.safety_interlocks):
                    self._trigger_event(event)
                else:
                    self.error_log.append(f"Safety interlock blocked event: {event.event_id}")

    def _trigger_event(self, event: ControlEvent) -> None:
        """Trigger a control event and activate target channels"""
        # Check dependencies
        for channel_id in event.target_channels:
            channel = self.channels[channel_id]
            for dep_id in channel.dependencies:
                if self.channels[dep_id].current_state != MechanicalState.IDLE:
                    # Dependency not satisfied, delay event
                    return

        # Activate event
        self.system_status.active_events.append(event.event_id)

        # Update target channels
        for i, channel_id in enumerate(event.target_channels):
            if channel_id < self.num_channels:
                channel = self.channels[channel_id]
                channel.current_state = event.target_states[i]
                channel.target_position = event.target_positions[i]

        self.performance_log.append({
            "time": self.current_time,
            "event": "triggered",
            "event_id": event.event_id,
            "target_channels": event.target_channels
        })

    def _update_channel_states(self, dt: float) -> None:
        """Update the position and state of all channels"""
        for _channel_id, channel in self.channels.items():
            if channel.current_state == MechanicalState.IDLE:
                continue

            # Calculate position update based on state
            if channel.current_state in [MechanicalState.WALKING, MechanicalState.CHEST_OPENING,
                                        MechanicalState.LILY_PRESENTING]:
                # Move toward target position
                position_diff = channel.target_position - channel.current_position
                move_rate = 2.0  # positions per second

                if abs(position_diff) > 0.01:
                    channel.current_position += np.sign(position_diff) * min(abs(position_diff), move_rate * dt)
                else:
                    channel.current_position = channel.target_position

            # Check safety limits
            if channel.current_position < channel.safety_limits[0]:
                channel.current_position = channel.safety_limits[0]
                self.error_log.append(f"Channel {channel.name} hit minimum limit")
            elif channel.current_position > channel.safety_limits[1]:
                channel.current_position = channel.safety_limits[1]
                self.error_log.append(f"Channel {channel.name} hit maximum limit")

    def _check_event_completion(self) -> None:
        """Check if any active events have completed"""
        completed_events = []

        for event_id in self.system_status.active_events:
            event = next((e for e in self.control_events if e.event_id == event_id), None)
            if not event:
                continue

            # Check if all target channels have reached their positions
            all_channels_complete = True
            for channel_id in event.target_channels:
                if channel_id < self.num_channels:
                    channel = self.channels[channel_id]
                    if abs(channel.current_position - channel.target_position) > 0.01:
                        all_channels_complete = False
                        break

            if all_channels_complete:
                completed_events.append(event_id)

                # Return channels to idle state
                for channel_id in event.target_channels:
                    if channel_id < self.num_channels:
                        self.channels[channel_id].current_state = MechanicalState.IDLE

        # Move completed events
        for event_id in completed_events:
            self.system_status.active_events.remove(event_id)
            self.system_status.completed_events.append(event_id)

            self.performance_log.append({
                "time": self.current_time,
                "event": "completed",
                "event_id": event_id
            })

    def _perform_safety_checks(self) -> None:
        """Perform all safety system checks"""
        # Check for mechanical collisions
        self._check_mechanical_collisions()

        # Check power systems
        self._check_power_systems()

        # Check emergency conditions
        self._check_emergency_conditions()

        # Update safety status
        if any(self.safety_interlocks.values()):
            self.system_status.safety_status = "warning"
        else:
            self.system_status.safety_status = "safe"

    def _check_mechanical_collisions(self) -> None:
        """Check for potential mechanical collisions"""
        # Check leg collisions
        leg_positions = [self.channels[i].current_position for i in range(4)]
        if abs(leg_positions[0] - leg_positions[1]) < 0.1:  # Front legs
            self.safety_interlocks["leg_collision"] = True
        if abs(leg_positions[2] - leg_positions[3]) < 0.1:  # Rear legs
            self.safety_interlocks["leg_collision"] = True

        # Check chest collision with legs
        chest_open = self.channels[5].current_position > 0.5
        any_leg_up = any(pos > 0.5 for pos in leg_positions)
        if chest_open and any_leg_up:
            self.safety_interlocks["chest_collision"] = True

    def _check_power_systems(self) -> None:
        """Check power system status"""
        # Simulate power system check
        # In real system, this would check spring tension, etc.
        power_available = self.current_time < self.total_performance_time
        if not power_available:
            self.safety_interlocks["power_failure"] = True

    def _check_emergency_conditions(self) -> None:
        """Check for emergency stop conditions"""
        if self.emergency_stop_triggered:
            for channel in self.channels.values():
                channel.emergency_stop = True
                channel.current_state = MechanicalState.EMERGENCY_STOP

    def _check_safety_interlocks(self, interlocks: List[str]) -> bool:
        """Check if all safety interlocks are satisfied"""
        for interlock in interlocks:
            if interlock == "no_leg_collision" and self.safety_interlocks["leg_collision"] or interlock == "chest_closed" and self.channels[5].current_position > 0.1 or interlock == "chest_clear" and self.safety_interlocks["chest_collision"] or interlock == "system_stable" and self.system_status.safety_status != "safe":
                return False

        return True

    def _update_system_status(self) -> None:
        """Update overall system status"""
        # Update channel states
        for channel_id, channel in self.channels.items():
            self.system_status.channel_states[channel_id] = channel.current_state

        # Determine overall state
        if self.emergency_stop_triggered:
            self.system_status.overall_state = MechanicalState.EMERGENCY_STOP
        elif any(s == MechanicalState.WALKING for s in self.system_status.channel_states.values()):
            self.system_status.overall_state = MechanicalState.WALKING
        elif any(s == MechanicalState.CHEST_OPENING for s in self.system_status.channel_states.values()):
            self.system_status.overall_state = MechanicalState.CHEST_OPENING
        elif any(s == MechanicalState.LILY_PRESENTING for s in self.system_status.channel_states.values()):
            self.system_status.overall_state = MechanicalState.LILY_PRESENTING
        elif any(s == MechanicalState.ROYAL_DISPLAY for s in self.system_status.channel_states.values()):
            self.system_status.overall_state = MechanicalState.ROYAL_DISPLAY
        elif any(s == MechanicalState.RESETTING for s in self.system_status.channel_states.values()):
            self.system_status.overall_state = MechanicalState.RESETTING
        else:
            self.system_status.overall_state = MechanicalState.IDLE

        # Update error conditions
        self.system_status.error_conditions = [
            condition for condition, active in self.safety_interlocks.items() if active
        ]

    def _log_performance_metrics(self) -> None:
        """Log performance metrics for analysis"""
        metrics = {
            "time": self.current_time,
            "overall_state": self.system_status.overall_state.value,
            "active_events": len(self.system_status.active_events),
            "completed_events": len(self.system_status.completed_events),
            "channel_positions": {ch.name: ch.current_position for ch in self.channels.values()},
            "safety_status": self.system_status.safety_status,
            "error_count": len(self.system_status.error_conditions)
        }

        self.system_status.performance_metrics = metrics

    def simulate_complete_performance(self, time_step: float = 0.01) -> Dict:
        """
        Simulate the complete mechanical lion performance

        This function runs the full 26.5-second performance and returns
        detailed analysis of the mechanical programming operation.
        """
        print("Starting complete performance simulation...")
        print(f"Total duration: {self.total_performance_time} seconds")
        print(f"Control events: {len(self.control_events)}")
        print(f"Control channels: {self.num_channels}")
        print()

        # Reset system
        self.current_time = 0.0
        self.system_status = SystemStatus(
            overall_state=MechanicalState.IDLE,
            channel_states=dict.fromkeys(range(self.num_channels), MechanicalState.IDLE),
            performance_time=0.0,
            active_events=[],
            completed_events=[],
            safety_status="safe",
            error_conditions=[],
            performance_metrics={}
        )

        # Clear logs
        self.performance_log = []
        self.error_log = []

        # Simulation data collection
        simulation_data = {
            "time": [],
            "channel_positions": {ch.name: [] for ch in self.channels.values()},
            "system_states": [],
            "active_events": [],
            "safety_status": []
        }

        # Run simulation
        steps = int(self.total_performance_time / time_step)
        for step in range(steps):
            status = self.execute_performance_cycle(time_step)

            # Collect data
            simulation_data["time"].append(self.current_time)
            simulation_data["system_states"].append(status.overall_state.value)
            simulation_data["active_events"].append(len(status.active_events))
            simulation_data["safety_status"].append(status.safety_status)

            for channel in self.channels.values():
                simulation_data["channel_positions"][channel.name].append(channel.current_position)

            # Progress indicator
            if step % 100 == 0:
                progress = (step / steps) * 100
                print(f"Progress: {progress:.1f}% - Time: {self.current_time:.1f}s - "
                      f"State: {status.overall_state.value}")

        print("\nSimulation complete!")

        # Analyze results
        analysis = self._analyze_simulation_results(simulation_data)

        return {
            "simulation_data": simulation_data,
            "performance_log": self.performance_log,
            "error_log": self.error_log,
            "analysis": analysis
        }

    def _analyze_simulation_results(self, data: Dict) -> Dict:
        """Analyze the simulation results"""
        total_events = len(self.control_events)
        completed_events = len(self.system_status.completed_events)
        total_errors = len(self.error_log)

        # Calculate timing accuracy
        expected_events = total_events
        actual_events = completed_events
        success_rate = actual_events / expected_events if expected_events > 0 else 0

        # Calculate channel utilization
        channel_utilization = {}
        for channel_name, positions in data["channel_positions"].items():
            active_time = sum(1 for pos in positions if pos > 0.01)
            utilization = active_time / len(positions)
            channel_utilization[channel_name] = utilization

        # Safety performance
        safe_time_percentage = sum(1 for status in data["safety_status"] if status == "safe") / len(data["safety_status"])

        return {
            "total_events_planned": total_events,
            "events_completed": completed_events,
            "success_rate": success_rate,
            "total_errors": total_errors,
            "channel_utilization": channel_utilization,
            "safety_performance": {
                "safe_time_percentage": safe_time_percentage,
                "total_safety_violations": len(self.error_log)
            },
            "performance_summary": {
                "total_duration": data["time"][-1],
                "average_active_events": np.mean(data["active_events"]),
                "peak_active_events": np.max(data["active_events"]),
                "state_changes": len(set(data["system_states"]))
            }
        }

    def create_programming_visualization(self, simulation_data: Dict, save_path: Optional[str] = None) -> None:
        """Create comprehensive visualization of the programming logic"""
        fig, axes = plt.subplots(4, 1, figsize=(16, 12))

        # 1. Channel positions over time
        ax1 = axes[0]
        for channel_name, positions in simulation_data["channel_positions"].items():
            ax1.plot(simulation_data["time"], positions, label=channel_name.replace('_', ' ').title(),
                    linewidth=2)

        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Channel Position (0-1)')
        ax1.set_title('Mechanical Channel Positions During Performance', fontweight='bold')
        ax1.legend(loc='upper right')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, self.total_performance_time)

        # 2. System states over time
        ax2 = axes[1]
        state_numeric = []
        state_map = {
            'idle': 0, 'initializing': 1, 'walking': 2, 'pausing': 3,
            'chest_opening': 4, 'lily_presenting': 5, 'royal_display': 6, 'resetting': 7
        }
        for state in simulation_data["system_states"]:
            state_numeric.append(state_map.get(state, 0))

        ax2.plot(simulation_data["time"], state_numeric, 'b-', linewidth=2)
        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('System State')
        ax2.set_title('System State Transitions', fontweight='bold')
        ax2.set_yticks(list(state_map.values()))
        ax2.set_yticklabels(list(state_map.keys()))
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, self.total_performance_time)

        # 3. Active events over time
        ax3 = axes[2]
        ax3.plot(simulation_data["time"], simulation_data["active_events"], 'g-', linewidth=2)
        ax3.fill_between(simulation_data["time"], 0, simulation_data["active_events"], alpha=0.3, color='green')
        ax3.set_xlabel('Time (seconds)')
        ax3.set_ylabel('Number of Active Events')
        ax3.set_title('Concurrent Event Activity', fontweight='bold')
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0, self.total_performance_time)

        # 4. Safety status over time
        ax4 = axes[3]
        safety_numeric = [1 if status == "safe" else 0 for status in simulation_data["safety_status"]]
        ax4.plot(simulation_data["time"], safety_numeric, 'r-', linewidth=2)
        ax4.fill_between(simulation_data["time"], 0, safety_numeric, alpha=0.3, color='red')
        ax4.set_xlabel('Time (seconds)')
        ax4.set_ylabel('Safety Status')
        ax4.set_title('Safety System Status', fontweight='bold')
        ax4.set_yticks([0, 1])
        ax4.set_yticklabels(['Warning', 'Safe'])
        ax4.grid(True, alpha=0.3)
        ax4.set_xlim(0, self.total_performance_time)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def export_programming_documentation(self, output_dir: str) -> None:
        """Export complete programming documentation"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Create programming documentation
        doc = {
            "project": "Leonardo's Mechanical Lion - Mechanical Programming Logic",
            "date": "1517",
            "designer": "Leonardo da Vinci",
            "system_type": "First programmable automation controller",
            "total_channels": self.num_channels,
            "total_events": len(self.control_events),
            "performance_duration": self.total_performance_time,
            "control_channels": {},
            "programming_events": [],
            "safety_systems": self.safety_interlocks,
            "technical_specifications": {
                "clock_frequency": self.clock_frequency,
                "safety_check_interval": self.safety_check_interval,
                "position_accuracy": 0.01,
                "timing_tolerance": 0.1
            }
        }

        # Add channel specifications
        for channel_id, channel in self.channels.items():
            doc["control_channels"][channel.name] = {
                "channel_id": channel_id,
                "mechanical_system": channel.mechanical_system,
                "safety_limits": channel.safety_limits,
                "dependencies": list(channel.dependencies),
                "dependents": list(channel.dependents)
            }

        # Add event specifications
        for event in self.control_events:
            event_doc = {
                "event_id": event.event_id,
                "trigger_time": event.trigger_time,
                "trigger_condition": event.trigger_condition,
                "trigger_value": event.trigger_value,
                "target_channels": event.target_channels,
                "target_states": [state.value for state in event.target_states],
                "target_positions": event.target_positions,
                "duration": event.duration,
                "priority": event.priority,
                "safety_interlocks": event.safety_interlocks
            }
            doc["programming_events"].append(event_doc)

        # Save documentation (convert enum values to strings for JSON)
        def serialize_enum(obj):
            if isinstance(obj, MechanicalState):
                return obj.value
            raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")

        doc_path = output_path / "programming_documentation.json"
        with open(doc_path, 'w') as f:
            json.dump(doc, f, indent=2, default=serialize_enum)

        print(f"✓ Programming documentation exported to: {output_path}")

def main():
    """Main function for demonstrating mechanical programming logic"""
    print("=" * 80)
    print("MECHANICAL PROGRAMMING LOGIC - LEONARDO'S MECHANICAL LION")
    print("=" * 80)
    print("First Programmable Automation Controller in History")
    print("Complete Sequential Control System - 1517")
    print()

    # Initialize controller
    controller = MechanicalProgrammingController()

    print("Initialized mechanical programming controller:")
    print(f"  Control channels: {controller.num_channels}")
    print(f"  Programming events: {len(controller.control_events)}")
    print(f"  Performance duration: {controller.total_performance_time} seconds")
    print()

    # Run complete performance simulation
    simulation_results = controller.simulate_complete_performance()

    # Display results
    analysis = simulation_results["analysis"]
    print("\n" + "=" * 60)
    print("SIMULATION RESULTS:")
    print("=" * 60)
    print(f"Events completed: {analysis['events_completed']}/{analysis['total_events_planned']}")
    print(f"Success rate: {analysis['success_rate']:.2%}")
    print(f"Total errors: {analysis['total_errors']}")
    print(f"Safety performance: {analysis['safety_performance']['safe_time_percentage']:.2%} safe operation")
    print()

    print("CHANNEL UTILIZATION:")
    for channel, utilization in analysis['channel_utilization'].items():
        print(f"  {channel}: {utilization:.2%}")

    # Create visualization
    viz_path = "artifacts/mechanical_programming_visualization.png"
    controller.create_programming_visualization(simulation_results["simulation_data"], viz_path)
    print(f"\n✓ Programming visualization created: {viz_path}")

    # Export documentation
    controller.export_programming_documentation("artifacts/mechanical_programming")

    print("\n" + "=" * 80)
    print("MECHANICAL PROGRAMMING LOGIC COMPLETE")
    print("=" * 80)
    print("This system represents the first programmable automation controller,")
    print("using cam-based mechanical programming to coordinate multiple")
    print("systems in a complex theatrical performance sequence.")
    print()
    print("Leonardo's mechanical programming logic preceded electronic")
    print("computers by over 400 years, establishing the foundation of")
    print("modern automation and robotics technology.")

if __name__ == "__main__":
    main()
