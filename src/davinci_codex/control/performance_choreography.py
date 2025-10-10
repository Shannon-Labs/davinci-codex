"""
Performance Choreography System for Leonardo's Mechanical Lion
Theatrical coordination and artistic direction of mechanical automation

Historical Context:
- Leonardo's fusion of art and engineering for royal court performance
- 16th century theatrical innovation and mechanical showmanship
- First use of choreographed mechanical automation
- Political and artistic expression through technology

Engineering Innovation:
- Theatrical timing optimization for dramatic impact
- Multi-system artistic coordination
- Audience engagement analysis and maximization
- Mechanical ballet programming for royal court entertainment
"""

import json
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional

import matplotlib.pyplot as plt
import numpy as np


class TheatricalElement(Enum):
    """Types of theatrical elements in the performance"""
    ENTRANCE = "entrance"
    MOVEMENT = "movement"
    REVEAL = "reveal"
    DISPLAY = "display"
    CONCLUSION = "conclusion"
    PAUSE = "pause"

class DramaticFunction(Enum):
    """Dramatic functions of performance elements"""
    ESTABLISH_PRESENCE = "establish_presence"
    BUILD_TENSION = "build_tension"
    CREATE_ANTICIPATION = "create_anticipation"
    DELIVER_CLIMAX = "deliver_climax"
    PROVIDE_RESOLUTION = "provide_resolution"
    MAINTAIN_MYSTERY = "maintain_mystery"

@dataclass
class TheatricalMoment:
    """Individual theatrical moment in the performance"""
    name: str
    start_time: float
    duration: float
    theatrical_element: TheatricalElement
    dramatic_function: DramaticFunction
    mechanical_systems: List[str]
    audience_focus: float  # 0.0 to 1.0
    emotional_impact: float  # 0.0 to 1.0
    symbolic_meaning: str
    royal_significance: str

@dataclass
class ChoreographicTransition:
    """Transition between theatrical moments"""
    name: str
    from_moment: str
    to_moment: str
    transition_duration: float
    transition_type: str  # "smooth", "dramatic", "surprise", "gradual"
    mechanical_coordination: List[str]
    audience_preparation: str

@dataclass
class PerformanceAnalysis:
    """Analysis of performance effectiveness"""
    dramatic_arc_score: float
    audience_engagement_score: float
    technical_execution_score: float
    artistic_cohesion_score: float
    political_effectiveness_score: float
    improvement_suggestions: List[str]

class PerformanceChoreographer:
    """
    Performance choreographer for Leonardo's Mechanical Lion

    This class coordinates the artistic and theatrical elements of the
    mechanical lion performance, ensuring maximum dramatic impact while
    maintaining technical precision and artistic integrity.
    """

    def __init__(self):
        # Performance parameters
        self.total_duration = 26.5  # seconds
        self.royal_court_attention_span = 45.0  # seconds
        self.optimal_dramatic_arc_duration = 25.0  # seconds

        # Theatrical timing constants
        self.entrance_impact_duration = 3.0  # seconds
        self.tension_buildup_rate = 0.8  # dramatic units per second
        self.climax_duration = 2.0  # seconds
        self.resolution_duration = 4.0  # seconds

        # Audience psychology parameters
        self.initial_curiosity_level = 0.6
        self.maximum_suspense_capacity = 0.9
        self.emotional_release_threshold = 0.7
        self.attention_decay_rate = 0.02  # per second

        # Symbolic and political elements
        self.franco_florentine_alliance_symbols = [
            "fleur_de_lis", "lion_strength", "mechanical_mastery", "innovation"
        ]
        self.royal_power_symbols = ["majesty", "control", "wealth", "authority"]

        # Create complete theatrical choreography
        self.theatrical_moments = self._create_theatrical_moments()
        self.transitions = self._create_transitions()

    def _create_theatrical_moments(self) -> List[TheatricalMoment]:
        """
        Create the complete sequence of theatrical moments

        This function designs the artistic narrative of the performance,
        balancing mechanical capabilities with dramatic requirements.
        """
        moments = []

        # MOMENT 1: Majestic Entrance (0.0 - 2.0 seconds)
        moments.append(TheatricalMoment(
            name="majestic_entrance",
            start_time=0.0,
            duration=2.0,
            theatrical_element=TheatricalElement.ENTRANCE,
            dramatic_function=DramaticFunction.ESTABLISH_PRESENCE,
            mechanical_systems=["tail_actuator"],
            audience_focus=0.8,
            emotional_impact=0.7,
            symbolic_meaning="Mechanical perfection and natural grace",
            royal_significance="Leonardo's tribute to royal majesty"
        ))

        # MOMENT 2: Graceful Movement - Phase 1 (2.0 - 5.0 seconds)
        moments.append(TheatricalMoment(
            name="graceful_movement_1",
            start_time=2.0,
            duration=3.0,
            theatrical_element=TheatricalElement.MOVEMENT,
            dramatic_function=DramaticFunction.BUILD_TENSION,
            mechanical_systems=["leg_systems", "tail_actuator"],
            audience_focus=0.9,
            emotional_impact=0.8,
            symbolic_meaning="Harmony of nature and mechanism",
            royal_significance="Natural authority and controlled power"
        ))

        # MOMENT 3: Dramatic Walking - Phase 2 (5.0 - 8.0 seconds)
        moments.append(TheatricalMoment(
            name="dramatic_walking_2",
            start_time=5.0,
            duration=3.0,
            theatrical_element=TheatricalElement.MOVEMENT,
            dramatic_function=DramaticFunction.CREATE_ANTICIPATION,
            mechanical_systems=["leg_systems", "tail_actuator"],
            audience_focus=0.95,
            emotional_impact=0.85,
            symbolic_meaning="Mastery over natural movement",
            royal_significance="Control and dominion"
        ))

        # MOMENT 4: Final Steps and Position (8.0 - 10.0 seconds)
        moments.append(TheatricalMoment(
            name="final_positioning",
            start_time=8.0,
            duration=2.0,
            theatrical_element=TheatricalElement.MOVEMENT,
            dramatic_function=DramaticFunction.CREATE_ANTICIPATION,
            mechanical_systems=["leg_systems", "tail_actuator"],
            audience_focus=0.9,
            emotional_impact=0.8,
            symbolic_meaning="Precision and perfection",
            royal_significance="Order and discipline"
        ))

        # MOMENT 5: Suspenseful Pause (10.0 - 12.0 seconds)
        moments.append(TheatricalMoment(
            name="suspenseful_pause",
            start_time=10.0,
            duration=2.0,
            theatrical_element=TheatricalElement.PAUSE,
            dramatic_function=DramaticFunction.MAINTAIN_MYSTERY,
            mechanical_systems=["tail_actuator"],
            audience_focus=0.95,
            emotional_impact=0.9,
            symbolic_meaning="Anticipation of revelation",
            royal_significance="Building royal expectations"
        ))

        # MOMENT 6: Chest Revelation Beginning (12.0 - 14.5 seconds)
        moments.append(TheatricalMoment(
            name="chest_revelation_begin",
            start_time=12.0,
            duration=2.5,
            theatrical_element=TheatricalElement.REVEAL,
            dramatic_function=DramaticFunction.BUILD_TENSION,
            mechanical_systems=["chest_mechanism", "timing_controller"],
            audience_focus=1.0,
            emotional_impact=0.95,
            symbolic_meaning="Opening of mechanical heart",
            royal_significance="Revelation of hidden treasures"
        ))

        # MOMENT 7: Chest Opening Complete (14.5 - 15.5 seconds)
        moments.append(TheatricalMoment(
            name="chest_revelation_complete",
            start_time=14.5,
            duration=1.0,
            theatrical_element=TheatricalElement.REVEAL,
            dramatic_function=DramaticFunction.CREATE_ANTICIPATION,
            mechanical_systems=["chest_mechanism", "timing_controller"],
            audience_focus=1.0,
            emotional_impact=0.98,
            symbolic_meaning="Mechanical mystery revealed",
            royal_significance="Royal generosity and openness"
        ))

        # MOMENT 8: Lily Presentation (15.5 - 17.5 seconds)
        moments.append(TheatricalMoment(
            name="lily_presentation",
            start_time=15.5,
            duration=2.0,
            theatrical_element=TheatricalElement.REVEAL,
            dramatic_function=DramaticFunction.DELIVER_CLIMAX,
            mechanical_systems=["lily_platform", "timing_controller"],
            audience_focus=1.0,
            emotional_impact=1.0,
            symbolic_meaning="Fleur-de-lis - French royal symbol",
            royal_significance="Franco-Florentine alliance celebration"
        ))

        # MOMENT 9: Royal Display (17.5 - 22.5 seconds)
        moments.append(TheatricalMoment(
            name="royal_display",
            start_time=17.5,
            duration=5.0,
            theatrical_element=TheatricalElement.DISPLAY,
            dramatic_function=DramaticFunction.PROVIDE_RESOLUTION,
            mechanical_systems=["lily_platform", "chest_mechanism", "tail_actuator"],
            audience_focus=0.9,
            emotional_impact=0.9,
            symbolic_meaning="Royal symbols in full glory",
            royal_significance="King Francis I's honor and prestige"
        ))

        # MOMENT 10: Graceful Conclusion (22.5 - 26.5 seconds)
        moments.append(TheatricalMoment(
            name="graceful_conclusion",
            start_time=22.5,
            duration=4.0,
            theatrical_element=TheatricalElement.CONCLUSION,
            dramatic_function=DramaticFunction.PROVIDE_RESOLUTION,
            mechanical_systems=["all_mechanical_systems"],
            audience_focus=0.8,
            emotional_impact=0.8,
            symbolic_meaning="Perfect mechanical artistry",
            royal_significance="Leonardo's dedication to royal service"
        ))

        return moments

    def _create_transitions(self) -> List[ChoreographicTransition]:
        """Create smooth transitions between theatrical moments"""
        transitions = []

        for i in range(len(self.theatrical_moments) - 1):
            from_moment = self.theatrical_moments[i]
            to_moment = self.theatrical_moments[i + 1]

            # Determine transition type based on dramatic function
            if to_moment.dramatic_function == DramaticFunction.DELIVER_CLIMAX:
                transition_type = "dramatic"
            elif from_moment.dramatic_function == DramaticFunction.DELIVER_CLIMAX:
                transition_type = "gradual"
            elif to_moment.theatrical_element == TheatricalElement.REVEAL:
                transition_type = "surprise"
            else:
                transition_type = "smooth"

            transition = ChoreographicTransition(
                name=f"transition_{i+1}",
                from_moment=from_moment.name,
                to_moment=to_moment.name,
                transition_duration=0.5,  # seconds
                transition_type=transition_type,
                mechanical_coordination=list(set(from_moment.mechanical_systems + to_moment.mechanical_systems)),
                audience_preparation=self._get_audience_preparation(from_moment, to_moment)
            )

            transitions.append(transition)

        return transitions

    def _get_audience_preparation(self, from_moment: TheatricalMoment,
                                to_moment: TheatricalMoment) -> str:
        """Get audience preparation instructions for transitions"""
        if to_moment.dramatic_function == DramaticFunction.DELIVER_CLIMAX:
            return "Build maximum anticipation, focus attention on chest area"
        elif to_moment.theatrical_element == TheatricalElement.REVEAL:
            return "Prepare audience for surprise, create sense of wonder"
        elif to_moment.theatrical_element == TheatricalElement.PAUSE:
            return "Allow emotional processing, build tension"
        else:
            return "Maintain engagement, smooth emotional flow"

    def calculate_dramatic_arc(self) -> Dict[str, np.ndarray]:
        """
        Calculate the dramatic arc of the performance

        This function models the emotional journey of the audience
        throughout the performance to maximize theatrical impact.
        """
        time_points = np.linspace(0, self.total_duration, 1000)

        # Initialize dramatic elements
        tension = np.zeros_like(time_points)
        anticipation = np.zeros_like(time_points)
        emotional_release = np.zeros_like(time_points)
        overall_drama = np.zeros_like(time_points)

        # Calculate dramatic elements for each moment
        for moment in self.theatrical_moments:
            # Find time indices for this moment
            mask = ((time_points >= moment.start_time) &
                   (time_points < moment.start_time + moment.duration))

            if moment.dramatic_function == DramaticFunction.BUILD_TENSION:
                tension[mask] += moment.emotional_impact
            elif moment.dramatic_function == DramaticFunction.CREATE_ANTICIPATION:
                anticipation[mask] += moment.emotional_impact
            elif moment.dramatic_function == DramaticFunction.DELIVER_CLIMAX:
                emotional_release[mask] += moment.emotional_impact
            elif moment.dramatic_function == DramaticFunction.PROVIDE_RESOLUTION:
                # Gradual release of tension
                for i, t in enumerate(time_points[mask]):
                    progress = (t - moment.start_time) / moment.duration
                    emotional_release[mask][i] += moment.emotional_impact * (1 - progress * 0.5)

        # Calculate overall dramatic arc
        overall_drama = tension + anticipation + emotional_release

        # Add smooth transitions
        for i in range(1, len(overall_drama) - 1):
            overall_drama[i] = 0.3 * overall_drama[i-1] + 0.4 * overall_drama[i] + 0.3 * overall_drama[i+1]

        # Normalize to 0-1 range
        overall_drama = np.clip(overall_drama, 0, 1)

        return {
            "time_points": time_points,
            "tension": tension,
            "anticipation": anticipation,
            "emotional_release": emotional_release,
            "overall_drama": overall_drama
        }

    def analyze_audience_engagement(self) -> Dict[str, float]:
        """
        Analyze audience engagement patterns

        This function predicts how the audience will engage with
        different aspects of the performance.
        """
        total_focus_time = 0
        total_emotional_impact = 0
        peak_engagement_moments = 0

        for moment in self.theatrical_moments:
            total_focus_time += moment.audience_focus * moment.duration
            total_emotional_impact += moment.emotional_impact * moment.duration

            if moment.audience_focus > 0.9:
                peak_engagement_moments += 1

        average_engagement = total_focus_time / self.total_duration
        emotional_satisfaction = total_emotional_impact / self.total_duration
        peak_engagement_ratio = peak_engagement_moments / len(self.theatrical_moments)

        return {
            "average_engagement": average_engagement,
            "emotional_satisfaction": emotional_satisfaction,
            "peak_engagement_ratio": peak_engagement_ratio,
            "total_focus_time": total_focus_time,
            "peak_moments": peak_engagement_moments
        }

    def optimize_theatrical_timing(self) -> List[TheatricalMoment]:
        """
        Optimize theatrical timing for maximum impact

        This function adjusts the timing of theatrical moments to
        create the most effective dramatic arc.
        """
        optimized_moments = []

        # Calculate current dramatic arc
        self.calculate_dramatic_arc()

        # Target dramatic arc parameters
        target_climax_time = 16.5  # seconds (around lily presentation)

        for _i, moment in enumerate(self.theatrical_moments):
            optimized_moment = TheatricalMoment(
                name=moment.name,
                start_time=moment.start_time,
                duration=moment.duration,
                theatrical_element=moment.theatrical_element,
                dramatic_function=moment.dramatic_function,
                mechanical_systems=moment.mechanical_systems,
                audience_focus=moment.audience_focus,
                emotional_impact=moment.emotional_impact,
                symbolic_meaning=moment.symbolic_meaning,
                royal_significance=moment.royal_significance
            )

            # Optimize timing based on dramatic function
            if moment.dramatic_function == DramaticFunction.DELIVER_CLIMAX:
                # Ensure climax occurs at optimal time
                if abs(moment.start_time - target_climax_time) > 1.0:
                    optimized_moment.start_time = target_climax_time - 0.5

            elif moment.dramatic_function == DramaticFunction.BUILD_TENSION:
                # Extend tension-building moments
                if moment.duration < 2.0:
                    optimized_moment.duration = 2.5

            elif moment.dramatic_function == DramaticFunction.PROVIDE_RESOLUTION and moment.duration < 3.0:
                # Ensure adequate resolution time
                optimized_moment.duration = 4.0

            optimized_moments.append(optimized_moment)

        # Ensure no overlaps and proper sequence
        optimized_moments = self._fix_timing_conflicts(optimized_moments)

        return optimized_moments

    def _fix_timing_conflicts(self, moments: List[TheatricalMoment]) -> List[TheatricalMoment]:
        """Fix any timing conflicts between moments"""
        # Sort by start time
        moments.sort(key=lambda m: m.start_time)

        # Fix conflicts
        for i in range(len(moments) - 1):
            current_end = moments[i].start_time + moments[i].duration
            next_start = moments[i + 1].start_time

            if current_end > next_start:
                # Adjust next moment start time
                moments[i + 1].start_time = current_end + 0.1

        return moments

    def calculate_political_effectiveness(self) -> Dict[str, float]:
        """
        Calculate the political effectiveness of the performance

        This function evaluates how well the performance serves its
        political purpose of honoring King Francis I and celebrating
        the Franco-Florentine alliance.
        """
        # Symbolic effectiveness
        french_symbols_present = ["fleur_de_lis"] in [str(m.symbolic_meaning).lower() for m in self.theatrical_moments]
        royal_honors_count = sum(1 for m in self.theatrical_moments if "royal" in m.royal_significance.lower())
        alliance_celebration = any("alliance" in m.royal_significance.lower() for m in self.theatrical_moments)

        # Timing effectiveness
        climax_timing = 16.5  # Optimal time for political impact
        actual_climax_time = max([m.start_time for m in self.theatrical_moments
                                if m.dramatic_function == DramaticFunction.DELIVER_CLIMAX], default=0)
        timing_effectiveness = 1.0 - abs(actual_climax_time - climax_timing) / 10.0

        # Overall political impact
        symbolic_impact = 0.8 if french_symbols_present else 0.4
        royal_impact = min(royal_honors_count / 3.0, 1.0)
        alliance_impact = 0.9 if alliance_celebration else 0.5

        overall_political_effectiveness = (symbolic_impact + royal_impact + alliance_impact + timing_effectiveness) / 4.0

        return {
            "symbolic_effectiveness": symbolic_impact,
            "royal_honor_effectiveness": royal_impact,
            "alliance_celebration_effectiveness": alliance_impact,
            "timing_effectiveness": timing_effectiveness,
            "overall_political_effectiveness": overall_political_effectiveness,
            "french_symbols_present": french_symbols_present,
            "royal_honors_count": royal_honors_count
        }

    def create_choreography_visualization(self, save_path: Optional[str] = None) -> None:
        """Create comprehensive visualization of the performance choreography"""
        # Calculate dramatic arc
        dramatic_arc = self.calculate_dramatic_arc()

        # Analyze audience engagement
        engagement = self.analyze_audience_engagement()

        # Calculate political effectiveness
        political = self.calculate_political_effectiveness()

        # Create subplot layout
        fig, axes = plt.subplots(4, 1, figsize=(16, 14),
                                gridspec_kw={'height_ratios': [2, 1, 1, 1]})

        # 1. Theatrical moments timeline
        ax1 = axes[0]
        y_position = 0
        colors = plt.cm.plasma(np.linspace(0, 1, len(self.theatrical_moments)))

        for y_position, moment in enumerate(self.theatrical_moments):
            # Draw moment bar
            ax1.barh(y_position, moment.duration, left=moment.start_time,
                    height=0.8, color=colors[y_position], alpha=0.7,
                    label=f"{moment.name}\n{moment.dramatic_function.value}")

            # Add emotional impact indicator
            impact_x = moment.start_time + moment.duration / 2
            impact_y = y_position + 0.4
            ax1.scatter(impact_x, impact_y, s=200 * moment.emotional_impact,
                       c='red', marker='*', alpha=0.8, zorder=5)

            # Add audience focus indicator
            focus_x = moment.start_time + moment.duration * 0.8
            focus_y = y_position + 0.4
            ax1.scatter(focus_x, focus_y, s=150 * moment.audience_focus,
                       c='blue', marker='o', alpha=0.8, zorder=5)

        ax1.set_xlabel('Time (seconds)')
        ax1.set_ylabel('Theatrical Moments')
        ax1.set_title('Leonardo\'s Mechanical Lion - Performance Choreography',
                     fontsize=14, fontweight='bold')
        ax1.grid(True, alpha=0.3)
        ax1.set_xlim(0, self.total_duration)

        # Add legend
        red_star = plt.Line2D([0], [0], marker='*', color='w', markerfacecolor='r',
                            markersize=10, label='Emotional Impact')
        blue_circle = plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='b',
                               markersize=8, label='Audience Focus')
        ax1.legend(handles=[red_star, blue_circle], loc='upper right')

        # 2. Dramatic arc
        ax2 = axes[1]
        ax2.plot(dramatic_arc["time_points"], dramatic_arc["overall_drama"],
                'purple', linewidth=3, label='Overall Dramatic Arc')
        ax2.fill_between(dramatic_arc["time_points"], 0, dramatic_arc["overall_drama"],
                        alpha=0.3, color='purple')

        # Mark key dramatic points
        ax2.axvline(x=10.0, color='red', linestyle='--', alpha=0.5, label='Suspense Peak')
        ax2.axvline(x=16.5, color='gold', linestyle='--', alpha=0.5, label='Climax')
        ax2.axvline(x=22.5, color='green', linestyle='--', alpha=0.5, label='Resolution')

        ax2.set_xlabel('Time (seconds)')
        ax2.set_ylabel('Dramatic Intensity')
        ax2.set_title('Dramatic Arc Analysis')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.set_xlim(0, self.total_duration)
        ax2.set_ylim(0, 1.1)

        # 3. Audience engagement analysis
        ax3 = axes[2]

        # Create engagement visualization
        engagement_time = np.linspace(0, self.total_duration, 100)
        engagement_level = np.zeros_like(engagement_time)

        for moment in self.theatrical_moments:
            mask = ((engagement_time >= moment.start_time) &
                   (engagement_time < moment.start_time + moment.duration))
            engagement_level[mask] = moment.audience_focus

        ax3.plot(engagement_time, engagement_level, 'blue', linewidth=2, label='Audience Engagement')
        ax3.fill_between(engagement_time, 0, engagement_level, alpha=0.3, color='blue')

        # Add average engagement line
        ax3.axhline(y=engagement["average_engagement"], color='red', linestyle='--',
                   alpha=0.7, label=f'Average: {engagement["average_engagement"]:.2f}')

        ax3.set_xlabel('Time (seconds)')
        ax3.set_ylabel('Engagement Level')
        ax3.set_title(f'Audience Engagement Analysis\nSatisfaction: {engagement["emotional_satisfaction"]:.2f}')
        ax3.legend()
        ax3.grid(True, alpha=0.3)
        ax3.set_xlim(0, self.total_duration)
        ax3.set_ylim(0, 1.1)

        # 4. Political effectiveness metrics
        ax4 = axes[4] if len(axes) > 4 else axes[3]

        metrics = ['Symbolic\nEffectiveness', 'Royal\nHonor', 'Alliance\nCelebration',
                  'Timing\nEffectiveness', 'Overall\nPolitical\nImpact']
        values = [
            political["symbolic_effectiveness"],
            political["royal_honor_effectiveness"],
            political["alliance_celebration_effectiveness"],
            political["timing_effectiveness"],
            political["overall_political_effectiveness"]
        ]

        colors_metrics = ['gold' if v > 0.7 else 'orange' if v > 0.5 else 'red' for v in values]

        bars = ax4.bar(metrics, values, color=colors_metrics, alpha=0.7)
        ax4.set_ylabel('Effectiveness Score')
        ax4.set_title('Political Effectiveness Analysis')
        ax4.set_ylim(0, 1.1)
        ax4.grid(True, alpha=0.3, axis='y')

        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax4.text(bar.get_x() + bar.get_width()/2., height + 0.02,
                    f'{value:.2f}', ha='center', va='bottom')

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()

        plt.close()

    def generate_performance_score(self) -> Dict:
        """Generate comprehensive performance score document"""
        return {
            "title": "Leonardo's Mechanical Lion - Performance Score",
            "date": "1517",
            "composer": "Leonardo da Vinci",
            "conductor": "Master Mechanic",
            "duration": self.total_duration,
            "genre": "Mechanical Theater",
            "occasion": "Royal Court Performance for King Francis I",

            "theatrical_structure": {
                "acts": len(self.theatrical_moments),
                "scenes": len(self.transitions),
                "climax_time": 16.5,
                "resolution_time": 22.5
            },

            "mechanical_cast": {
                "protagonist": "Mechanical Lion",
                "supporting_mechanisms": [
                    "Four-legged walking system",
                    "Articulated tail mechanism",
                    "Chest reveal mechanism",
                    "Lily presentation platform",
                    "Master timing controller"
                ]
            },

            "symbolic_elements": {
                "primary_symbols": self.franco_florentine_alliance_symbols,
                "royal_symbols": self.royal_power_symbols,
                "artistic_themes": [
                    "Harmony of nature and machine",
                    "Renaissance innovation",
                    "Royal patronage",
                    "Franco-Italian alliance"
                ]
            },

            "performance_notes": self._generate_performance_notes(),

            "technical_requirements": {
                "mechanical_precision": "±0.1mm",
                "timing_accuracy": "±0.1s",
                "power_requirements": "Hand-wound springs",
                "operational_reliability": ">95%"
            }
        }

    def _generate_performance_notes(self) -> List[str]:
        """Generate detailed performance notes"""
        notes = [
            "The performance must create a sense of wonder and awe",
            "Mechanical movements should appear natural and lifelike",
            "Timing of the chest reveal is critical for dramatic impact",
            "The fleurs-de-lis presentation must be perfectly synchronized",
            "Maintain eye contact with King Francis I during royal display",
            "Ensure smooth transitions between all mechanical movements",
            "The conclusion should demonstrate complete control mastery",
            "Performance must be flawless - royal reputation depends on it"
        ]

        # Add moment-specific notes
        for moment in self.theatrical_moments:
            if moment.dramatic_function == DramaticFunction.DELIVER_CLIMAX:
                notes.append(f"CRITICAL: {moment.name} must deliver maximum emotional impact")
            elif moment.theatrical_element == TheatricalElement.REVEAL:
                notes.append(f"IMPORTANT: {moment.name} requires perfect mechanical coordination")

        return notes

    def export_choreography_documentation(self, output_dir: str) -> None:
        """Export complete choreography documentation"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Generate performance score
        score = self.generate_performance_score()

        # Calculate analysis metrics
        dramatic_arc = self.calculate_dramatic_arc()
        engagement = self.analyze_audience_engagement()
        political = self.calculate_political_effectiveness()

        # Create comprehensive documentation
        documentation = {
            "performance_score": score,
            "theatrical_moments": [
                {
                    "name": moment.name,
                    "start_time": moment.start_time,
                    "duration": moment.duration,
                    "theatrical_element": moment.theatrical_element.value,
                    "dramatic_function": moment.dramatic_function.value,
                    "mechanical_systems": moment.mechanical_systems,
                    "audience_focus": moment.audience_focus,
                    "emotional_impact": moment.emotional_impact,
                    "symbolic_meaning": moment.symbolic_meaning,
                    "royal_significance": moment.royal_significance
                }
                for moment in self.theatrical_moments
            ],
            "transitions": [
                {
                    "name": trans.name,
                    "from_moment": trans.from_moment,
                    "to_moment": trans.to_moment,
                    "transition_duration": trans.transition_duration,
                    "transition_type": trans.transition_type,
                    "mechanical_coordination": trans.mechanical_coordination,
                    "audience_preparation": trans.audience_preparation
                }
                for trans in self.transitions
            ],
            "analysis": {
                "audience_engagement": engagement,
                "political_effectiveness": political,
                "dramatic_arc_peak": float(np.max(dramatic_arc["overall_drama"])),
                "dramatic_arc_climax_time": float(dramatic_arc["time_points"][np.argmax(dramatic_arc["overall_drama"])]),
                "total_theatrical_moments": len(self.theatrical_moments),
                "average_moment_duration": np.mean([m.duration for m in self.theatrical_moments])
            }
        }

        # Save documentation
        doc_path = output_path / "choreography_documentation.json"
        with open(doc_path, 'w') as f:
            json.dump(documentation, f, indent=2)

        # Save performance score as readable text
        score_path = output_path / "performance_score.txt"
        with open(score_path, 'w') as f:
            f.write(f"{'='*80}\n")
            f.write(f"{score['title']}\n")
            f.write(f"{'='*80}\n")
            f.write(f"Date: {score['date']}\n")
            f.write(f"Composer: {score['composer']}\n")
            f.write(f"Duration: {score['duration']} seconds\n")
            f.write(f"Occasion: {score['occasion']}\n\n")

            f.write("THEATRICAL STRUCTURE:\n")
            f.write(f"  Acts: {score['theatrical_structure']['acts']}\n")
            f.write(f"  Scenes: {score['theatrical_structure']['scenes']}\n")
            f.write(f"  Climax: {score['theatrical_structure']['climax_time']} seconds\n")
            f.write(f"  Resolution: {score['theatrical_structure']['resolution_time']} seconds\n\n")

            f.write("MECHANICAL CAST:\n")
            for element in score["mechanical_cast"]["supporting_mechanisms"]:
                f.write(f"  • {element}\n")
            f.write("\n")

            f.write("PERFORMANCE NOTES:\n")
            for i, note in enumerate(score["performance_notes"], 1):
                f.write(f"  {i}. {note}\n")

        print(f"✓ Choreography documentation exported to: {output_path}")

def main():
    """Main function for demonstrating performance choreography"""
    print("=" * 80)
    print("PERFORMANCE CHOREOGRAPHY - LEONARDO'S MECHANICAL LION")
    print("=" * 80)
    print("Theatrical Coordination and Artistic Direction")
    print("First Use of Mechanical Choreography - 1517")
    print()

    # Initialize choreographer
    choreographer = PerformanceChoreographer()

    print("Initialized performance choreographer:")
    print(f"  Theatrical moments: {len(choreographer.theatrical_moments)}")
    print(f"  Transitions: {len(choreographer.transitions)}")
    print(f"  Total duration: {choreographer.total_duration} seconds")
    print()

    # Calculate dramatic arc
    dramatic_arc = choreographer.calculate_dramatic_arc()
    climax_time = dramatic_arc["time_points"][np.argmax(dramatic_arc["overall_drama"])]
    peak_drama = np.max(dramatic_arc["overall_drama"])

    print("DRAMATIC ANALYSIS:")
    print(f"  Climax time: {climax_time:.1f} seconds")
    print(f"  Peak dramatic intensity: {peak_drama:.2f}")
    print(f"  Average dramatic intensity: {np.mean(dramatic_arc['overall_drama']):.2f}")
    print()

    # Analyze audience engagement
    engagement = choreographer.analyze_audience_engagement()
    print("AUDIENCE ENGAGEMENT:")
    print(f"  Average engagement: {engagement['average_engagement']:.2%}")
    print(f"  Emotional satisfaction: {engagement['emotional_satisfaction']:.2%}")
    print(f"  Peak engagement moments: {engagement['peak_moments']}")
    print()

    # Calculate political effectiveness
    political = choreographer.calculate_political_effectiveness()
    print("POLITICAL EFFECTIVENESS:")
    print(f"  Overall political impact: {political['overall_political_effectiveness']:.2%}")
    print(f"  Symbolic effectiveness: {political['symbolic_effectiveness']:.2%}")
    print(f"  Royal honor effectiveness: {political['royal_honor_effectiveness']:.2%}")
    print(f"  Alliance celebration: {political['alliance_celebration_effectiveness']:.2%}")
    print()

    # Optimize timing
    optimized_moments = choreographer.optimize_theatrical_timing()
    print(f"Optimized {len(optimized_moments)} theatrical moments for maximum impact")

    # Create visualization
    viz_path = "artifacts/performance_choreography.png"
    choreographer.create_choreography_visualization(viz_path)
    print(f"✓ Choreography visualization created: {viz_path}")

    # Export documentation
    choreographer.export_choreography_documentation("artifacts/choreography")

    print("\n" + "=" * 80)
    print("PERFORMANCE CHOREOGRAPHY COMPLETE")
    print("=" * 80)
    print("The performance has been choreographed to create maximum theatrical")
    print("impact while honoring King Francis I and celebrating the")
    print("Franco-Florentine alliance through mechanical innovation.")
    print()
    print("This represents the first use of theatrical choreography in")
    print("mechanical automation, establishing the foundation of modern")
    print("performance art and robotic entertainment.")

if __name__ == "__main__":
    main()
