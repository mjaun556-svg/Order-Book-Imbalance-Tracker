"""
imbalance.py
------------
Core logic for calculating Order Book Imbalance (OBI).

What is Order Book Imbalance?
  The order book has two sides:
    - Bids: buyers waiting to buy (demand)
    - Asks: sellers waiting to sell (supply)

  Imbalance Ratio = bid_volume / (bid_volume + ask_volume)

  - Ratio > 0.6  → More buyers than sellers → BUY PRESSURE
  - Ratio < 0.4  → More sellers than buyers → SELL PRESSURE
  - Ratio 0.4–0.6 → Balanced market → NEUTRAL

Why does this matter?
  Large imbalance often PRECEDES price movement.
  If bids massively outweigh asks, price tends to rise (and vice versa).
  Market makers and HFT firms use this signal constantly.
"""


def calculate_imbalance(bids: list, asks: list, levels: int = 10) -> dict:
    """
    Calculate order book imbalance from top N price levels.

    Args:
        bids   : List of [price, quantity] pairs (best bid first)
        asks   : List of [price, quantity] pairs (best ask first)
        levels : How many top levels to consider (default: 10)

    Returns:
        Dictionary with bid_vol, ask_vol, ratio, and signal.
    """
    # Slice to top N levels only
    top_bids = bids[:levels]
    top_asks = asks[:levels]

    # Sum up total volume on each side
    # Each entry is [price_str, qty_str] from Binance — convert to float
    bid_volume = sum(float(b[1]) for b in top_bids)
    ask_volume = sum(float(a[1]) for a in top_asks)

    total_volume = bid_volume + ask_volume

    # Avoid division by zero on startup or empty book
    if total_volume == 0:
        return {
            "bid_vol": 0.0,
            "ask_vol": 0.0,
            "ratio": 0.5,
            "signal": "NEUTRAL",
        }

    # Imbalance ratio: closer to 1.0 = all bids, closer to 0.0 = all asks
    ratio = bid_volume / total_volume

    # Classify signal based on thresholds
    if ratio > 0.6:
        signal = "BUY PRESSURE 🟢"
    elif ratio < 0.4:
        signal = "SELL PRESSURE 🔴"
    else:
        signal = "NEUTRAL  ⚪"

    return {
        "bid_vol": round(bid_volume, 4),
        "ask_vol": round(ask_volume, 4),
        "ratio":   round(ratio, 4),
        "signal":  signal,
    }
