from src.db.database import get_connection


def get_symbols():
    con = get_connection()

    try:
        result = con.execute(
            """
            SELECT DISTINCT symbol
            FROM prices
            ORDER BY symbol
            """
        ).fetchall()

        return [row[0] for row in result]

    finally:
        con.close()


def get_price_history(symbol: str):
    con = get_connection()

    try:
        return con.execute(
            """
            SELECT
                date,
                open,
                high,
                low,
                close,
                volume,
                trades
            FROM prices
            WHERE symbol = ?
            ORDER BY date
            """,
            [symbol],
        ).df()

    finally:
        con.close()