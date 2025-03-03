# Extract from Wikidata

## Functional Design for Wikidata

1. 辞書のスコープ：高分子化学に特化する（のちに有機化学、無機化学などに拡張）
2. Wikidataから抽出するデータ：
    - 化学物質の名称（日本語、英語の両方）
    - 化学物質の同義語、類義語（慣用句とIUPAC名も類義語とみなす）
    - 上位と下位概念
3. 出力する辞書の形式：CSV形式
4. データ抽出・加工ツール：Python

## Wikidataからの抽出手順 (Procedure)

1. SPARQL クエリでアイテムのリストを取得

    ```get_item_list関数
    def get_item_list(offset, limit=100):

        query = f"""
        SELECT?item WHERE {{
        ?item wdt:P279/wdt:P279* wd:Q81163.  # 高分子
        }}
        """
        url = 'https://query.wikidata.org/sparql'
        headers = {
            'User-Agent': 'MyMakeDic/1.0 (xxxxx@xxxxx.co.jp)' #e-mail本物を入力しないとタイムアウトが起こるので注意！
            }
        params = {
            'query': query,
            'format': 'json'
        }
    ```

2. Wikidata APIでアイテムid毎に詳細データを抽出

    ```get_item_data関数
    def get_item_data(item_ids):
        url = 'https://www.wikidata.org/w/api.php'
        params = {
            'action': 'wbgetentities',
            'ids': '|'.join(item_ids),  # 複数のIDを|で区切って指定
            'languages': 'ja|en',
            'props': 'labels|aliases|claims',
            'format': 'json'
        }
    ```  

3. 抽出データをファイルに出力

    ```概略のみ記載
    # 抽出データ項目
    'http://www.wikidata.org/entity/' + item_id,
    data['labels'].get('ja', {}).get('value'),
    data['labels'].get('en', {}).get('value'),
    altLabel_ja = [alias['value'] for alias in data['aliases']['ja']]
    altLabel_en = [alias['value'] for alias in data['aliases']['en']]
    claims_p31 = data.get('claims', {}).get('P31')

    # csvファイルの構成
    df = pd.DataFrame(all_data, columns=[
                            "item", "label_ja", "label_en", "altLabel_ja", "altLabel_en", "instance of"
                        ])

    ```

## Python Execution Command

- データダウンロードに時間がかかるため、分割ダウンロードができる
- `start_index` : 抽出する語句の最初の`index`
- `stop_index` : 抽出を修了する語句の`index`
- データは2万語毎にCSVファイルに出力されるため、`start_index`と`stop_index`の差が、2万の倍数であることが好ましい

```実行コード例
poetry run python main_restrict.py {start_index} {stop_index}
poetry run python main_restrict.py 1 40000
```

### Wikidata収録アイテム数 (2025.02.19)

- Wikidata Query Serviceから検索可能 :https://query.wikidata.org/

```アイテム数カウント用クエリ
SELECT (COUNT(?item) AS ?count) WHERE {
?item wdt:P31/wdt:P279* wd:Q178593 .  # インスタンス(P31)が高分子、またはそのサブクラス(P279)であるアイテムをカウント
}
```

- Q178593 (高分子): 1148429
- Q11173 (化合物)：
- Q35758 (物質)：
- Q214609 (材料)： 1245339
- Q79529 (化学物質)：
- Q11344 (元素)： 369

### Reference

#### SPARQLクエリのプロパティ

```- wdt:P460 (類義語): 最も直接的な類義語を表すプロパティ
- wdt:P1889 (同義語): ほぼ同じ意味を持つ語を表す
- wdt:P1424 (別名): 異なる名称で呼ばれる場合に使われ、慣用名、略称、商品名なども含まれる可能性がある
- wdt:P1709 (ブランド): 商品名を表し、高分子材料の商品名も含まれる可能性がある
- IUPAC名と慣用名は、同じ物質を指す場合は類義語とみなす
- 略称は、正式名称の類義語とみなす
- 商品名は、正式名称(または慣用名)の類義語とみなす

- wdt:P31 :instance of
- wdt:P279 :subclass of```
