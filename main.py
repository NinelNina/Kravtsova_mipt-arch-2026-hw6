from typing import Optional
from config import SUPPORTED_CURRENCIES, BASE_CURRENCY
from utils.logger import setup_logger
from converters import ConverterFactory


logger = setup_logger(__name__)


def get_user_amount() -> Optional[float]:
    try:
        user_input = input(f"Введите сумму в {BASE_CURRENCY}: ").strip()
        amount = float(user_input)

        if amount < 0:
            logger.error("Сумма не может быть отрицательной")
            return None

        return amount

    except ValueError:
        logger.error(f"Неверный формат числа: '{user_input}'")
        return None
    except KeyboardInterrupt:
        logger.info("Операция отменена пользователем")
        return None


def convert_and_display(amount: float, currency: str) -> bool:
    try:
        converter = ConverterFactory.create(currency)
        result = converter.convert(amount)

        if result is not None:
            print(f"{amount:.2f} {BASE_CURRENCY} = {result:.2f} {currency}")
            return True
        else:
            logger.warning(f"Не удалось конвертировать в {currency}")
            return False

    except ValueError as e:
        logger.error(f"Ошибка: {e}")
        return False
    except Exception as e:
        logger.error(f"Непредвиденная ошибка: {type(e).__name__}: {e}")
        return False


def main() -> int:
    logger.info("Запуск конвертера валют")

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
    logger.info(f"Завершено: {success_count}/{len(SUPPORTED_CURRENCIES)} успешных конвертаций")

    return 0 if success_count > 0 else 1


if __name__ == "__main__":
    main()
