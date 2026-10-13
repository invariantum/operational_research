"""The Part B data generator must be deterministic, personalised and leak no local paths."""
from __future__ import annotations

import json
import subprocess

import pandas as pd
import pytest

from conftest import PYTHON, REPO_ROOT

GENERATOR = REPO_ROOT / "02-coursework-part-b/starter-repo/generate_data.py"


def generate(student_id, out_dir):
    subprocess.run(
        [PYTHON, str(GENERATOR), "--student_id", student_id, "--out_dir", str(out_dir)],
        check=True,
        capture_output=True,
        text=True,
    )
    return out_dir


@pytest.fixture(scope="module")
def datasets(tmp_path_factory):
    base = tmp_path_factory.mktemp("generated")
    return {
        "a1": generate("100000000", base / "a1"),
        "a2": generate("100000000", base / "a2"),
        "b": generate("TEST001", base / "b"),
    }


@pytest.mark.parametrize("name", ["zones.csv", "stores.csv", "zone_store_dist.csv", "margins.json"])
def test_same_id_gives_identical_data(datasets, name):
    assert (datasets["a1"] / name).read_bytes() == (datasets["a2"] / name).read_bytes()


def test_different_ids_give_different_data(datasets):
    assert (datasets["a1"] / "zones.csv").read_bytes() != (datasets["b"] / "zones.csv").read_bytes()


def test_dataset_structure(datasets):
    d = datasets["a1"]
    zones = pd.read_csv(d / "zones.csv")
    stores = pd.read_csv(d / "stores.csv")
    dist = pd.read_csv(d / "zone_store_dist.csv")
    assert len(zones) == 300 and len(stores) == 80 and len(dist) == 300 * 80
    missing_share = zones["historical_sales"].isna().mean()
    assert 0.33 <= missing_share <= 0.50
    assert (dist["distance_km"] >= 0).all()
    assert set(dist["zone_id"]) == set(zones["zone_id"])
    assert set(dist["store_id"]) == set(stores["store_id"])


def test_manifest_has_no_absolute_paths(datasets):
    manifest = json.loads((datasets["a1"] / "manifest.json").read_text(encoding="utf-8"))
    text = json.dumps(manifest)
    assert ":\\\\" not in text and not manifest["base_dir"].startswith("/"), manifest["base_dir"]
