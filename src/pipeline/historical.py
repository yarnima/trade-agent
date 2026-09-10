from src.assets.service import resolve_provider_symbol
from src.db.database import get_connection
from src.providers.factory import get_provider


def load_history(
    symbol: str,
    provider_name: str,
    limit: int | None = None,
):
    try:
        provider = get_provider(provider_name)

        provider_symbol = resolve_provider_symbol(
            symbol=symbol,
            provider_name=provider_name,
        )

        df = provider.get_history(
            provider_symbol=provider_symbol,
            limit=limit,
        )

        if df.empty:
            print(
                f"[WARN] {symbol}: no data"
            )
            return False

        df["symbol"] = symbol

        con = get_connection()

        try:
            con.register(
                "temp_prices",
                df,
            )

            con.execute(
                """
                INSERT OR REPLACE INTO prices
                (
                    symbol,
                    date,
                    open,
                    high,
                    low,
                    close,
                    last,
                    volume,
                    value,
                    trades
                )
                SELECT
                    symbol,
                    date,
                    open,
                    high,
                    low,
                    close,
                    last,
                    volume,
                    value,
                    trades
                FROM temp_prices
                """
            )

            con.unregister(
                "temp_prices"
            )

        finally:
            con.close()

        print(
            f"[OK]   {symbol}: "
            f"{len(df)} rows loaded"
        )

        return True

    except Exception as exc:
        print(
            f"[WARN] {symbol}: {exc}"
        )
        return False