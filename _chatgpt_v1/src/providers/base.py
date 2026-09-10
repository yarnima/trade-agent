from abc import ABC, abstractmethod

import pandas as pd


class MarketDataProvider(ABC):

    @abstractmethod
    def get_history(
        self,
        provider_symbol: str,
        limit: int | None = None,
    ) -> pd.DataFrame:
        """
        Fetch historical market data.

        Returns a normalized DataFrame.
        """
        pass