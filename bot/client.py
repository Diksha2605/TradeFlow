"""
client.py
Binance Futures Testnet REST client with HMAC-SHA256 signing.
"""
from __future__ import annotations

import hashlib
import hmac
import time

import requests

from bot.logging_config import get_logger

BASE_URL = "https://demo-fapi.binance.com"
logger = get_logger(__name__)


class BinanceFuturesClient:

    def __init__(self, api_key: str, api_secret: str, timeout: int = 10) -> None:
        if not api_key or not api_secret:
            raise ValueError("API key and secret must not be empty.")
        self.api_key = api_key
        self._api_secret = api_secret
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update({"X-MBX-APIKEY": self.api_key})

    def _sign(self, params: dict) -> dict:
        params["timestamp"] = int(time.time() * 1000)
        query_string = "&".join(f"{k}={v}" for k, v in params.items())
        signature = hmac.new(
            self._api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        params["signature"] = signature
        return params

    def _post(self, endpoint: str, params: dict) -> dict:
        signed = self._sign(params)
        url = f"{BASE_URL}{endpoint}"
        logger.debug(
            f"POST {url} | params: "
            f"{ {k: v for k, v in signed.items() if k != 'signature'} }"
        )
        try:
            resp = self._session.post(url, data=signed, timeout=self.timeout)
            resp.raise_for_status()
            data: dict = resp.json()
            logger.debug(f"Response [{resp.status_code}]: {data}")
            return data
        except requests.exceptions.HTTPError:
            logger.error(
                f"HTTP {resp.status_code} | endpoint={endpoint} | body={resp.text}"
            )
            raise
        except requests.exceptions.ConnectionError as exc:
            logger.error(f"Network error: {exc}")
            raise
        except requests.exceptions.Timeout:
            logger.error(f"Request timed out after {self.timeout}s")
            raise

    def place_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        quantity: float,
        price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "GTC",
    ) -> dict:
        params: dict = {
            "symbol": symbol,
            "side": side,
            "type": order_type if order_type != "STOP_LIMIT" else "STOP",
            "quantity": quantity,
        }

        if order_type in {"LIMIT", "STOP_LIMIT"}:
            params["price"] = price
            params["timeInForce"] = time_in_force

        if order_type == "STOP_LIMIT":
            params["stopPrice"] = stop_price

        logger.info(
            f"[ORDER REQUEST] symbol={symbol} | side={side} | type={order_type} "
            f"| qty={quantity} | price={price} | stopPrice={stop_price}"
        )
        result = self._post("/fapi/v1/order", params)
        logger.info(
            f"[ORDER SUCCESS] orderId={result.get('orderId')} "
            f"| status={result.get('status')} "
            f"| executedQty={result.get('executedQty')} "
            f"| avgPrice={result.get('avgPrice')}"
        )
        return result