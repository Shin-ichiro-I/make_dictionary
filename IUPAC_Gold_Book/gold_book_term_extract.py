import requests
import json
import os

# 保存先ディレクトリ
output_dir = 'goldbook_data'
os.makedirs(output_dir, exist_ok=True)

# 全用語の情報の取得
response = requests.get("https://goldbook.iupac.org/terms/index/all/json/")
terms_data = response.json()

# 各用語について
for term_id, term_info in terms_data["terms"]["list"].items():
    url = f"https://goldbook.iupac.org/terms/view/{term_id}/xml/download"
    response = requests.get(url)

    # XMLファイルへの保存
    file_path = os.path.join(output_dir, f"{term_id}.xml")
    with open(file_path, 'wb') as f:
        f.write(response.content)

print("完了しました。")