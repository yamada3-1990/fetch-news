import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv
import os
import news

# .env ファイルをロード
load_dotenv()
GOOGLE_SHEETS_CREDENTIALS_PATH = os.getenv('GOOGLE_SHEETS_CREDENTIALS_PATH')
GOOGLE_SHEETS_API_KEY = os.getenv('GOOGLE_SHEETS_API_KEY')
SPREADSHEET_ID = os.getenv('SPREADSHEET_ID')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
# GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# 認証スコープ
scope = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

# サービスアカウント用の認証情報ファイルのパス
credentials_file = GOOGLE_SHEETS_CREDENTIALS_PATH
def main():
    # サービスアカウントの認証情報を取得
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_file, scope)

    # Google Sheetsに接続
    gc = gspread.authorize(credentials)

    try:
        # プレッドシートのID
        spreadsheet_key = SPREADSHEET_ID

        # スプレッドシートを開く
        worksheet = gc.open_by_key(spreadsheet_key).sheet1

        query = 'policy OR 日本の政策 OR 政府 政策 日本 OR 行政 政策 日本 OR 海外 政策 OR 国際 政策 OR 米国 政策 OR 中国 政策 OR EU 政策 OR 経済政策 OR 金融政策 OR 財政政策 OR 少子化 OR 少子高齢化 OR 少子化対策'
        df = news.fetch_news_relative(query=query, days_ago=7) # 過去1週間に変更

        print("\n過去1週間のニュース:") 
        if not df.empty:
            for index, row in df.iterrows():
                print(f"タイトル: {row['title']}")
                print(f"概要: {row['description']}")
                print(f"URL: {row['url']}")
                print(f"公開日時: {row['publishedAt']}")
                print("-" * 30)

            # 新しいデータの書き込み
            new_data = []
            for index, row in df.iterrows():
                new_data.append([row['publishedAt'], row['title'], row['description'], row['url']])

            if new_data:
                worksheet.append_rows(new_data)
                print("新しいデータが Google Sheets に追加されました。")
                # print(new_data)
            else:
                print("新しいニュース記事が見つかりませんでした。")

        else:
            print("過去過去1週間のニュースは見つかりませんでした。")

    except Exception as e:
        print("エラーが発生しました:", e)

if __name__ == "__main__":
    main()
