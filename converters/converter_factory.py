from typing import Optional
from config import SUPPORTED_CURRENCIES, BASE_CURRENCY
from .currency_converter import CurrencyConverter
from api.api_rates import ApiRates
from utils.cache import Cache


class ConverterFactory:
    @classmethod
    def create(
            cls,
            target_currency: str,
            base_currency: Optional[str] = None,
    ) -> CurrencyConverter:
        target = target_currency.upper()
        base = (base_currency or BASE_CURRENCY).upper()

        if target not in SUPPORTED_CURRENCIES:
            raise ValueError(
                f"Unsupported currency: {target}. "
                f"Supported: {', '.join(SUPPORTED_CURRENCIES)}"
            )

        rates_provider = ApiRates()
        cache = Cache("rates")

        return CurrencyConverter(
            target_currency=target,
            base_currency=base,
            api_rates=rates_provider,
            cache=cache
        )
