from typing import Optional
from config import SUPPORTED_CURRENCIES, BASE_CURRENCY
from utils.logger import setup_logger
from converters import ConverterBuilder


logger = setup_logger(__name__)


def get_user_amount() -> Optional[float]:
    try:
        user_input = input(f"Введите сумму в {BASE_CURRENCY}: ").strip()
        amount = float(user_input)

        if amount <= 0:
            logger.error("The amount cannot be less than or equal to zero")
            return None

        return amount

    except ValueError:
        logger.error(f"Unexpected number format: '{user_input}'")
        return None
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        return None


def convert_and_display(amount: float, currency: str) -> bool:
    try:
        converter = ConverterBuilder.build(currency)
        result = converter.convert(amount)

        if result is not None:
            print(f"{amount:.2f} {BASE_CURRENCY} = {result:.2f} {currency}")
            return True
        else:
            logger.warning(f"Failed convert to {currency}")
            return False

    except ValueError as e:
        logger.error(f"Error: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {type(e).__name__}: {e}")
        return False


def main() -> int:
    logger.info("Starting currency converter")

    amount = get_user_amount()
    if amount is None:
        return 1

    success_count = 0

    print(f"\nКонвертация {amount:.2f} {BASE_CURRENCY}:")
    print("-" * 40)

    for currency in SUPPORTED_CURRENCIES:
        if convert_and_display(amount, currency):
            success_count += 1

    print("-" * 40)
    logger.info(f"Completed: {success_count}/{len(SUPPORTED_CURRENCIES)} successful conversions")

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    main()
