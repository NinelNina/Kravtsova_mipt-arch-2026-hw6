import requests
import json
from typing import Optional
from config import API_BASE_URL, API_TIMEOUT, API_RETRIES
from utils.logger import setup_logger


logger = setup_logger(__name__)


class ApiRates:
    def __init__(
        self,
        timeout: int = API_TIMEOUT,
        retries: int = API_RETRIES,
        base_url: str = API_BASE_URL
    ):
        self.timeout = timeout
        self.retries = retries
        self.base_url = base_url

    def get_rates(self, base_currency: str) -> Optional[dict[str, float]]:
        url = f"{self.base_url}{base_currency.upper()}"

        for attempt in range(self.retries):
            try:
                logger.debug(f"Fetching rates from {url} (attempt {attempt + 1})")

                response = requests.get(
                    url,
                    timeout=self.timeout
                )
                response.raise_for_status()

                data = response.json()
                rates = data.get("rates")

                if not isinstance(rates, dict):
                    logger.error("Invalid API response: 'rates' is not a dict")
                    return None

                return {k.upper(): v for k, v in rates.items()}

            except requests.exceptions.Timeout:
                logger.warning(f"Timeout on attempt {attempt + 1}")
            except requests.exceptions.ConnectionError:
                logger.warning(f"Connection error on attempt {attempt + 1}")
            except requests.exceptions.HTTPError as e:
                logger.error(f"HTTP {e.response.status_code}: {e}")
                if 400 <= e.response.status_code < 500:
                    break
            except json.JSONDecodeError as e:
                logger.error(f"JSON parse error: {e}")
                break
            except Exception as e:
                logger.error(f"Unexpected error: {type(e).__name__}: {e}")
                break

        logger.error(f"Failed to fetch rates after {self.retries} attempts")
        return None
