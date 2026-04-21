"""
orders.py
Orchestrates validation → API call → formatted output.
"""
from __future__ import annotations

from bot.client import BinanceFuturesClient
from bot.logging_config import get_logger
from bot.validators import validate_all

logger = get_logger(__name__)


def _print_separator() -> None:
    print("=" * 60)


def _print_request_summary(params: dict) -> None:
    _print_separator()
    print("📤  ORDER REQUEST SUMMARY")
    _print_separator()
    print(f"  Symbol     : {params['symbol']}")
    print(f"  Side       : {params['side']}")
    print(f"  Order Type : {params['order_type']}")
    print(f"  Quantity   : {params['quantity']}")
    if params.get("price"):
        print(f"  Price      : {params['price']}")
    if params.get("stop_price"):
        print(f"  Stop Price : {params['stop_price']}")
    _print_separator()


def _print_response_summary(response: dict) -> None:
    print("✅  ORDER RESPONSE")
    _print_separator()
    print(f"  Order ID     : {response.get('orderId', 'N/A')}")
    print(f"  Status       : {response.get('status', 'N/A')}")
    print(f"  Executed Qty : {response.get('executedQty', 'N/A')}")
    avg_price = response.get("avgPrice")
    print(
        f"  Avg Price    : "
        f"{avg_price if avg_price and float(avg_price) > 0 else 'N/A (pending)'}"
    )
    print(f"  Client OID   : {response.get('clientOrderId', 'N/A')}")
    _print_separator()
    print("🎉  Order placed successfully on Binance Futures Testnet!\n")


def place_order(
    client: BinanceFuturesClient,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: float | None = None,
    stop_price: float | None = None,
) -> dict:
    # Step 1 — Validate
    try:
        params = validate_all(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price,
            stop_price=stop_price,
        )
    except ValueError as exc:
        logger.error(f"Validation failed: {exc}")
        print(f"\n❌  Validation Error: {exc}\n")
        raise

    # Step 2 — Show request summary
    _print_request_summary(params)

    # Step 3 — Place order
    try:
        response = client.place_order(
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
            stop_price=params["stop_price"],
        )
    except Exception as exc:
        logger.error(f"Order placement failed: {exc}")
        print(f"\n❌  Order Failed: {exc}\n")
        print("    Check logs/trading_bot.log for details.\n")
        raise

    # Step 4 — Show response
    _print_response_summary(response)
    return response