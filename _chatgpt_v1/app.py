from src.assets.service import sync_assets
from src.config_loader import load_assets
from src.db.schema import initialize_database
from src.pipeline.historical import load_history


def main():

    initialize_database()

    config = load_assets()

    sync_assets(config)

    assets = (
        config.get("stocks", [])
        + config.get("crypto", [])
    )

    for asset in assets:

        load_history(
            symbol=asset["symbol"],
            provider_name=asset["provider"],
        )


if __name__ == "__main__":
    main()