from pathlib import Path
import yaml

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "symbols.yml"


def load_symbols() -> dict:
    with open(CONFIG_PATH, encoding="utf-8") as f:
        return yaml.safe_load(f)