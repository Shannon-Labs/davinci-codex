"""
Leonardo's Mechanical Lion - Complete Control System Demonstration
Integration of all control systems for theatrical performance

Historical Context:
- 1517 Royal court performance for King Francis I
- First programmable automation controller
- Fusion of Renaissance engineering and theatrical art
- Birth of mechanical computing and robotics

Engineering Achievement:
- 8-channel coordinated control system
- 5 precision cam profiles
- 26.5-second theatrical performance
- Complete mechanical programming implementation
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Add the control modules to path
sys.path.append(str(Path(__file__).parent))

from cam_profile_generator import CamProfileGenerator
from lion_control_system import MechanicalLionController
from mechanical_programming_logic import MechanicalProgrammingController
from performance_choreography import PerformanceChoreographer
from timing_sequence_optimizer import TimingSequenceOptimizer


class LionControlSystemDemo:
    """
    Complete demonstration of Leonardo's Mechanical Lion control system

    This class integrates all control components to demonstrate the
    first programmable automation controller in history.
    """

    def __init__(self):
        print("=" * 80)
        print("LEONARDO'S MECHANICAL LION - COMPLETE CONTROL SYSTEM")
        print("=" * 80)
        print("First Programmable Automation Controller in History")
        print("Royal Court Performance for King Francis I - 1517")
        print()

        # Initialize all control system components
        print("Initializing control system components...")

        # Core control system
        self.lion_controller = MechanicalLionController()
        print("✓ Mechanical Lion Controller initialized")

        # Cam profile generator
        self.cam_generator = CamProfileGenerator()
        print("✓ Cam Profile Generator initialized")

        # Timing optimizer
        self.timing_optimizer = TimingSequenceOptimizer()
        print("✓ Timing Sequence Optimizer initialized")

        # Programming logic controller
        self.programming_controller = MechanicalProgrammingController()
        print("✓ Mechanical Programming Controller initialized")

        # Performance choreographer
        self.choreographer = PerformanceChoreographer()
        print("✓ Performance Choreographer initialized")

        print(f"\nAll systems initialized for {self.lion_controller.total_performance_time} second performance")
        print()

    def demonstrate_cam_profiles(self):
        """Demonstrate cam profile generation and analysis"""
        print("=" * 60)
        print("CAM PROFILE GENERATION DEMONSTRATION")
        print("=" * 60)

        # Generate all cam specifications
        cams = {
            'walking_gait': self.cam_generator.generate_walking_gait_cam(),
            'tail_motion': self.cam_generator.generate_tail_motion_cam(),
            'chest_opening': self.cam_generator.generate_chest_opening_cam(),
            'lily_platform': self.cam_generator.generate_lily_platform_cam(),
            'master_timing': self.cam_generator.generate_master_timing_cam()
        }

        print(f"Generated {len(cams)} precision cam profiles:")
        print()

        for cam_name, cam_spec in cams.items():
            analysis = self.cam_generator.analyze_cam_profile(cam_spec)
            print(f"  {cam_name.replace('_', ' ').title()}:")
            print(f"    Function: {cam_spec.function}")
            print(f"    Material: {cam_spec.material}")
            print(f"    Max Lift: {cam_spec.max_lift*1000:.1f} mm")
            print(f"    Smoothness: {analysis.smoothness_rating:.2f}")
            print(f"    Complexity: {analysis.manufacturing_complexity:.2f}")
            print()

        # Create cam profile visualizations
        print("Creating cam profile manufacturing drawings...")
        output_dir = "artifacts/cam_demonstration"
        for cam_name, cam_spec in cams.items():
            viz_path = f"{output_dir}/{cam_name}_demo.png"
            self.cam_generator.create_cam_profile_visualization(cam_spec, viz_path)

        print("✓ Cam profile demonstrations created")
        print()

    def demonstrate_timing_optimization(self):
        """Demonstrate timing sequence optimization"""
        print("=" * 60)
        print("TIMING OPTIMIZATION DEMONSTRATION")
        print("=" * 60)

        # Create optimal timing sequence
        timing = self.timing_optimizer.create_optimal_timing_sequence()

        print("Created optimal timing sequence:")
        print(f"  Total duration: {timing.total_duration} seconds")
        print(f"  Performance events: {len(timing.events)}")
        print(f"  Critical timing points: {len(timing.critical_timing_points)}")
        print(f"  Audience focus moments: {len(timing.audience_focus_points)}")
        print()

        # Analyze timing effectiveness
        analysis = self.timing_optimizer.analyze_timing_effectiveness(timing)

        print("Timing Analysis Results:")
        print(f"  Dramatic Impact Score: {analysis.dramatic_impact_score:.2f}")
        print(f"  Mechanical Feasibility: {analysis.mechanical_feasibility_score:.2f}")
        print(f"  Audience Engagement: {analysis.audience_engagement_score:.2f}")
        print(f"  Coordination Complexity: {analysis.coordination_complexity:.2f}")
        print()

        # Calculate audience attention model
        attention_model = self.timing_optimizer.calculate_audience_attention_model(timing)

        print("Audience Attention Analysis:")
        print(f"  Average Attention: {attention_model['average_attention']:.2f}")
        print(f"  Attention Variance: {attention_model['attention_variance']:.2f}")
        print(f"  Peak Attention Periods: {len(attention_model['peak_attention_times'])}")
        print()

        # Create timing visualization
        viz_path = "artifacts/timing_optimization_demo.png"
        self.timing_optimizer.create_timing_visualization(timing, viz_path)
        print("✓ Timing optimization visualization created")
        print()

    def demonstrate_mechanical_programming(self):
        """Demonstrate mechanical programming logic"""
        print("=" * 60)
        print("MECHANICAL PROGRAMMING LOGIC DEMONSTRATION")
        print("=" * 60)

        print("Mechanical Programming Controller:")
        print(f"  Control channels: {self.programming_controller.num_channels}")
        print(f"  Programming events: {len(self.programming_controller.control_events)}")
        print(f"  Performance duration: {self.programming_controller.total_performance_time} seconds")
        print()

        # Display control channels
        print("Control Channels:")
        for channel_id, channel in self.programming_controller.channels.items():
            print(f"  Channel {channel_id}: {channel.name}")
            print(f"    System: {channel.mechanical_system}")
            print(f"    Dependencies: {list(channel.dependencies)}")
        print()

        # Display programming events summary
        print("Programming Events Summary:")
        event_types = {}
        for event in self.programming_controller.control_events:
            event_type = event.dramatic_function.value if hasattr(event, 'dramatic_function') else event.trigger_condition
            event_types[event_type] = event_types.get(event_type, 0) + 1

        for event_type, count in event_types.items():
            print(f"  {event_type}: {count} events")
        print()

        # Run simulation
        print("Running complete performance simulation...")
        simulation_results = self.programming_controller.simulate_complete_performance(time_step=0.1)

        analysis = simulation_results["analysis"]
        print("Simulation Results:")
        print(f"  Events completed: {analysis['events_completed']}/{analysis['total_events_planned']}")
        print(f"  Success rate: {analysis['success_rate']:.2%}")
        print(f"  Total errors: {analysis['total_errors']}")
        print(f"  Safety performance: {analysis['safety_performance']['safe_time_percentage']:.2%}")
        print()

        # Create programming visualization
        viz_path = "artifacts/programming_demo.png"
        self.programming_controller.create_programming_visualization(
            simulation_results["simulation_data"], viz_path)
        print("✓ Mechanical programming visualization created")
        print()

    def demonstrate_performance_choreography(self):
        """Demonstrate performance choreography"""
        print("=" * 60)
        print("PERFORMANCE CHOREOGRAPHY DEMONSTRATION")
        print("=" * 60)

        print("Performance Choreographer:")
        print(f"  Theatrical moments: {len(self.choreographer.theatrical_moments)}")
        print(f"  Transitions: {len(self.choreographer.transitions)}")
        print(f"  Total duration: {self.choreographer.total_duration} seconds")
        print()

        # Display theatrical moments
        print("Theatrical Moments:")
        for i, moment in enumerate(self.choreographer.theatrical_moments):
            print(f"  {i+1}. {moment.name}")
            print(f"     Time: {moment.start_time:.1f}-{moment.start_time+moment.duration:.1f}s")
            print(f"     Element: {moment.theatrical_element.value}")
            print(f"     Function: {moment.dramatic_function.value}")
            print(f"     Focus: {moment.audience_focus:.2f} | Impact: {moment.emotional_impact:.2f}")
        print()

        # Calculate dramatic arc
        dramatic_arc = self.choreographer.calculate_dramatic_arc()
        climax_time = dramatic_arc["time_points"][np.argmax(dramatic_arc["overall_drama"])]
        peak_drama = np.max(dramatic_arc["overall_drama"])

        print("Dramatic Analysis:")
        print(f"  Climax time: {climax_time:.1f} seconds")
        print(f"  Peak dramatic intensity: {peak_drama:.2f}")
        print(f"  Average intensity: {np.mean(dramatic_arc['overall_drama']):.2f}")
        print()

        # Analyze audience engagement
        engagement = self.choreographer.analyze_audience_engagement()
        print("Audience Engagement:")
        print(f"  Average engagement: {engagement['average_engagement']:.2%}")
        print(f"  Emotional satisfaction: {engagement['emotional_satisfaction']:.2%}")
        print()

        # Calculate political effectiveness
        political = self.choreographer.calculate_political_effectiveness()
        print("Political Effectiveness:")
        print(f"  Overall impact: {political['overall_political_effectiveness']:.2%}")
        print(f"  Symbolic effectiveness: {political['symbolic_effectiveness']:.2%}")
        print(f"  Alliance celebration: {political['alliance_celebration_effectiveness']:.2%}")
        print()

        # Create choreography visualization
        viz_path = "artifacts/choreography_demo.png"
        self.choreographer.create_choreography_visualization(viz_path)
        print("✓ Performance choreography visualization created")
        print()

    def demonstrate_complete_integration(self):
        """Demonstrate complete system integration"""
        print("=" * 60)
        print("COMPLETE SYSTEM INTEGRATION DEMONSTRATION")
        print("=" * 60)

        print("Integrating all control systems...")

        # Create master performance simulation
        master_simulation = {
            "cam_profiles": 5,
            "control_channels": 8,
            "timing_events": len(self.timing_optimizer.create_optimal_timing_sequence().events),
            "programming_logic": len(self.programming_controller.control_events),
            "theatrical_moments": len(self.choreographer.theatrical_moments),
            "total_duration": self.lion_controller.total_performance_time
        }

        print("Complete System Specifications:")
        for key, value in master_simulation.items():
            print(f"  {key.replace('_', ' ').title()}: {value}")
        print()

        # Run integrated performance simulation
        print("Running integrated performance simulation...")

        # Simulate the complete performance
        np.linspace(0, self.lion_controller.total_performance_time, 100)

        # Generate integrated control signals
        integrated_control = self.lion_controller.simulate_complete_performance(0.1)

        print("Integration Results:")
        print(f"  Control channels active: {len([ch for ch in integrated_control if ch != 'time' and ch != 'phase'])}")
        print(f"  Performance phases: {len(set(integrated_control['phase']))}")
        print(f"  Data points generated: {len(integrated_control['time'])}")
        print()

        # Create integrated visualization
        self.create_integration_visualization(integrated_control)
        print("✓ Complete integration visualization created")
        print()

    def create_integration_visualization(self, control_data):
        """Create visualization showing complete system integration"""
        fig, axes = plt.subplots(3, 1, figsize=(16, 12))

        # 1. Channel positions
        ax1 = axes[0]
        for channel_name, positions in control_data.items():
            if channel_name not in ['time', 'phase']:
                ax1.plot(control_data['time'], positions,
                        label=channel_name.replace('_', ' ').title(),
                        linewidth=2)

        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Channel Position (0-1)')
        ax1.set_title('Complete Control System Integration - Channel Positions')
        ax1.legend(loc='upper right', ncol=2)
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, self.lion_controller.total_performance_time)

        # 2. Performance phases
        ax2 = axes[1]
        phase_colors = {}
        unique_phases = list(set(control_data['phase']))
        colors = plt.cm.Set3(np.linspace(0, 1, len(unique_phases)))

        for i, phase in enumerate(unique_phases):
            phase_colors[phase] = colors[i]

        for i, phase in enumerate(control_data['phase']):
            if i > 0:
                ax2.plot([control_data['time'][i-1], control_data['time'][i]],
                        [0, 1], color=phase_colors[phase], linewidth=3, alpha=0.7)

        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Performance Phase')
        ax2.set_title('Performance Phase Transitions')
        ax2.set_ylim(0, 1.2)
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, self.lion_controller.total_performance_time)

        # Add phase legend
        legend_elements = [plt.Line2D([0], [0], color=phase_colors[phase], lw=3, label=phase.replace('_', ' ').title())
                          for phase in unique_phases]
        ax2.legend(handles=legend_elements, loc='upper right')

        # 3. System activity
        ax3 = axes[2]
        system_activity = []
        for i in range(len(control_data['time'])):
            # Count active channels
            active_count = 0
            for channel_name, positions in control_data.items():
                if channel_name not in ['time', 'phase'] and positions[i] > 0.01:
                    active_count += 1
            system_activity.append(active_count)

        ax3.plot(control_data['time'], system_activity, 'purple', linewidth=2)
        ax3.fill_between(control_data['time'], 0, system_activity, alpha=0.3, color='purple')
        ax3.set_xlabel('Time (seconds)')
        ax3.set_ylabel('Active Channels')
        ax3.set_title('System Activity Throughout Performance')
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0, self.lion_controller.total_performance_time)

        plt.tight_layout()
        plt.savefig('artifacts/complete_integration_demo.png', dpi=300, bbox_inches='tight')
        plt.close()

    def run_complete_demonstration(self):
        """Run complete demonstration of all systems"""
        print("Starting complete control system demonstration...")
        print()

        # Create output directory
        Path("artifacts").mkdir(exist_ok=True)

        # Run all demonstrations
        self.demonstrate_cam_profiles()
        self.demonstrate_timing_optimization()
        self.demonstrate_mechanical_programming()
        self.demonstrate_performance_choreography()
        self.demonstrate_complete_integration()

        # Export all documentation
        print("=" * 60)
        print("EXPORTING DOCUMENTATION")
        print("=" * 60)

        # Export all system documentation
        self.cam_generator.export_cam_design_package("artifacts/cam_designs_demo")
        self.timing_optimizer.export_timing_specifications(
            self.timing_optimizer.create_optimal_timing_sequence(),
            self.timing_optimizer.analyze_timing_effectiveness(
                self.timing_optimizer.create_optimal_timing_sequence()),
            "artifacts/timing_specs_demo")
        self.programming_controller.export_programming_documentation("artifacts/programming_demo")
        self.choreographer.export_choreography_documentation("artifacts/choreography_demo")

        print("✓ All documentation exported")
        print()

        # Final summary
        print("=" * 80)
        print("LEONARDO'S MECHANICAL LION - DEMONSTRATION COMPLETE")
        print("=" * 80)
        print()
        print("HISTORICAL ACHIEVEMENTS DEMONSTRATED:")
        print("  ✓ First programmable automation controller")
        print("  ✓ Cam-based mechanical computer system")
        print("  ✓ Multi-system theatrical coordination")
        print("  ✓ Biomechanical motion replication")
        print("  ✓ Political and artistic expression through technology")
        print()
        print("TECHNICAL INNOVATIONS:")
        print("  ✓ 8-channel synchronized control system")
        print("  ✓ 5 precision mathematical cam profiles")
        print("  ✓ 26.5-second theatrical performance sequence")
        print("  ✓ Complete safety and emergency systems")
        print("  ✓ Renaissance manufacturing compatibility")
        print()
        print("ARTISTIC ACCOMPLISHMENTS:")
        print("  ✓ Theatrical timing optimization")
        print("  ✓ Audience engagement maximization")
        print("  ✓ Political effectiveness enhancement")
        print("  ✓ Symbolic meaning integration")
        print("  ✓ Royal court entertainment perfection")
        print()
        print("This control system represents Leonardo da Vinci's genius in")
        print("combining mathematical precision with artistic expression,")
        print("creating the world's first programmable automation that would")
        print("not be surpassed for over 400 years.")
        print()
        print("The Mechanical Lion stands as a testament to Renaissance")
        print("innovation and the birth of mechanical computing.")

def main():
    """Main demonstration function"""
    demo = LionControlSystemDemo()
    demo.run_complete_demonstration()

if __name__ == "__main__":
    main()
