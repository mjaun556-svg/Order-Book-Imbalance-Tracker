"""
display.py
----------
Terminal display helpers for real-time streaming output.

Keeps all print/formatting logic separate from business logic
so the main file stays clean and readable.
"""

import os
from datetime import datetime


def clear_line():
    """Move cursor up one line and clear it (for live updates)."""
    print("\033[A\033[K", end="")


def print_header(symbol: str, levels: int):
    """Print a one-time header when the tracker starts."""
    print("=" * 55)
    print(f"  📊 Order Book Imbalance Tracker")
    print(f"  Symbol : {symbol.upper()}")
    print(f"  Levels : Top {levels} bid/ask levels")
    print(f"  Source : Binance WebSocket (live)")
    print("=" * 55)
    print(f"  {'TIME':<10} {'BID VOL':>10} {'ASK VOL':>10} {'RATIO':>7}  SIGNAL")
    print("-" * 55)


def print_snapshot(data: dict):
    """
    Print one line of real-time imbalance data.

    Args:
        data: Output dict from imbalance.calculate_imbalance()
    """
    now = datetime.now().strftime("%H:%M:%S")

    line = (
        f"  {now:<10} "
        f"{data['bid_vol']:>10.4f} "
        f"{data['ask_vol']:>10.4f} "
        f"{data['ratio']:>7.4f}  "
        f"{data['signal']}"
    )
    print(line)
