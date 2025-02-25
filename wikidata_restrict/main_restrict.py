import requests
import pandas as pd
from time import sleep, time
import logging
import argparse

# セッションの作成
session = requests.Session()

# ログ設定
logging.basicConfig(filename='wikidata_download_polymer_restrict.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# SPARQL クエリでアイテムのリストを取得
def get_item_list(offset, limit=100):

    query = f"""
    SELECT?item WHERE {{
    ?item wdt:P279/wdt:P279* wd:Q81163.  # 高分子
    }}
    ORDER BY?item
    LIMIT {limit}
    OFFSET {offset}
    """
    url = 'https://query.wikidata.org/sparql'
    headers = {
        'User-Agent': 'MyMakeDic/1.0 (s_imai@eaglys.co.jp)'
    }
    params = {
        'query': query,
        'format': 'json'
    }
    try:
        response = requests.get(url, headers=headers, params=params)  # セッションを使用
        response.raise_for_status()
        data = response.json()
        item_ids = [item['item']['value'].split('/')[-1] for item in data['results']['bindings']]
        return item_ids
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

# Wikidata API でアイテムの詳細情報を取得
def get_item_data(item_ids):
    url = 'https://www.wikidata.org/w/api.php'
    params = {
        'action': 'wbgetentities',
        'ids': '|'.join(item_ids),  # 複数のIDを|で区切って指定
        'languages': 'ja|en',
        'props': 'labels|aliases|claims',
        'format': 'json'
    }
    try:
        response = requests.get(url, params=params)  # セッションを使用
        response.raise_for_status()
        data = response.json()
        result = {} # 結果を格納する辞書
        for item_id in item_ids: # item_idsの各要素に対して処理
            if item_id in data['entities']: # item_idが存在するか確認
                result[item_id] = data['entities'][item_id]
        return result # 辞書を返す
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Wikidataから高分子データをダウンロードし、CSVファイルに保存する')
    parser.add_argument('start_index', type=int, help='開始位置')
    parser.add_argument('end_index', type=int, help='終了位置')
    args = parser.parse_args()

    start_index = args.start_index  # 開始位置
    end_index = args.end_index  # 終了位置
    step = 20000  # 1回の処理で取得するアイテム数
    limit = 100 # SPARQLクエリのLIMIT
    offset = start_index - 1  # オフセットを開始位置から計算
    file_count = start_index // step + 1  # ファイル番号を開始位置から計算
    max_count = 114867 # 全アイテム数1148676を上限に設定

    while offset <= end_index:  # end_index を上限として繰り返す
        all_data = []
        start_time = time()

        # 指定された範囲のアイテムIDを取得
        item_ids = get_item_list(offset, limit)

        while item_ids:
            for i in range(0, len(item_ids), 50):
                batch_ids = item_ids[i:i + 50]
                item_data = get_item_data(batch_ids)
                if item_data:
                    for item_id, data in item_data.items():
                        # 必要な情報を抽出
                        if 'ja' in data.get('aliases', {}):  # 修正箇所
                            altLabel_ja = [alias['value'] for alias in data['aliases']['ja']]
                        else:
                            altLabel_ja = []
                        if 'en' in data.get('aliases', {}):  # 修正箇所
                            altLabel_en = [alias['value'] for alias in data['aliases']['en']]
                        else:
                            altLabel_en = []

                        instance_of_list = []
                        claims_p31 = data.get('claims', {}).get('P31')
                        if claims_p31:
                            for claim in claims_p31:
                                instance_of_list.append(claim.get('mainsnak', {}).get('datavalue', {}).get('value', {}).get('id'))

                        all_data.append([
                            'http://www.wikidata.org/entity/' + item_id,
                            data['labels'].get('ja', {}).get('value'),
                            data['labels'].get('en', {}).get('value'),
                            altLabel_ja,  # 修正箇所
                            altLabel_en,  # 修正箇所
                            instance_of_list  # instance of のリストを追加
                        ])

                        # step件ごとにCSVファイル出力
                        if len(all_data) >= step:
                            df = pd.DataFrame(all_data, columns=[
                                "item", "label_ja", "label_en", "altLabel_ja", "altLabel_en", "instance of"
                            ])
                            csv_filename = f"chemical_data_api_Q81163_高分子_{file_count * step - step + 1}-{file_count * step}.csv"
                            df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
                            all_data = [] # all_dataをリセット
                            file_count += 1  # ファイル番号をインクリメント

            elapsed_time = time() - start_time
            logging.info(f"処理済みアイテム数: {len(all_data)}, 経過時間: {elapsed_time:.2f}秒")
            sleep(0.1)

            # 次のアイテムIDを取得
            offset += limit
            offset = min(offset, end_index)  # offset が end_index を超えないように制限
            item_ids = get_item_list(offset, limit)

        # 残りのデータをCSVファイル出力
        if all_data:
            df = pd.DataFrame(all_data, columns=[
                "item", "label_ja", "label_en", "altLabel_ja", "altLabel_en", "instance of"  # 追加した情報のカラム名
            ])
            csv_filename = f"wikidata_restrict/chemical_data_api_Q81163_高分子_{file_count * step - step + 1}-{file_count * step}.csv"
            df.to_csv(csv_filename, index=False, encoding="utf-8-sig")
            all_data =[] # all_dataをリセット
            file_count += 1  # ファイル番号をインクリメント

            # 次の範囲を設定
            start_index = end_index + 1
            end_index = min(start_index + step - 1, max_count)  # 上限を超えないように調整
            offset = start_index - 1  # offsetを更新
            file_count = start_index // step + 1  # ファイル番号を更新