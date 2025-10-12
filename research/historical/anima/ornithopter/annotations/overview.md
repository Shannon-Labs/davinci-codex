# Ornithopter Annotation Overview

This directory records normalized vector overlays and semantic tags applied to the original folios. Detailed SVG layers are stored in the `svg/` subfolder (to be generated from Illustrator/Inkscape sessions). Each annotation links back to coordinates in the source scan and maps to component IDs in `intent.json`.

| ID | Folio | Description | Linked Component |
|----|-------|-------------|------------------|
| A1 | CA-846r | Wing spar locus traced along primary sketch | `wing_spar_left`, `wing_spar_right` |
| A2 | CA-846r | Crank pedal assembly at pilot's feet | `pedal_crank` |
| A3 | MSB-70r | Torsion spring depiction at shoulder joint | `torsion_spring_pair` |
| A4 | FLIGHT-12v | Camber curvature guides extracted from feather study | `flex_skin` |

**Coordinate System**
- Images normalized to 300 DPI; origin at lower left corner.
- All coordinates stored as pixels with millimeter conversion factor 0.0847 mm/pixel.

**Next Steps**
1. Export final SVG overlays with layer naming convention `component/<component_id>.svg`.
2. Auto-generate JSON coordinate sets via `scripts/trace_annotations.py` (to be authored).
3. Review ambiguous linkages (especially pedal-to-wing rods) with subject-matter experts.
