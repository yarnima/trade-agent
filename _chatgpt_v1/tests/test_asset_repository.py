from src.assets.repository import get_asset
from src.db.database import get_connection
from src.assets.repository import (
    get_asset,
    update_provider_symbol,
    upsert_asset,
)

def test_get_asset():

    con = get_connection()

    con.execute(
        """
        INSERT OR REPLACE INTO assets
        (
            symbol,
            asset_type,
            provider,
            provider_symbol,
            active
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            "TEST",
            "crypto",
            "binance",
            "TESTUSDT",
            True,
        ],
    )

    con.close()

    asset = get_asset("TEST")

    assert asset is not None
    assert asset[0] == "TEST"
    assert asset[1] == "crypto"
    assert asset[2] == "binance"
    assert asset[3] == "TESTUSDT"
    assert asset[4] is True


def test_update_provider_symbol():

    upsert_asset(
        symbol="TEST_CACHE",
        asset_type="stock",
        provider="tsetmc",
        provider_symbol=None,
    )

    update_provider_symbol(
        symbol="TEST_CACHE",
        provider_symbol="123456789",
    )

    asset = get_asset("TEST_CACHE")

    assert asset is not None
    assert asset[0] == "TEST_CACHE"
    assert asset[3] == "123456789"