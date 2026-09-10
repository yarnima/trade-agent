from src.providers.tsetmc import TSETMCProvider


def test_search_femli():
    provider = TSETMCProvider()

    result = provider.search_symbol("فملی")

    print()
    print("Search result:")
    print(result)

    assert result["symbol"]
    assert result["ins_code"]


def test_get_history():
    provider = TSETMCProvider()

    result = provider.search_symbol("فملی")

    df = provider.get_history(
        result["ins_code"],
        limit=10,
    )

    print()
    print(df)

    assert not df.empty

    required_columns = {
        "date",
        "open",
        "high",
        "low",
        "close",
        "last",
        "volume",
        "value",
        "trades",
    }

    assert required_columns.issubset(df.columns)


def test_resolve_symbol():
    provider = TSETMCProvider()

    provider_symbol = provider.resolve_symbol("فملی")

    assert provider_symbol


def test_get_history_by_provider_symbol():
    provider = TSETMCProvider()

    provider_symbol = provider.resolve_symbol("فملی")

    df = provider.get_history(
        provider_symbol,
        limit=10,
    )

    assert not df.empty
    assert len(df) <= 10