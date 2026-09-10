from src.pipeline.historical import load_history
from src.db.database import get_connection


def test_load_history():

    symbol = "فملی"

    load_history(
        symbol=symbol,
        provider_name="tsetmc",
        limit=10,
    )

    con = get_connection()

    count = con.execute(
        """
        SELECT COUNT(*)
        FROM prices
        WHERE symbol = ?
        """,
        [symbol],
    ).fetchone()[0]

    con.close()

    assert count > 0