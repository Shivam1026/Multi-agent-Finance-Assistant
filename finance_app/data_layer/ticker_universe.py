"""
US equity symbol lists from NASDAQ Trader public symbol directories.
"""
from __future__ import annotations

import io
from typing import List

import pandas as pd
import requests

from finance_app.utils.helpers import cache_data

NASDAQ_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/nasdaqlisted.txt"
OTHER_LISTED_URL = "https://www.nasdaqtrader.com/dynamic/SymDir/otherlisted.txt"

# Reasonable fallback if the public feeds are unreachable
_FALLBACK_SYMBOLS: List[str] = [
    "AAPL", "MSFT", "GOOGL", "GOOG", "AMZN", "META", "NVDA", "TSLA", "BRK-B", "JPM",
    "V", "UNH", "JNJ", "WMT", "PG", "MA", "HD", "DIS", "BAC", "ADBE",
    "NFLX", "CRM", "XOM", "CSCO", "PFE", "KO", "PEP", "TMO", "COST", "ABBV",
    "AVGO", "MRK", "ACN", "DHR", "VZ", "WFC", "LIN", "NEE", "PM", "TXN",
    "ORCL", "UPS", "RTX", "HON", "LOW", "IBM", "QCOM", "INTU", "SPGI", "AMAT",
]


def _read_nasdaq_symbols(text: str) -> List[str]:
    out: List[str] = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("File Creation Time"):
            continue
        parts = line.split("|")
        if len(parts) < 2:
            continue
        sym = parts[0].strip().upper()
        if sym == "SYMBOL" or not sym.replace(".", "").replace("-", "").isalnum():
            continue
        out.append(sym)
    return out


def _read_other_symbols(text: str) -> List[str]:
    """Parse otherlisted.txt; first column is ACT Symbol."""
    out: List[str] = []
    for i, line in enumerate(text.splitlines()):
        line = line.strip()
        if not line or line.startswith("File Creation Time"):
            continue
        parts = line.split("|")
        if len(parts) < 2:
            continue
        sym = parts[0].strip().upper()
        if i == 0 and sym == "ACT SYMBOL":
            continue
        if not sym or sym == "ACT SYMBOL":
            continue
        if not sym.replace(".", "").replace("-", "").isalnum():
            continue
        out.append(sym)
    return out


@cache_data(ttl=86_400)
def fetch_us_listed_equity_symbols() -> List[str]:
    """
    Merge NASDAQ-listed and other-exchange symbols (NYSE, etc.) from NASDAQ Trader.
    Returns sorted unique symbols.
    """
    symbols: set[str] = set()
    for url, parser in (
        (NASDAQ_LISTED_URL, _read_nasdaq_symbols),
        (OTHER_LISTED_URL, _read_other_symbols),
    ):
        r = requests.get(url, timeout=45)
        r.raise_for_status()
        symbols.update(parser(r.text))
    return sorted(symbols)


def get_us_equity_symbols() -> List[str]:
    try:
        return fetch_us_listed_equity_symbols()
    except Exception:
        return sorted(_FALLBACK_SYMBOLS)
