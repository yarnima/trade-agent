from src.providers.base import MarketDataProvider
from src.providers.binance import BinanceProvider
from src.providers.tsetmc import TSETMCProvider


def get_provider(
    provider_name: str,
) -> MarketDataProvider:

    providers = {
        "binance": BinanceProvider,
        "tsetmc": TSETMCProvider,
    }

    try:
        provider_class = providers[
            provider_name
        ]

    except KeyError:
        raise ValueError(
            f"Unsupported provider: {provider_name}"
        )

    return provider_class()