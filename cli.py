"""
cli.py
Main CLI entry point.
"""
from __future__ import annotations

import argparse
import os
import sys

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

from bot.logging_config import setup_logging, get_logger
from bot.client import BinanceFuturesClient
from bot.orders import place_order

setup_logging()
logger = get_logger(__name__)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="trading_bot",
        description="🤖 Binance Futures Testnet Trading Bot (USDT-M)",
        formatter_class=argparse.RawTextHelpFormatter,
        epilog="""
Examples:
  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01
  python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
  python cli.py --symbol BTCUSDT --side BUY --type STOP_LIMIT --quantity 0.01 --price 65100 --stop-price 65000
        """,
    )
    parser.add_argument("--symbol",    required=True, help="e.g. BTCUSDT")
    parser.add_argument("--side",      required=True, choices=["BUY", "SELL"])
    parser.add_argument("--type",      dest="order_type", required=True,
                        choices=["MARKET", "LIMIT", "STOP_LIMIT"])
    parser.add_argument("--quantity",  required=True, type=float)
    parser.add_argument("--price",     type=float, default=None)
    parser.add_argument("--stop-price",dest="stop_price", type=float, default=None)
    parser.add_argument("--api-key",   dest="api_key", default=None)
    parser.add_argument("--api-secret",dest="api_secret", default=None)
    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    api_key    = args.api_key    or os.getenv("BINANCE_API_KEY", "")
    api_secret = args.api_secret or os.getenv("BINANCE_API_SECRET", "")

    if not api_key or not api_secret:
        parser.error(
            "API credentials required.\n"
            "Set BINANCE_API_KEY and BINANCE_API_SECRET as env variables."
        )

    logger.info(
        f"Bot started | symbol={args.symbol} | side={args.side} "
        f"| type={args.order_type} | qty={args.quantity}"
    )

    try:
        client = BinanceFuturesClient(api_key=api_key, api_secret=api_secret)
        place_order(
            client=client,
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
            stop_price=args.stop_price,
        )
    except (ValueError, KeyboardInterrupt):
        sys.exit(1)
    except Exception:
        logger.exception("Unexpected error.")
        print("\n❌  Unexpected error. Check logs/trading_bot.log\n")
        sys.exit(1)


if __name__ == "__main__":
    main()