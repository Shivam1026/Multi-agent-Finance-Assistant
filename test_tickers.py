import pandas as pd
import requests

def test_fetch():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    try:
        # Wikipedia requires a user-agent header sometimes
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        tables = pd.read_html(response.text)
        df = tables[0]
        print(f"Success! Fetched {len(df)} tickers.")
        print(df.head())
    except Exception as e:
        print(f"Failed with error: {e}")

if __name__ == "__main__":
    test_fetch()
