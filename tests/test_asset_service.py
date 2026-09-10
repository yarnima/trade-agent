from src.assets.service import (
    resolve_provider_symbol,
    sync_assets,
)

from src.assets.repository import get_asset
from unittest.mock import patch

def test_resolve_provider_symbol_does_not_call_api_when_cached():

    sync_assets({
        "stocks": [
            {
                "symbol": "فملی",
                "provider": "tsetmc",
            }
        ]
    })

    # First call: populate the cache
    first = resolve_provider_symbol(
        symbol="فملی",
        provider_name="tsetmc",
    )

    with patch(
        "src.assets.service.get_provider"
    ) as mock_get_provider:

        second = resolve_provider_symbol(
            symbol="فملی",
            provider_name="tsetmc",
        )

        mock_get_provider.assert_not_called()

    assert second == first

def test_resolve_provider_symbol():

    sync_assets({
        "stocks": [
            {
                "symbol": "فملی",
                "provider": "tsetmc",
            }
        ]
    })

    provider_symbol = resolve_provider_symbol(
        symbol="فملی",
        provider_name="tsetmc",
    )

    assert provider_symbol

    asset = get_asset("فملی")

    assert asset is not None
    assert asset[3] == provider_symbol

def test_resolve_provider_symbol_uses_cache():

    sync_assets({
        "stocks": [
            {
                "symbol": "فملی",
                "provider": "tsetmc",
            }
        ]
    })

    first = resolve_provider_symbol(
        symbol="فملی",
        provider_name="tsetmc",
    )

    second = resolve_provider_symbol(
        symbol="فملی",
        provider_name="tsetmc",
    )

    assert first == second