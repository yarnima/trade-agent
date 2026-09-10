from src.db.database import get_connection


def initialize_database():

    con = get_connection()

    con.execute("""
        CREATE TABLE IF NOT EXISTS assets (
            symbol VARCHAR PRIMARY KEY,
            asset_type VARCHAR,
            provider VARCHAR,
            provider_symbol VARCHAR,
            active BOOLEAN DEFAULT TRUE
        )
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS prices (
            symbol VARCHAR,
            date DATE,

            open DOUBLE,
            high DOUBLE,
            low DOUBLE,
            close DOUBLE,
            last DOUBLE,

            volume DOUBLE,
            value DOUBLE,
            trades BIGINT,

            PRIMARY KEY (symbol, date)
        )
    """)

    con.close()