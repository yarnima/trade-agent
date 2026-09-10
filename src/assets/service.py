from src.assets.repository import (
    get_asset,
    update_provider_symbol,
    upsert_asset,
)

from src.providers.factory import get_provider


def sync_assets(config):

    for asset in config.get("stocks", []):

        upsert_asset(
            symbol=asset["symbol"],
            asset_type="stock",
            provider=asset["provider"],
            provider_symbol=None,
        )

    for asset in config.get("crypto", []):

        upsert_asset(
            symbol=asset["symbol"],
            asset_type="crypto",
            provider=asset["provider"],
            provider_symbol=None,
        )


def resolve_provider_symbol(
    symbol: str,
    provider_name: str,
) -> str:

    asset = get_asset(symbol)

    if asset is None:
        raise ValueError(
            f"Asset not found: {symbol}"
        )

    provider_symbol = asset[3]

    if provider_symbol:
        return provider_symbol

    provider = get_provider(provider_name)

    provider_symbol = provider.resolve_symbol(symbol)

    update_provider_symbol(
        symbol=symbol,
        provider_symbol=provider_symbol,
    )

    return provider_symbol