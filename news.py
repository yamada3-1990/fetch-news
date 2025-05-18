import requests
from dotenv import load_dotenv
import os
import pandas as pd
from datetime import datetime, timedelta, timezone, date

load_dotenv()
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
headers = {'X-Api-Key': NEWS_API_KEY}
url = 'https://newsapi.org/v2/everything'

def fetch_news_relative(query, days_ago=None):
    search_query = query

    params = {
        'q': search_query,
        'sortBy': 'relevancy',
        'pageSize': 50,
        'excludeDomains': 'itainews.com'
    }

    if days_ago is not None:
        # 現在時刻を取得
        today_utc = datetime.now(timezone.utc).date()
        from_date = today_utc - timedelta(days=days_ago)
        params['from'] = from_date.isoformat()
        params['to'] = datetime.now(timezone.utc).date().isoformat()
    else:
        params['from'] = date.today().isoformat()

    response = requests.get(url, headers=headers, params=params)
    print(response)

    if response.ok:
        data = response.json()
        df = pd.DataFrame(data['articles'])
        print('totalResults:', data['totalResults'])
        # print('DataFrame columns:', df.columns)
        return df
    else:
        print(f"News API エラー: {response.status_code}, {response.text}")
        return pd.DataFrame()
