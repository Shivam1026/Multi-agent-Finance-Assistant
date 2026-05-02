import yfinance as yf
import pandas as pd
import json
from typing import Optional, Dict, Any
from finance_app.utils.helpers import cache_instance

def get_stock_history(ticker: str, period: str = "1mo", interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical stock data for a given ticker with in-memory caching.
    """
    cache_key = f"hist:{ticker}:{period}:{interval}"
    cached_data = cache_instance.get(cache_key)
    
    if cached_data:
        # Convert dict back to DataFrame
        return pd.DataFrame.from_dict(cached_data)

    stock = yf.Ticker(ticker)
    hist = stock.history(period=period, interval=interval)
    
    # Store in cache as dict (TTL: 1 hour)
    cache_instance.set(cache_key, hist.to_dict(), ttl=3600)
    
    return hist

def get_ticker_info(ticker: str) -> Dict[str, Any]:
    """
    Fetch general information about the company/ticker with in-memory caching.
    """
    cache_key = f"info:{ticker}"
    cached_data = cache_instance.get(cache_key)
    
    if cached_data:
        return cached_data

    stock = yf.Ticker(ticker)
    info = stock.info
    
    # Store in cache (TTL: 24 hours)
    cache_instance.set(cache_key, info, ttl=86400)
    
    return info

def get_stock_news(ticker: str) -> list:
    """
    Fetch recent news related to the ticker with in-memory caching.
    """
    cache_key = f"news:{ticker}"
    cached_data = cache_instance.get(cache_key)
    
    if cached_data:
        return cached_data

    stock = yf.Ticker(ticker)
    news = stock.news
    
    # Store in cache (TTL: 1 hour)
    cache_instance.set(cache_key, news, ttl=3600)
    
    return news

if __name__ == "__main__":
    # Quick test
    ticker_symbol = "AAPL"
    print(f"Fetching data for {ticker_symbol}...")
    history = get_stock_history(ticker_symbol, period="5d")
    print("History Sample:")
    print(history.head())
    
    info = get_ticker_info(ticker_symbol)
    print(f"Sector: {info.get('sector')}")
    
    news = get_stock_news(ticker_symbol)
    print(f"Number of news items: {len(news)}")
