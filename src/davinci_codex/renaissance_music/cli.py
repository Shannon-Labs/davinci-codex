"""Command-line interface for Renaissance music composition."""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Dict, Optional

import typer

from ..artifacts import ensure_artifact_dir
from .composition import RenaissanceCompositionGenerator
from .integration import MechanicalEnsembleIntegrator
from .models import (
    InstrumentType,
    MusicalForm,
    RenaissanceMode,
)
from .pattern_composer import PatternBasedComposer

app = typer.Typer(help="Renaissance Music Composition CLI")


def get_instrument_mapping(instrument_str: str) -> Dict[int, InstrumentType]:
    """Parse instrument mapping string into a dictionary.

    Args:
        instrument_str: String in format "0:instrument1,1:instrument2,..."

    Returns:
        Dictionary mapping voice indices to instrument types
    """
    mapping = {}

    for part in instrument_str.split(","):
        try:
            voice_idx, instrument_name = part.strip().split(":")
            voice_idx = int(voice_idx)

            # Map string to InstrumentType
            instrument_map = {
                "drum": InstrumentType.MECHANICAL_DRUM,
                "organ": InstrumentType.MECHANICAL_ORGAN,
                "viola": InstrumentType.VIOLA_ORGANISTA,
                "flute": InstrumentType.PROGRAMMABLE_FLUTE,
                "carillon": InstrumentType.MECHANICAL_CARILLON,
                "trumpet": InstrumentType.MECHANICAL_TRUMPETER,
            }

            instrument = instrument_map.get(instrument_name.lower())
            if instrument:
                mapping[voice_idx] = instrument
            else:
                typer.echo(f"Unknown instrument: {instrument_name}")
                raise typer.Exit(1)

        except ValueError:
            typer.echo(f"Invalid instrument mapping: {part}")
            raise typer.Exit(1)

    return mapping


def get_mode(mode_str: str) -> RenaissanceMode:
    """Parse mode string into RenaissanceMode enum.

    Args:
        mode_str: String representation of the mode

    Returns:
        RenaissanceMode enum value
    """
    mode_map = {
        "dorian": RenaissanceMode.DORIAN,
        "phrygian": RenaissanceMode.PHRYGIAN,
        "lydian": RenaissanceMode.LYDIAN,
        "mixolydian": RenaissanceMode.MIXOLYDIAN,
        "hypodorian": RenaissanceMode.HYPODORIAN,
        "hypophrygian": RenaissanceMode.HYPOPHRYGIAN,
        "hypolydian": RenaissanceMode.HYPOLYDIAN,
        "hypomixolydian": RenaissanceMode.HYPOMIXOLYDIAN,
    }

    mode = mode_map.get(mode_str.lower())
    if not mode:
        typer.echo(f"Unknown mode: {mode_str}")
        typer.echo(f"Available modes: {', '.join(mode_map.keys())}")
        raise typer.Exit(1)

    return mode


def get_form(form_str: str) -> MusicalForm:
    """Parse form string into MusicalForm enum.

    Args:
        form_str: String representation of the form

    Returns:
        MusicalForm enum value
    """
    form_map = {
        "basse_danse": MusicalForm.BASSE_DANSE,
        "pavane": MusicalForm.PAVANE,
        "galliard": MusicalForm.GALLIARD,
        "chanson": MusicalForm.CHANSON,
        "madrigal": MusicalForm.MADRIGAL,
        "motet": MusicalForm.MOTET,
        "isorhythmic": MusicalForm.ISORHYTHMIC,
        "fantasia": MusicalForm.FANTASIA,
    }

    form = form_map.get(form_str.lower())
    if not form:
        typer.echo(f"Unknown form: {form_str}")
        typer.echo(f"Available forms: {', '.join(form_map.keys())}")
        raise typer.Exit(1)

    return form


@app.command()
def generate(
    form: str = typer.Option(..., help="Musical form (e.g., pavane, galliard, basse_danse)"),
    mode: str = typer.Option(..., help="Renaissance mode (e.g., dorian, phrygian, lydian)"),
    instruments: str = typer.Option(..., help="Instrument mapping (e.g., '0:flute,1:viola,2:organ')"),
    measures: int = typer.Option(32, help="Number of measures to generate"),
    output: Optional[str] = typer.Option(None, help="Output file path"),
    seed: Optional[int] = typer.Option(None, help="Random seed for reproducible generation"),
    method: str = typer.Option("hybrid", help="Composition method (hybrid, pattern, rule)"),
    adapt: bool = typer.Option(True, help="Adapt for mechanical instruments"),
    demo: bool = typer.Option(False, help="Generate demo with ensemble simulation"),
) -> None:
    """Generate a Renaissance-style composition."""
    # Parse inputs
    musical_form = get_form(form)
    musical_mode = get_mode(mode)
    instrument_mapping = get_instrument_mapping(instruments)

    typer.echo(f"Generating {form} in {mode} mode...")
    typer.echo(f"Instrument mapping: {instrument_mapping}")
    typer.echo(f"Number of measures: {measures}")
    typer.echo(f"Composition method: {method}")

    # Generate composition based on method
    if method == "pattern":
        composer = PatternBasedComposer()
        score = composer.compose_by_patterns(
            form=musical_form,
            mode=musical_mode,
            instrument_assignments=instrument_mapping,
            measures=measures,
            seed=seed
        )
    else:  # hybrid or rule
        generator = RenaissanceCompositionGenerator()
        score = generator.generate_composition(
            form=musical_form,
            mode=musical_mode,
            instrument_assignments=instrument_mapping,
            measures=measures,
            seed=seed
        )

    typer.echo(f"Generated composition: {score.title}")
    typer.echo(f"Tempo: {score.tempo_bpm} BPM")
    typer.echo(f"Number of voices: {len(score.voices)}")

    # Adapt for mechanical instruments if requested
    if adapt:
        typer.echo("Adapting for mechanical instruments...")
        integrator = MechanicalEnsembleIntegrator()
        adaptation_result = integrator.adapt_score_for_ensemble(
            score, instrument_mapping
        )

        if adaptation_result.adaptation_success:
            typer.echo("Successfully adapted for mechanical instruments")
            score = adaptation_result.adapted_score

            # Print adaptation log
            if adaptation_result.adaptation_log:
                typer.echo("Adaptation details:")
                for entry in adaptation_result.adaptation_log:
                    typer.echo(f"  - {entry}")
        else:
            typer.echo("Warning: Could not fully adapt for mechanical instruments")
            for violation in adaptation_result.constraint_violations:
                typer.echo(f"  - {violation}")

    # Generate demo if requested
    if demo:
        typer.echo("Generating ensemble demo...")
        integrator = MechanicalEnsembleIntegrator()
        demo_result = integrator.generate_ensemble_demo(
            score, instrument_mapping, render_audio=True
        )

        if demo_result["valid"]:
            typer.echo("Successfully generated ensemble demo")
            typer.echo("Demo artifacts:")
            for artifact in demo_result["artifacts"]:
                typer.echo(f"  - {artifact}")
        else:
            typer.echo("Warning: Demo generation had issues")
            for error in demo_result["errors"]:
                typer.echo(f"  - {error}")

    # Save output
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        if output_path.suffix.lower() == ".json":
            # Save as JSON
            save_as_json(score, output_path)
        elif output_path.suffix.lower() in [".mid", ".midi"]:
            # Save as MIDI
            save_as_midi(score, output_path)
        else:
            # Default to JSON
            output_path = output_path.with_suffix(".json")
            save_as_json(score, output_path)

        typer.echo(f"Saved composition to: {output_path}")
    else:
        # Save to default location
        artifacts_dir = ensure_artifact_dir("renaissance_music", subdir="compositions")
        output_path = artifacts_dir / f"{form}_{mode}_composition.json"
        save_as_json(score, output_path)
        typer.echo(f"Saved composition to: {output_path}")


@app.command()
def adapt(
    input_file: str = typer.Option(..., help="Input score file (JSON)"),
    instruments: str = typer.Option(..., help="Instrument mapping (e.g., '0:flute,1:viola,2:organ')"),
    output: Optional[str] = typer.Option(None, help="Output file path"),
    constraint_level: str = typer.Option("medium", help="Constraint level (low, medium, high)"),
) -> None:
    """Adapt an existing composition for mechanical instruments."""
    input_path = Path(input_file)

    if not input_path.exists():
        typer.echo(f"Input file not found: {input_path}")
        raise typer.Exit(1)

    # Load input score
    try:
        score = load_from_json(input_path)
    except Exception as e:
        typer.echo(f"Error loading input file: {e}")
        raise typer.Exit(1)

    # Parse instrument mapping
    instrument_mapping = get_instrument_mapping(instruments)

    typer.echo(f"Adapting {score.title} for mechanical instruments...")
    typer.echo(f"Instrument mapping: {instrument_mapping}")
    typer.echo(f"Constraint level: {constraint_level}")

    # Adapt for mechanical instruments
    integrator = MechanicalEnsembleIntegrator()
    adaptation_result = integrator.adapt_score_for_ensemble(
        score, instrument_mapping
    )

    if adaptation_result.adaptation_success:
        typer.echo("Successfully adapted for mechanical instruments")
        adapted_score = adaptation_result.adapted_score

        # Print adaptation log
        if adaptation_result.adaptation_log:
            typer.echo("Adaptation details:")
            for entry in adaptation_result.adaptation_log:
                typer.echo(f"  - {entry}")

        # Print feasibility scores
        if adaptation_result.feasibility_scores:
            typer.echo("Feasibility scores:")
            for instrument, score in adaptation_result.feasibility_scores.items():
                typer.echo(f"  - {instrument.value}: {score:.2f}")
    else:
        typer.echo("Warning: Could not fully adapt for mechanical instruments")
        for violation in adaptation_result.constraint_violations:
            typer.echo(f"  - {violation}")

        adapted_score = adaptation_result.adapted_score

    # Save output
    if output:
        output_path = Path(output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
    else:
        artifacts_dir = ensure_artifact_dir("renaissance_music", subdir="adaptations")
        output_path = artifacts_dir / f"{input_path.stem}_adapted.json"

    save_as_json(adapted_score, output_path)
    typer.echo(f"Saved adapted composition to: {output_path}")


@app.command()
def demo(
    form: str = typer.Option("pavane", help="Musical form (e.g., pavane, galliard, basse_danse)"),
    mode: str = typer.Option("lydian", help="Renaissance mode (e.g., dorian, phrygian, lydian)"),
    measures: int = typer.Option(16, help="Number of measures to generate"),
    render_audio: bool = typer.Option(True, help="Render audio output"),
    seed: Optional[int] = typer.Option(None, help="Random seed for reproducible generation"),
) -> None:
    """Generate a demonstration of the AI composition system."""
    # Parse inputs
    musical_form = get_form(form)
    musical_mode = get_mode(mode)

    # Define instrument mapping for demo
    instrument_mapping = {
        0: InstrumentType.PROGRAMMABLE_FLUTE,
        1: InstrumentType.VIOLA_ORGANISTA,
        2: InstrumentType.MECHANICAL_ORGAN,
        3: InstrumentType.MECHANICAL_CARILLON,
    }

    typer.echo(f"Generating demo {form} in {mode} mode...")

    # Generate composition
    generator = RenaissanceCompositionGenerator()
    score = generator.generate_composition(
        form=musical_form,
        mode=musical_mode,
        instrument_assignments=instrument_mapping,
        measures=measures,
        seed=seed
    )

    typer.echo(f"Generated composition: {score.title}")

    # Adapt for mechanical instruments
    integrator = MechanicalEnsembleIntegrator()
    adaptation_result = integrator.adapt_score_for_ensemble(
        score, instrument_mapping
    )

    if adaptation_result.adaptation_success:
        score = adaptation_result.adapted_score
        typer.echo("Successfully adapted for mechanical instruments")

    # Generate demo
    demo_result = integrator.generate_ensemble_demo(
        score, instrument_mapping, render_audio=render_audio
    )

    if demo_result["valid"]:
        typer.echo("Successfully generated ensemble demo")
        typer.echo("Demo artifacts:")
        for artifact in demo_result["artifacts"]:
            typer.echo(f"  - {artifact}")
    else:
        typer.echo("Warning: Demo generation had issues")
        for error in demo_result["errors"]:
            typer.echo(f"  - {error}")

    # Print composition analysis
    typer.echo("\nComposition Analysis:")
    typer.echo(f"  - Form: {score.form.value}")
    typer.echo(f"  - Mode: {score.mode.value}")
    typer.echo(f"  - Tempo: {score.tempo_bpm} BPM")
    typer.echo(f"  - Duration: {score.get_duration():.1f} seconds")
    typer.echo(f"  - Voices: {len(score.voices)}")

    for i, voice in enumerate(score.voices):
        typer.echo(f"    Voice {i+1}: {voice.name} ({voice.instrument.value if voice.instrument else 'unspecified'})")


@app.command()
def patterns(
    mode: Optional[str] = typer.Option(None, help="Filter by mode"),
    form: Optional[str] = typer.Option(None, help="Filter by form"),
    instrument: Optional[str] = typer.Option(None, help="Filter by instrument"),
) -> None:
    """List available patterns in the pattern library."""
    from .patterns import RenaissancePatternLibrary

    library = RenaissancePatternLibrary()

    # Parse filters
    mode_filter = get_mode(mode) if mode else None
    form_filter = get_form(form) if form else None
    instrument_filter = None

    if instrument:
        instrument_map = {
            "drum": InstrumentType.MECHANICAL_DRUM,
            "organ": InstrumentType.MECHANICAL_ORGAN,
            "viola": InstrumentType.VIOLA_ORGANISTA,
            "flute": InstrumentType.PROGRAMMABLE_FLUTE,
            "carillon": InstrumentType.MECHANICAL_CARILLON,
            "trumpet": InstrumentType.MECHANICAL_TRUMPETER,
        }
        instrument_filter = instrument_map.get(instrument.lower())

    # Query patterns
    if mode_filter:
        patterns = library.query_patterns_by_mode(mode_filter)
    elif form_filter:
        patterns = library.query_patterns_by_form(form_filter)
    elif instrument_filter:
        patterns = library.query_patterns_by_instrument(instrument_filter)
    else:
        patterns = library.get_all_patterns()

    typer.echo(f"Found {len(patterns)} patterns")

    # Group patterns by type
    pattern_groups = {}
    for pattern in patterns:
        pattern_type = pattern.pattern_type
        if pattern_type not in pattern_groups:
            pattern_groups[pattern_type] = []
        pattern_groups[pattern_type].append(pattern)

    # Print patterns
    for pattern_type, type_patterns in pattern_groups.items():
        typer.echo(f"\n{pattern_type.title()} Patterns:")
        for pattern in type_patterns:
            typer.echo(f"  - {pattern.name}")
            typer.echo(f"    Mode: {pattern.mode.value}")
            typer.echo(f"    Notes: {len(pattern.notes)}")
            if pattern.context_tags:
                typer.echo(f"    Tags: {', '.join(pattern.context_tags)}")


@app.command()
def dataset(
    action: str = typer.Option("stats", help="Action (stats, list, query)"),
    mode: Optional[str] = typer.Option(None, help="Filter by mode"),
    form: Optional[str] = typer.Option(None, help="Filter by form"),
    category: Optional[str] = typer.Option(None, help="Filter by category"),
) -> None:
    """Interact with the Renaissance music dataset."""
    from data.renaissance_music.dataset import DatasetCategory, RenaissanceMusicDataset

    dataset = RenaissanceMusicDataset()

    if action == "stats":
        # Print dataset statistics
        stats = dataset.get_statistics()

        typer.echo("Dataset Statistics:")
        typer.echo(f"  Total entries: {stats['total_entries']}")

        typer.echo("\nModes:")
        for mode, count in stats['modes'].items():
            typer.echo(f"  - {mode}: {count}")

        typer.echo("\nForms:")
        for form, count in stats['forms'].items():
            typer.echo(f"  - {form}: {count}")

        typer.echo("\nCategories:")
        for category, count in stats['categories'].items():
            typer.echo(f"  - {category}: {count}")

        typer.echo("\nDifficulty Levels:")
        for level, count in stats['difficulty_levels'].items():
            typer.echo(f"  - Level {level}: {count}")

    elif action == "list":
        # List entries
        entries = dataset.get_all_entries()

        # Apply filters
        if mode:
            mode_filter = get_mode(mode)
            entries = [e for e in entries if e.mode == mode_filter]

        if form:
            form_filter = get_form(form)
            entries = [e for e in entries if e.form == form_filter]

        if category:
            category_map = {
                "dance": DatasetCategory.DANCE,
                "vocal": DatasetCategory.VOCAL,
                "sacred": DatasetCategory.SACRED,
                "instrumental": DatasetCategory.INSTRUMENTAL,
                "isorhythmic": DatasetCategory.ISORHYTHMIC,
            }
            category_filter = category_map.get(category.lower())
            if category_filter:
                entries = [e for e in entries if e.category == category_filter]

        typer.echo(f"Found {len(entries)} entries")

        for entry in entries:
            typer.echo(f"  - {entry.title}")
            typer.echo(f"    Composer: {entry.composer}")
            typer.echo(f"    Year: {entry.year}")
            typer.echo(f"    Mode: {entry.mode.value}")
            typer.echo(f"    Form: {entry.form.value}")
            typer.echo(f"    Category: {entry.category.value}")
            typer.echo(f"    Difficulty: {entry.difficulty_level}")
            if entry.source_reference:
                typer.echo(f"    Source: {entry.source_reference}")
            typer.echo()

    elif action == "query":
        # Get random entry matching criteria
        try:
            mode_filter = get_mode(mode) if mode else None
            form_filter = get_form(form) if form else None

            category_filter = None
            if category:
                category_map = {
                    "dance": DatasetCategory.DANCE,
                    "vocal": DatasetCategory.VOCAL,
                    "sacred": DatasetCategory.SACRED,
                    "instrumental": DatasetCategory.INSTRUMENTAL,
                    "isorhythmic": DatasetCategory.ISORHYTHMIC,
                }
                category_filter = category_map.get(category.lower())

            entry = dataset.get_random_entry(
                mode=mode_filter,
                form=form_filter,
                category=category_filter
            )

            typer.echo("Random Entry:")
            typer.echo(f"  Title: {entry.title}")
            typer.echo(f"  Composer: {entry.composer}")
            typer.echo(f"  Year: {entry.year}")
            typer.echo(f"  Mode: {entry.mode.value}")
            typer.echo(f"  Form: {entry.form.value}")
            typer.echo(f"  Category: {entry.category.value}")
            typer.echo(f"  Difficulty: {entry.difficulty_level}")
            typer.echo(f"  Tempo: {entry.score.tempo_bpm} BPM")
            typer.echo(f"  Voices: {len(entry.score.voices)}")
            typer.echo(f"  Duration: {entry.score.get_duration():.1f} seconds")
            if entry.source_reference:
                typer.echo(f"  Source: {entry.source_reference}")

        except ValueError as e:
            typer.echo(f"Error: {e}")


def save_as_json(score, output_path: Path) -> None:
    """Save a musical score as JSON.

    Args:
        score: The musical score to save
        output_path: Path to save the file
    """
    # Convert score to JSON-serializable format
    score_data = {
        "title": score.title,
        "composer": score.composer,
        "mode": score.mode.value if score.mode else None,
        "form": score.form.value if score.form else None,
        "tempo_bpm": score.tempo_bpm,
        "voices": []
    }

    for voice in score.voices:
        voice_data = {
            "name": voice.name,
            "instrument": voice.instrument.value if voice.instrument else None,
            "range_low": voice.range_low,
            "range_high": voice.range_high,
            "notes": []
        }

        for note in voice.notes:
            note_data = {
                "pitch": note.pitch,
                "duration": note.duration,
                "velocity": note.velocity,
                "start_time": note.start_time,
                "voice": note.voice,
                "is_rest": note.is_rest
            }
            voice_data["notes"].append(note_data)

        score_data["voices"].append(voice_data)

    # Write to file
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(score_data, f, indent=2)


def load_from_json(input_path: Path):
    """Load a musical score from JSON.

    Args:
        input_path: Path to the JSON file

    Returns:
        MusicalScore object
    """
    from .models import InstrumentType, MusicalForm, MusicalScore, Note, RenaissanceMode, Voice

    with input_path.open("r", encoding="utf-8") as f:
        score_data = json.load(f)

    # Create score
    score = MusicalScore(
        title=score_data.get("title", ""),
        composer=score_data.get("composer", ""),
        mode=RenaissanceMode(score_data["mode"]) if score_data.get("mode") else None,
        form=MusicalForm(score_data["form"]) if score_data.get("form") else None,
        tempo_bpm=score_data.get("tempo_bpm", 120.0)
    )

    # Add voices
    for voice_data in score_data.get("voices", []):
        voice = Voice(
            name=voice_data.get("name", ""),
            instrument=InstrumentType(voice_data["instrument"]) if voice_data.get("instrument") else None,
            range_low=voice_data.get("range_low", 110.0),
            range_high=voice_data.get("range_high", 880.0)
        )

        # Add notes
        for note_data in voice_data.get("notes", []):
            note = Note(
                pitch=note_data["pitch"],
                duration=note_data["duration"],
                velocity=note_data["velocity"],
                start_time=note_data["start_time"],
                voice=note_data.get("voice", 0),
                is_rest=note_data.get("is_rest", False)
            )
            voice.add_note(note)

        score.add_voice(voice)

    return score


def save_as_midi(score, output_path: Path) -> None:
    """Save a musical score as MIDI.

    Args:
        score: The musical score to save
        output_path: Path to save the file
    """
    try:
        import midi
    except ImportError:
        typer.echo("MIDI export requires the 'midi' package. Install with: pip install midi")
        return

    # Create MIDI file
    midi_file = midi.MIDIFile(1)  # One track

    # Add track name
    midi_file.addTrackName(0, 0, score.title)

    # Add tempo
    midi_file.addTempo(0, 0, score.tempo_bpm)

    # Add notes
    for voice_idx, voice in enumerate(score.voices):
        for note in voice.notes:
            if note.is_rest:
                continue

            # Convert pitch to MIDI note number
            midi_note = int(12 * (math.log2(note.pitch / 440.0) + 4.75))

            # Convert time to beats
            start_beat = note.start_time * score.tempo_bpm / 60.0
            duration_beat = note.duration * score.tempo_bpm / 60.0

            # Add note
            midi_file.addNote(
                track=0,
                channel=voice_idx,
                pitch=midi_note,
                time=start_beat,
                duration=duration_beat,
                volume=int(note.velocity * 100)
            )

    # Write to file
    with output_path.open("wb") as f:
        midi_file.writeFile(f)


if __name__ == "__main__":
    app()
