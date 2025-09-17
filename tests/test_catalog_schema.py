from pathlib import Path

import yaml

from davinci_codex.catalog import Catalog


def test_catalog_yaml_conforms_and_links_provenance():
    root = Path(__file__).resolve().parents[1]
    catalog_path = root / "inventions" / "catalog.yaml"
    data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    catalog = Catalog.model_validate(data)

    slugs = [record.slug for record in catalog.inventions]
    assert len(slugs) == len(set(slugs))

    for record in catalog.inventions:
        provenance_path = (root / record.provenance).resolve()
        assert provenance_path.exists(), f"Missing provenance file for {record.slug}"
        provenance_data = yaml.safe_load(provenance_path.read_text(encoding="utf-8"))
        assert provenance_data.get("slug") == record.slug
        assert provenance_data.get("folio_id") == record.folio_reference

    category_counts = {}
    for record in catalog.inventions:
        category_counts.setdefault(record.category, 0)
        category_counts[record.category] += 1
    for category, count in category_counts.items():
        assert count <= catalog.overview.focus_areas[category]

    assert catalog.overview.documented == len(catalog.inventions)
    assert catalog.overview.total_target >= len(catalog.inventions)
