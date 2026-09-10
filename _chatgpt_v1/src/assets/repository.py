from src.db.database import get_connection


def get_asset(symbol: str):
    con = get_connection()

    result = con.execute(
        """
        SELECT
            symbol,
            asset_type,
            provider,
            provider_symbol,
            active
        FROM assets
        WHERE symbol = ?
        """,
        [symbol],
    ).fetchone()

    con.close()

    return result


def get_all_assets():
    con = get_connection()

    result = con.execute(
        """
        SELECT
            symbol,
            asset_type,
            provider,
            provider_symbol,
            active
        FROM assets
        WHERE active = TRUE
        ORDER BY symbol
        """
    ).fetchall()

    con.close()

    return result


def upsert_asset(
    symbol: str,
    asset_type: str,
    provider: str,
    provider_symbol: str | None,
):
    con = get_connection()

    con.execute(
        """
        INSERT INTO assets
        (
            symbol,
            asset_type,
            provider,
            provider_symbol,
            active
        )
        VALUES (?, ?, ?, ?, TRUE)

        ON CONFLICT (symbol)
        DO UPDATE SET
            asset_type = EXCLUDED.asset_type,
            provider = EXCLUDED.provider,
            provider_symbol = EXCLUDED.provider_symbol,
            active = EXCLUDED.active
        """,
        [
            symbol,
            asset_type,
            provider,
            provider_symbol,
        ],
    )

    con.close()

def update_provider_symbol(
    symbol: str,
    provider_symbol: str,
):
    con = get_connection()

    con.execute(
        """
        UPDATE assets
        SET provider_symbol = ?
        WHERE symbol = ?
        """,
        [
            provider_symbol,
            symbol,
        ],
    )

    con.close()