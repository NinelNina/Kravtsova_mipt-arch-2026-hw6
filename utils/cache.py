import json
import time
from pathlib import Path
from typing import Optional, Any
from config import CACHE_EXPIRY_SECONDS, CACHE_DIR
from utils.logger import setup_logger


logger = setup_logger(__name__)


class Cache:
    def __init__(
            self,
            namespace: str,
            expiry_seconds: int = CACHE_EXPIRY_SECONDS,
            cache_dir: str = CACHE_DIR
    ):
        self.namespace = namespace
        self.expiry_seconds = expiry_seconds
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def _get_path(self, key: str) -> Path:
        return self.cache_dir / f"{self.namespace}_{key}.json"

    def get(self, key: str) -> Optional[Any]:
        path = self._get_path(key)
        if not path.exists():
            return None

        try:
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)

            if time.time() - data["timestamp"] > self.expiry_seconds:
                logger.debug(f"Cache expired: {key}")
                return None

            logger.debug(f"Cache hit: {key}")
            return data["value"]

        except (json.JSONDecodeError, KeyError, OSError) as e:
            logger.warning(f"Cache read error: {e}")
            return None

    def set(self, key: str, value: Any) -> None:
        path = self._get_path(key)
        try:
            data = {"value": value, "timestamp": time.time()}
            with open(path, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logger.debug(f"Cache saved: {key}")
        except OSError as e:
            logger.error(f"Cache write error: {e}")

    def clear(self, key: str) -> None:
        path = self._get_path(key)
        if path.exists():
            path.unlink()
            logger.debug(f"Cache cleared: {key}")