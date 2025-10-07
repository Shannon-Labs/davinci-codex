#!/usr/bin/env python3
"""
Demo script for Renaissance music composition generation.

This script demonstrates how to use the Renaissance music composition
components to generate, analyze, and save musical compositions.
"""

from pathlib import Path
import json

from davinci_codex.artifacts import ensure_artifact_dir
from davinci_codex.renaissance_music.composition import RenaissanceCompositionGenerator
from davinci_codex.renaissance_music.pattern_composer import PatternBasedComposer
from davinci_codex.renaissance_music.models import (
    InstrumentType,
    MusicalForm,
    RenaissanceMode,
    MusicalScore,
)
from davinci_codex.renaissance_music.cli import save_as_json


def analyze_composition(score) -> dict:
    """Analyze a composition and return statistics.
    
    Args:
        score: The musical score to analyze
        
    Returns:
        Dictionary with analysis results
    """
    analysis = {
        "title": score.title,
        "composer": score.composer,
        "form": score.form.value,
        "mode": score.mode.value,
        "tempo_bpm": score.tempo_bpm,
        "num_voices": len(score.voices),
        "total_duration": score.get_duration(),
        "voices": []
    }
    
    for i, voice in enumerate(score.voices):
        voice_analysis = {
            "name": voice.name,
            "instrument": voice.instrument.value,
            "num_notes": len(voice.notes),
            "pitch_range": [
                min(note.pitch for note in voice.notes if not note.is_rest),
                max(note.pitch for note in voice.notes if not note.is_rest)
            ]
        }
        analysis["voices"].append(voice_analysis)
    
    return analysis


def save_composition_analysis(analysis, output_path: Path) -> None:
    """Save composition analysis to a JSON file.
    
    Args:
        analysis: The analysis dictionary
        output_path: Path to save the analysis
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(analysis, f, indent=2)


def generate_example_compositions() -> dict:
    """Generate example compositions in different forms and modes.
    
    Returns:
        Dictionary with generated compositions
    """
    # Initialize composition generators
    ai_generator = RenaissanceCompositionGenerator()
    pattern_composer = PatternBasedComposer()
    
    # Define instrument assignments
    instrument_assignments = {
        0: InstrumentType.PROGRAMMABLE_FLUTE,
        1: InstrumentType.VIOLA_ORGANISTA,
        2: InstrumentType.MECHANICAL_ORGAN,
    }
    
    compositions = {}
    
    # Generate compositions in different forms and modes
    forms = [MusicalForm.PAVANE, MusicalForm.GALLIARD, MusicalForm.BASSE_DANSE]
    modes = [RenaissanceMode.LYDIAN, RenaissanceMode.DORIAN, RenaissanceMode.PHRYGIAN]
    
    for form in forms:
        for mode in modes:
            # Generate with AI composition generator
            ai_score = ai_generator.generate_composition(
                form=form,
                mode=mode,
                measures=16,
                instrument_assignments=instrument_assignments,
                seed=42
            )
            
            # Generate with pattern-based composer
            pattern_score = pattern_composer.compose_by_patterns(
                form=form,
                mode=mode,
                instrument_assignments=instrument_assignments,
                measures=16,
                seed=42
            )
            
            # Store compositions
            key = f"{form.value}_{mode.value}"
            compositions[key] = {
                "ai_score": ai_score,
                "pattern_score": pattern_score,
                "form": form.value,
                "mode": mode.value
            }
    
    return compositions


def save_compositions(compositions: dict, output_dir: Path) -> dict:
    """Save compositions to various formats.
    
    Args:
        compositions: Dictionary of compositions
        output_dir: Directory to save files
        
    Returns:
        Dictionary with file paths
    """
    ensure_artifact_dir(output_dir)
    
    saved_files = {}
    
    for key, comp_data in compositions.items():
        # Create subdirectory for this composition
        comp_dir = output_dir / key
        ensure_artifact_dir(comp_dir)
        
        # Save AI-generated score
        ai_file = comp_dir / "ai_score.json"
        ai_file.parent.mkdir(parents=True, exist_ok=True)
        save_as_json(comp_data["ai_score"], ai_file)
        
        # Save pattern-generated score
        pattern_file = comp_dir / "pattern_score.json"
        pattern_file.parent.mkdir(parents=True, exist_ok=True)
        save_as_json(comp_data["pattern_score"], pattern_file)
        
        # Analyze and save analysis
        ai_analysis = analyze_composition(comp_data["ai_score"])
        pattern_analysis = analyze_composition(comp_data["pattern_score"])
        
        ai_analysis_file = comp_dir / "ai_analysis.json"
        pattern_analysis_file = comp_dir / "pattern_analysis.json"
        
        save_composition_analysis(ai_analysis, ai_analysis_file)
        save_composition_analysis(pattern_analysis, pattern_analysis_file)
        
        # Store file paths
        saved_files[key] = {
            "ai_score": str(ai_file),
            "pattern_score": str(pattern_file),
            "ai_analysis": str(ai_analysis_file),
            "pattern_analysis": str(pattern_analysis_file)
        }
    
    return saved_files


def compare_compositions(compositions: dict) -> dict:
    """Compare AI-generated and pattern-based compositions.
    
    Args:
        compositions: Dictionary of compositions
        
    Returns:
        Dictionary with comparison results
    """
    comparisons = {}
    
    for key, comp_data in compositions.items():
        ai_score = comp_data["ai_score"]
        pattern_score = comp_data["pattern_score"]
        
        # Analyze both scores
        ai_analysis = analyze_composition(ai_score)
        pattern_analysis = analyze_composition(pattern_score)
        
        # Compare metrics
        comparison = {
            "form": comp_data["form"],
            "mode": comp_data["mode"],
            "tempo_difference": ai_analysis["tempo_bpm"] - pattern_analysis["tempo_bpm"],
            "duration_difference": ai_analysis["total_duration"] - pattern_analysis["total_duration"],
            "voice_count_difference": ai_analysis["num_voices"] - pattern_analysis["num_voices"],
            "ai_avg_notes_per_voice": sum(v["num_notes"] for v in ai_analysis["voices"]) / ai_analysis["num_voices"],
            "pattern_avg_notes_per_voice": sum(v["num_notes"] for v in pattern_analysis["voices"]) / pattern_analysis["num_voices"]
        }
        
        comparisons[key] = comparison
    
    return comparisons


def main():
    """Main demo function."""
    print("Renaissance Music Composition Demo")
    print("=" * 40)
    
    # Generate compositions
    print("Generating compositions...")
    compositions = generate_example_compositions()
    
    # Save compositions
    output_dir = Path("artifacts/renaissance_compositions")
    print(f"Saving compositions to {output_dir}...")
    saved_files = save_compositions(compositions, output_dir)
    
    # Compare compositions
    print("Comparing compositions...")
    comparisons = compare_compositions(compositions)
    
    # Save comparison results
    comparison_file = output_dir / "comparisons.json"
    comparison_file.parent.mkdir(parents=True, exist_ok=True)
    with comparison_file.open("w", encoding="utf-8") as f:
        json.dump(comparisons, f, indent=2)
    
    # Print summary
    print("\nDemo completed successfully!")
    print(f"Generated {len(compositions)} compositions")
    print(f"Files saved to {output_dir}")
    print(f"Comparison results saved to {comparison_file}")
    
    # Print a sample comparison
    sample_key = list(comparisons.keys())[0]
    sample_comparison = comparisons[sample_key]
    print(f"\nSample comparison for {sample_key}:")
    print(f"  Form: {sample_comparison['form']}")
    print(f"  Mode: {sample_comparison['mode']}")
    print(f"  Tempo difference: {sample_comparison['tempo_difference']:.2f} BPM")
    print(f"  Duration difference: {sample_comparison['duration_difference']:.2f} seconds")
    print(f"  AI avg notes per voice: {sample_comparison['ai_avg_notes_per_voice']:.2f}")
    print(f"  Pattern avg notes per voice: {sample_comparison['pattern_avg_notes_per_voice']:.2f}")


if __name__ == "__main__":
    main()