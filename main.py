"""
main.py
-------
Order Book Imbalance Tracker — Entry Point

Connects to Binance's free public WebSocket and streams live
order book depth data. Calculates imbalance every update and
prints buy/sell pressure signals directly in your terminal.

Usage:
    python main.py                        # default: BTCUSDT, 10 levels
    python main.py --symbol ethusdt       # track ETH
    python main.py --symbol solusdt --levels 5  # top 5 levels only
    python main.py --no-log               # skip CSV logging

No API key required — Binance depth stream is fully public.
"""

import json
import argparse
import websocket  # websocket-client library

# Our own modules (all in src/)
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from imbalance import calculate_imbalance
from display   import print_header, print_snapshot
from logger    import init_logger, log_snapshot


# ── Global state ──────────────────────────────────────────────────────────────
# We store the latest bids and asks here so the WebSocket callback can access them.
state = {
    "bids":       [],
    "asks":       [],
    "levels":     10,
    "enable_log": True,
    "update_count": 0,
}


# ── WebSocket Callbacks ────────────────────────────────────────────────────────

def on_message(ws, message):
    """
    Called automatically every time Binance sends new order book data.
    This is the hot path — keep it fast.
    """
    data = json.loads(message)

    # Binance depth stream format:
    # { "bids": [["price", "qty"], ...], "asks": [["price", "qty"], ...] }
    bids = data.get("bids", [])
    asks = data.get("asks", [])

    # Skip empty updates (can happen on reconnect)
    if not bids or not asks:
        return

    # Update shared state
    state["bids"] = bids
    state["asks"] = asks
    state["update_count"] += 1

    # Calculate imbalance for the top N levels
    result = calculate_imbalance(bids, asks, levels=state["levels"])

    # Print to terminal
    print_snapshot(result)

    # Log to CSV (if enabled)
    if state["enable_log"]:
        log_snapshot(result)


def on_error(ws, error):
    """Called if the WebSocket hits an error."""
    print(f"\n[ERROR] WebSocket error: {error}")


def on_close(ws, close_status_code, close_msg):
    """Called when the connection closes (Ctrl+C or network drop)."""
    print(f"\n[INFO] Connection closed. Total updates received: {state['update_count']}")
    if state["enable_log"]:
        print(f"[INFO] Signals saved to: logs/signals.csv")


def on_open(ws):
    """Called once when the WebSocket first connects successfully."""
    # Nothing special needed — Binance streams data automatically after connect
    pass


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Real-time Order Book Imbalance Tracker via Binance WebSocket"
    )
    parser.add_argument(
        "--symbol",
        type=str,
        default="btcusdt",
        help="Trading pair to track (default: btcusdt)"
    )
    parser.add_argument(
        "--levels",
        type=int,
        default=10,
        choices=[5, 10, 20],
        help="Number of top order book levels to use (default: 10)"
    )
    parser.add_argument(
        "--no-log",
        action="store_true",
        help="Disable CSV logging"
    )
    args = parser.parse_args()

    # Store config in shared state
    symbol            = args.symbol.lower()
    state["levels"]   = args.levels
    state["enable_log"] = not args.no_log

    # Initialise CSV logger (creates file + header if needed)
    if state["enable_log"]:
        init_logger()

    # Binance public WebSocket URL for partial book depth
    # @depth{levels}@100ms  →  top N levels, pushed every 100 ms
    url = f"wss://stream.binance.com:9443/ws/{symbol}@depth{args.levels}@100ms"

    # Print header once before streaming begins
    print_header(symbol, args.levels)
    print(f"  Connecting to Binance... (Press Ctrl+C to stop)\n")

    # Create WebSocket app and start streaming
    ws = websocket.WebSocketApp(
        url,
        on_open    = on_open,
        on_message = on_message,
        on_error   = on_error,
        on_close   = on_close,
    )

    # run_forever() blocks here and calls our callbacks as data arrives.
    # ping_interval keeps the connection alive; reconnect on drop.
    ws.run_forever(ping_interval=20, ping_timeout=10)


if __name__ == "__main__":
    main()
