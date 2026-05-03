"""
test_imbalance.py
-----------------
Unit tests for the core imbalance calculation logic.

Run with:  python -m pytest tests/ -v
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from imbalance import calculate_imbalance


# ── Helpers ───────────────────────────────────────────────────────────────────

def make_levels(qty: float, n: int = 10) -> list:
    """Create N fake order book levels each with the given quantity."""
    return [["50000.00", str(qty)] for _ in range(n)]


# ── Tests ─────────────────────────────────────────────────────────────────────

def test_buy_pressure():
    """Heavy bids → ratio > 0.6 → BUY PRESSURE signal."""
    bids = make_levels(9.0)   # 9 units per level × 10 = 90 total
    asks = make_levels(1.0)   # 1 unit  per level × 10 = 10 total
    # ratio = 90 / (90 + 10) = 0.9

    result = calculate_imbalance(bids, asks)

    assert result["ratio"] > 0.6
    assert "BUY" in result["signal"]


def test_sell_pressure():
    """Heavy asks → ratio < 0.4 → SELL PRESSURE signal."""
    bids = make_levels(1.0)
    asks = make_levels(9.0)
    # ratio = 10 / (10 + 90) = 0.1

    result = calculate_imbalance(bids, asks)

    assert result["ratio"] < 0.4
    assert "SELL" in result["signal"]


def test_neutral():
    """Equal bids and asks → ratio ≈ 0.5 → NEUTRAL signal."""
    bids = make_levels(5.0)
    asks = make_levels(5.0)
    # ratio = 50 / 100 = 0.5

    result = calculate_imbalance(bids, asks)

    assert 0.4 <= result["ratio"] <= 0.6
    assert "NEUTRAL" in result["signal"]


def test_empty_book():
    """Empty book should not crash and return ratio = 0.5."""
    result = calculate_imbalance([], [])

    assert result["ratio"] == 0.5
    assert result["bid_vol"] == 0.0
    assert result["ask_vol"] == 0.0


def test_levels_respected():
    """Only top N levels should be used, not all levels."""
    # 20 levels of bids but only 5 of asks at much higher qty
    bids = make_levels(1.0, n=20)
    asks = make_levels(100.0, n=20)

    # With levels=5: bid_vol=5, ask_vol=500 → heavy sell
    result_5 = calculate_imbalance(bids, asks, levels=5)

    # With levels=20: bid_vol=20, ask_vol=2000 → still heavy sell
    result_20 = calculate_imbalance(bids, asks, levels=20)

    # Both should be SELL but ratio should differ based on levels
    assert "SELL" in result_5["signal"]
    assert "SELL" in result_20["signal"]
    # Ratios are the same here (proportional), but the volumes differ
    assert result_5["bid_vol"] == 5.0
    assert result_20["bid_vol"] == 20.0


def test_ratio_range():
    """Ratio must always be between 0 and 1."""
    bids = make_levels(7.3)
    asks = make_levels(2.1)
    result = calculate_imbalance(bids, asks)
    assert 0.0 <= result["ratio"] <= 1.0
