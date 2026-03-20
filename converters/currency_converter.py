from typing import Optional
from utils.logger import setup_logger
from api.api_rates import ApiRates
from utils.cache import Cache


logger = setup_logger(__name__)


class CurrencyConverter:
    def __init__(
            self,
            target_currency: str,
            base_currency: str,
            api_rates: ApiRates,
            cache: Cache
    ):
        self.base_currency = base_currency.upper()
        self.target_currency = target_currency.upper()
        self._api_rates = api_rates
        self._cache = cache
        self._rates: Optional[dict[str, float]] = None

    def _get_cache_key(self) -> str:
        return f"{self.base_currency}"

    def _fetch_rates(self) -> Optional[dict[str, float]]:
        cache_key = self._get_cache_key()

        cached = self._cache.get(cache_key)
        if cached is not None:
            logger.debug(f"Using cached rates for {self.base_currency}")
            return cached

        rates = self._api_rates.get_rates(self.base_currency)

        if rates and self._cache:
            self._cache.set(cache_key, rates)

        return rates

    def get_rate(self) -> Optional[float]:
        if self._rates is None:
            self._rates = self._fetch_rates()

        rate = self._rates.get(self.target_currency) if self._rates else None

        if rate is None:
            logger.warning(f"Rate for {self.target_currency} not found")

        return rate

    def convert(self, amount: float) -> Optional[float]:
        if amount < 0:
            logger.error(f"Negative amount: {amount}")
            return None

        rate = self.get_rate()
        if rate is None:
            return None

        return round(amount * rate, 2)

    def clear_cache(self) -> None:
        if self._cache:
            self._cache.clear(self._get_cache_key())
