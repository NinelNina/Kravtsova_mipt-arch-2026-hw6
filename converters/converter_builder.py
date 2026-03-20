from typing import Optional
from config import SUPPORTED_CURRENCIES, BASE_CURRENCY
from .currency_converter import CurrencyConverter
from api.api_rates import ApiRates
from utils.cache import Cache


class ConverterBuilder:
    @staticmethod
    def _validate_currency(currency: str) -> str:
        code = currency.upper()
        if code not in SUPPORTED_CURRENCIES:
            raise ValueError(
                f"Unsupported currency: {code}. "
                f"Supported: {', '.join(SUPPORTED_CURRENCIES)}"
            )
        return code

    @classmethod
    def build(
            cls,
            target_currency: str,
            base_currency: Optional[str] = None,
            rates_provider: Optional[ApiRates] = None,
            cache: Optional[Cache] = None
    ) -> CurrencyConverter:

        target = cls._validate_currency(target_currency)
        base = (base_currency or BASE_CURRENCY).upper()

        api = rates_provider or ApiRates()
        cache_strategy = cache or Cache("rates")

        return CurrencyConverter(
            target_currency=target,
            base_currency=base,
            api_rates=api,
            cache=cache_strategy
        )
