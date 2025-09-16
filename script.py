import os
import requests
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

polygon_api_key = os.getenv("POLYGON_API_KEY")

LIMIT = 1000
base_url = (
    f"https://api.polygon.io/v3/reference/tickers?"
    f"market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={polygon_api_key}"
)


def fetch_all_tickers(api_url: str, api_key: str) -> list[dict]:
    """Fetch all tickers from Polygon API with pagination."""
    tickers = []
    response = requests.get(api_url)
    data = response.json()
    tickers.extend(data.get('results', []))

    while 'next_url' in data:
        next_url = data['next_url'] + f'&apiKey={api_key}'
        response = requests.get(next_url)
        data = response.json()
        tickers.extend(data.get('results', []))

    return tickers


def save_tickers_to_csv(tickers: list[dict], filename: str):
    """Save tickers list of dicts to a CSV file."""
    if not tickers:
        print("No tickers to save.")
        return

    df = pd.DataFrame(tickers)
    df.to_csv(filename, index=False)
    print(f"✅ Saved {len(tickers)} tickers to {filename}")


if __name__ == "__main__":
    all_tickers = fetch_all_tickers(base_url, polygon_api_key)
    print(f"Fetched {len(all_tickers)} tickers")

    # Save to CSV
    save_tickers_to_csv(all_tickers, "tickers.csv")
