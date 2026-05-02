import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Multi-Agent Finance Assistant", layout="wide")

st.title("🤖 Multi-Agent Financial Assistant")
st.markdown("---")

st.caption("Disclaimer: This tool provides mathematical trends and AI-generated insights. It is NOT financial advice.")




@st.cache_data
def get_all_tickers():
    """Fetches a list of S&P 500 tickers from Wikipedia for the dropdown."""
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    try:
        # Wikipedia requires a user-agent to prevent blocking
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        # Use StringIO to wrap the html string as pandas recommends
        from io import StringIO
        tables = pd.read_html(StringIO(response.text))
        df = tables[0]
        
        # Combine Symbol and Name (Security) for a better user experience
        tickers = (df['Symbol'] + " - " + df['Security']).tolist()
        return sorted(tickers)
    except Exception as e:
        # Fallback list if the request fails
        return sorted([
            "AAPL - Apple Inc.", "MSFT - Microsoft Corp.", "GOOGL - Alphabet Inc.", 
            "AMZN - Amazon.com Inc.", "TSLA - Tesla Inc.", "NVDA - NVIDIA Corp.",
            "META - Meta Platforms", "BRK-B - Berkshire Hathaway", "UNH - UnitedHealth Group",
            "JNJ - Johnson & Johnson", "V - Visa Inc.", "WMT - Walmart Inc.",
            "JPM - JPMorgan Chase", "PG - Procter & Gamble", "MA - Mastercard Inc.",
            "DIS - Walt Disney Co.", "HD - Home Depot", "CVX - Chevron Corp.",
            "BAC - Bank of America", "KO - Coca-Cola Co.", "PEP - PepsiCo Inc."
        ])

# Sidebar for inputs
with st.sidebar:
    st.header("Settings")
    
    all_stocks = get_all_tickers()
    selected_stock = st.selectbox("Select Ticker Symbol", options=all_stocks, index=0)
    
    # Extract the ticker symbol from the selection (e.g., "AAPL" from "AAPL - Apple Inc.")
    ticker = selected_stock.split(" - ")[0]
    
    query = st.text_area("Your Question", placeholder="Should I buy this stock? What are the trends?")
    analyze_button = st.button("Analyze Stock")

if analyze_button:
    if not query:
        st.error("Please enter a question.")
    else:
        with st.spinner(f"Analyzing {ticker}..."):
            try:
                # Call FastAPI backend
                response = requests.post(
                    f"{API_URL}/analyze",
                    json={"query": query, "ticker": ticker}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    
                    # Display Final Response
                    st.subheader("💡 Analysis Summary")
                    st.markdown(data["final_response"])
                    
                    st.markdown("---")
                    
                    # Create columns for details
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        with st.expander("📊 Numerical Analysis"):
                            st.write(data["analysis"])
                        
                        with st.expander("🏢 Company Information"):
                            info = data["ticker_info"]
                            st.write(f"**Name:** {info.get('longName')}")
                            st.write(f"**Sector:** {info.get('sector')}")
                            st.write(f"**Industry:** {info.get('industry')}")
                            st.write(f"**Market Cap:** {info.get('marketCap')}")
                    
                    with col2:
                        st.subheader("📈 Future Price Trend (Prediction)")
                        predicted_prices = data["predicted_prices"]
                        if predicted_prices:
                            # Plotly Chart
                            fig = go.Figure()
                            fig.add_trace(go.Scatter(
                                y=predicted_prices,
                                mode='lines+markers',
                                name='Predicted Price',
                                line=dict(color='firebrick', width=4)
                            ))
                            fig.update_layout(
                                title=f"Next 5 Days Trend for {ticker}",
                                xaxis_title="Days Ahead",
                                yaxis_title="Price ($)",
                                template="plotly_dark"
                            )
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.warning("No prediction data available.")
                            
                else:
                    st.error(f"Error from API: {response.text}")
                    
            except Exception as e:
                st.error(f"Could not connect to backend: {e}")



