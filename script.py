import requests
import os
from dotenv import load_dotenv
import pandas as pd
import time

load_dotenv()
POLYGON_API_KEY = os.getenv("POLYGON_API_KEY")
LIMIT = 1000

def run_stock_job():
    url = f'https://api.polygon.io/v3/reference/tickers?market=stocks&active=true&order=asc&limit={LIMIT}&sort=ticker&apiKey={POLYGON_API_KEY}'
    response = requests.get(url)
    response.raise_for_status()  # stop if API fails
    data = response.json()
    
    tickers = list(data.get('results', []))

    while 'next_url' in data:
        print('Requesting next page:', data['next_url'])
        response = requests.get(data['next_url'] + f'&apiKey={POLYGON_API_KEY}')
        response.raise_for_status()
        data = response.json()
        tickers.extend(data.get('results', []))
        print(f'Fetched {len(tickers)} tickers so far...')

        # Wait 12–15 seconds to avoid hitting free tier rate limit
        time.sleep(15)


    # Convert to pandas DataFrame
    df = pd.DataFrame(tickers)

    # Save to CSV
    output_csv = 'tickers.csv'
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f'Wrote {len(df)} rows to {output_csv} using pandas')

if __name__ == '__main__':
    run_stock_job()
