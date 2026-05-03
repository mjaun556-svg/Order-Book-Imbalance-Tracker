"""
logger.py
---------
Optional CSV logger — saves every imbalance snapshot to logs/signals.csv.

Useful for:
  - Backtesting: did high imbalance actually predict price movement?
  - Visualisation: plot ratio over time in Excel / matplotlib
  - Portfolio: shows interviewers you think about data persistence
"""

import csv
import os
from datetime import datetime


LOG_DIR  = os.path.join(os.path.dirname(__file__), "..", "logs")
LOG_FILE = os.path.join(LOG_DIR, "signals.csv")

# CSV column headers
HEADERS = ["timestamp", "bid_vol", "ask_vol", "ratio", "signal"]


def init_logger():
    """Create the logs directory and write the CSV header (once)."""
    os.makedirs(LOG_DIR, exist_ok=True)

    # Only write header if the file is new / empty
    if not os.path.exists(LOG_FILE) or os.path.getsize(LOG_FILE) == 0:
        with open(LOG_FILE, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=HEADERS)
            writer.writeheader()


def log_snapshot(data: dict):
    """
    Append one row to the CSV log.

    Args:
        data: Output dict from imbalance.calculate_imbalance()
    """
    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "bid_vol":   data["bid_vol"],
        "ask_vol":   data["ask_vol"],
        "ratio":     data["ratio"],
        # Strip emoji for clean CSV
        "signal":    data["signal"].split(" ")[0],
    }

    with open(LOG_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        writer.writerow(row)
