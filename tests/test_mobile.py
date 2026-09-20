import sqlite3

import pytest

from mobile.rules import evaluate_condition
from mobile.storage import LocalStore, check_password, password_hash


def test_password_hash_round_trip():
    encoded = password_hash("rahasia-aman")
    assert check_password("rahasia-aman", encoded)
    assert not check_password("salah", encoded)


def test_local_store_seeds_trees_and_persists_inspection(tmp_path):
    store = LocalStore(tmp_path / "mobile.sqlite3")
    store.register("petugas", "rahasia-aman")

    trees = store.trees()
    assert len(trees) == 12
    assert store.authenticate("petugas", "rahasia-aman")

    store.save_inspection(
        trees[0]["id"],
        {
            **evaluate_condition(
                surface_dark=False,
                standing_water=True,
                leaf_wilt=True,
                moisture="WATERLOGGED",
            ),
            "surface_dark": False,
            "standing_water": True,
            "leaf_wilt": True,
            "moisture": "WATERLOGGED",
            "notes": "uji",
        },
    )
    assert store.inspections(trees[0]["id"])[0]["condition"] == "PERLU_PERHATIAN"


def test_duplicate_username_is_rejected(tmp_path):
    store = LocalStore(tmp_path / "mobile.sqlite3")
    store.register("petugas", "rahasia-aman")
    with pytest.raises(sqlite3.IntegrityError):
        store.register("petugas", "rahasia-lain")


def test_backup_round_trip(tmp_path):
    source = LocalStore(tmp_path / "source.sqlite3")
    tree = source.trees()[0]
    source.save_inspection(
        tree["id"],
        {
            **evaluate_condition(
                surface_dark=True,
                standing_water=False,
                leaf_wilt=False,
                moisture="MOIST",
            ),
            "surface_dark": True,
            "standing_water": False,
            "leaf_wilt": False,
            "moisture": "MOIST",
            "notes": "backup",
        },
    )
    backup = source.export_backup(tmp_path / "backup.json")
    restored = LocalStore(tmp_path / "restored.sqlite3")
    assert restored.import_backup(backup) == 1
    assert restored.inspections(tree["id"])[0]["notes"] == "backup"
