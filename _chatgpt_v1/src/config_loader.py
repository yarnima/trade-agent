from pathlib import Path

import yaml


ROOT_DIR = Path(__file__).resolve().parents[1]
ASSETS_FILE = ROOT_DIR / "config" / "assets.yaml"


def load_assets():
    with open(ASSETS_FILE, "r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    return config