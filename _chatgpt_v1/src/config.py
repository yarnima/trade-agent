# src/config.py
import yaml
from pathlib import Path

CONFIG_PATH = Path(__file__).parent.parent / "config" / "assets.yaml"

def load_assets():
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def get_symbols():
    config = load_assets()

    all_assets = []

    for asset_type, items in config.items():
        for item in items:
            all_assets.append({
                "symbol": item["symbol"],
                "type": asset_type,          # 'stocks' or 'crypto'
                "provider": item["provider"],
            })

    return all_assets