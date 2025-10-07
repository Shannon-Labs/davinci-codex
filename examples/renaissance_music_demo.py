#!/usr/bin/env python3
"""Demonstration of Renaissance music adaptation for Leonardo's mechanical ensemble."""

import sys
from pathlib import Path

# Add the src directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from davinci_codex.renaissance_music import MechanicalEnsembleIntegrator
from davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    MusicalScore,
    Note,
    RenaissanceMode,
    Voice,
)


def create_pavane_score() -> MusicalScore:
    """Create a simple Pavane (Renaissance dance) score."""
    score = MusicalScore(
        title="Simple Pavane",
        composer="Demo Composer",
        mode=RenaissanceMode.LYDIAN,
        form=MusicalForm.PAVANE,
        tempo_bpm=90.0
    )

    # Create a melody voice
    melody = Voice(name="Melody", instrument=InstrumentType.PROGRAMMABLE_FLUTE)

    # Simple melody in Lydian mode (E-based)
    melody_notes = [
        Note(pitch=329.63, duration=2.0, velocity=0.7, start_time=0.0),   # E4
        Note(pitch=392.00, duration=1.0, velocity=0.7, start_time=2.0),   # G4
        Note(pitch=440.00, duration=1.0, velocity=0.7, start_time=3.0),   # A4
        Note(pitch=493.88, duration=2.0, velocity=0.7, start_time=4.0),   # B4
        Note(pitch=392.00, duration=2.0, velocity=0.7, start_time=6.0),   # G4
        Note(pitch=329.63, duration=2.0, velocity=0.7, start_time=8.0),   # E4
    ]

    for note in melody_notes:
        melody.add_note(note)

    # Create a bass voice
    bass = Voice(name="Bass", instrument=InstrumentType.MECHANICAL_DRUM)

    # Simple bass line
    bass_notes = [
        Note(pitch=164.81, duration=2.0, velocity=0.8, start_time=0.0),   # E3
        Note(pitch=164.81, duration=2.0, velocity=0.8, start_time=2.0),   # E3
        Note(pitch=196.00, duration=2.0, velocity=0.8, start_time=4.0),   # G3
        Note(pitch=196.00, duration=2.0, velocity=0.8, start_time=6.0),   # G3
        Note(pitch=164.81, duration=2.0, velocity=0.8, start_time=8.0),   # E3
    ]

    for note in bass_notes:
        bass.add_note(note)

    # Add voices to the score
    score.add_voice(melody)
    score.add_voice(bass)

    return score


def main() -> None:
    """Main demonstration function."""
    print("Leonardo's Mechanical Ensemble - Renaissance Music Adaptation")
    print("=" * 60)

    # Create a simple Renaissance score
    print("\n1. Creating a simple Pavane score...")
    score = create_pavane_score()
    print(f"   Title: {score.title}")
    print(f"   Mode: {score.mode.value if score.mode else 'unknown'}")
    print(f"   Form: {score.form.value if score.form else 'unknown'}")
    print(f"   Tempo: {score.tempo_bpm} BPM")
    print(f"   Voices: {score.get_voice_count()}")
    print(f"   Duration: {score.get_duration():.1f} seconds")

    # Assign instruments to voices
    instrument_assignments = {
        0: InstrumentType.PROGRAMMABLE_FLUTE,  # Melody
        1: InstrumentType.MECHANICAL_DRUM,     # Bass
    }

    print("\n2. Instrument assignments:")
    for voice_idx, instrument in instrument_assignments.items():
        voice_name = score.voices[voice_idx].name
        print(f"   {voice_name}: {instrument.value}")

    # Adapt the score for the mechanical ensemble
    print("\n3. Adapting score for mechanical ensemble...")
    integrator = MechanicalEnsembleIntegrator()
    adaptation_result = integrator.adapt_score_for_ensemble(score, instrument_assignments)

    print(f"   Adaptation successful: {adaptation_result.adaptation_success}")
    print("   Feasibility scores:")
    for instrument, score_value in adaptation_result.feasibility_scores.items():
        print(f"     {instrument.value}: {score_value:.2f}")

    if adaptation_result.constraint_violations:
        print("   Constraint violations:")
        for violation in adaptation_result.constraint_violations:
            print(f"     - {violation}")

    # Convert to ensemble format
    print("\n4. Converting to ensemble format...")
    ensemble_score = integrator.convert_to_ensemble_format(
        adaptation_result.adapted_score,
        instrument_assignments,
        tempo_bpm=score.tempo_bpm,
        measures=2
    )

    print("   Ensemble score created with the following instruments:")
    for instrument, events in ensemble_score.items():
        print(f"     {instrument}: {len(events)} events")

    # Validate with simulation
    print("\n5. Validating with simulation...")
    validation_result = integrator.validate_with_simulation(
        adaptation_result.adapted_score,
        instrument_assignments
    )

    print(f"   Simulation validation: {'PASSED' if validation_result['valid'] else 'FAILED'}")

    if validation_result['warnings']:
        print("   Warnings:")
        for warning in validation_result['warnings']:
            print(f"     - {warning}")

    if validation_result['errors']:
        print("   Errors:")
        for error in validation_result['errors']:
            print(f"     - {error}")

    # Generate demo
    print("\n6. Generating ensemble demo...")
    demo_result = integrator.generate_ensemble_demo(
        adaptation_result.adapted_score,
        instrument_assignments,
        tempo_bpm=score.tempo_bpm,
        measures=2,
        render_audio=False  # Set to True to generate audio
    )

    print(f"   Demo generated successfully: {demo_result['valid']}")
    print("   Artifacts:")
    for artifact in demo_result['artifacts']:
        print(f"     - {artifact}")

    print("\n" + "=" * 60)
    print("Renaissance Music Adaptation Demo Complete!")
    print("\nThe adapted score can now be used with Leonardo's mechanical ensemble.")


if __name__ == "__main__":
    main()
