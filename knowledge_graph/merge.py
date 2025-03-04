import json
import pandas as pd

# Gold BookのJSONファイルを読み込む
with open("C:/Users/LPC_0099/Documents/python_program/make_dictionary/IUPAC_Gold_Book/goldbook_terms.json", "r", encoding="utf-8") as f:
    goldbook_data = json.load(f)

# WikidataのCSVファイルを読み込む
wikidata_df = pd.read_csv("C:/Users/LPC_0099/Documents/python_program/make_dictionary/wikidata_restrict/chemical_data_api_Q81163_高分子_1-20000.csv")
wikidata_df = wikidata_df.drop_duplicates(subset='item', keep='first')  # 重複するレコードがあれば削除
wikidata_df = wikidata_df[wikidata_df['label_en'].notna()]

# ナレッジグラフのデータを格納するリスト
knowledge_graph = []

# Gold Bookの各エントリについて
for gb_entry in goldbook_data:
    gb_title = gb_entry["title"]
    # Wikidataでlabel_enが一致するエントリを検索
    wd_entry = wikidata_df[wikidata_df["label_en"] == gb_title]
    # 一致するエントリがあれば統合
    if len(wd_entry) > 0:
        knowledge_graph.append({
            "@id": wd_entry["item"].iloc[0],  # WikidataのIDを優先
            "title": gb_title,
            "definitions": gb_entry.get("definitions", []),
            # Wikidataのlabel_ja, altLabel_ja, altLabel_enを追加
            "label_ja": wd_entry["label_ja"].values[0] if pd.notna(wd_entry["label_ja"].values[0]) else "",
            "altLabel_ja": wd_entry["altLabel_ja"].values[0] if pd.notna(wd_entry["altLabel_ja"].values[0]) else "",
            "altLabel_en": wd_entry["altLabel_en"].values[0] if pd.notna(wd_entry["altLabel_en"].values[0]) else "",
            # その他のGold Bookの情報を追加
            "id": gb_entry["id"],
            "altLabels": gb_entry.get("altLabels", []),
            "relatedTerms": gb_entry.get("relatedTerms", []),
            "chemicals": gb_entry.get("chemicals", []),
            "abbrevs": gb_entry.get("abbrevs", []),
            "contains": gb_entry.get("contains", []),
            "synonyms": gb_entry.get("synonyms", []),
            "contexts": gb_entry.get("contexts", []),
            "math": gb_entry.get("math", []),
            "symbols": gb_entry.get("symbols", []),
            "processes": gb_entry.get("processes", []),
        })
    # 一致するエントリがなければGold Bookのエントリを追加
    else:
        knowledge_graph.append({
            "@id": gb_entry["id"],
            "title": gb_title,
            "definitions": gb_entry.get("definitions", []),
            # Gold Bookにエントリがないlabel_ja, altLabel_ja, altLabel_enは空で追加
            "label_ja": "",
            "altLabel_ja": "",
            "altLabel_en": "",
            # その他のGold Bookの情報を追加
            "altLabels": gb_entry.get("altLabels", []),
            "relatedTerms": gb_entry.get("relatedTerms", []),
            "chemicals": gb_entry.get("chemicals", []),
            "abbrevs": gb_entry.get("abbrevs", []),
            "contains": gb_entry.get("contains", []),
            "synonyms": gb_entry.get("synonyms", []),
            "contexts": gb_entry.get("contexts", []),
            "math": gb_entry.get("math", []),
            "symbols": gb_entry.get("symbols", []),
            "processes": gb_entry.get("processes", []),
        })

# WikidataのエントリでGold Bookにないものを追加
for index, wd_row in wikidata_df.iterrows():
    wd_label = wd_row["label_en"]
    # Gold Bookのtitleに一致するエントリがないか確認
    if not any(gb_entry["title"] == wd_label for gb_entry in goldbook_data):
        knowledge_graph.append({
            "@id": wd_row["item"],
            "title": wd_label,
            "definitions": "",  # wikidataにエントリがないので空で追加
            # Wikidataのlabel_ja, altLabel_ja, altLabel_enを追加
            "label_ja": wd_row["label_ja"] if pd.notna(wd_row["label_ja"]) else "",
            "altLabel_ja": wd_row["altLabel_ja"] if pd.notna(wd_row["altLabel_ja"]) else "",
            "altLabel_en": wd_row["altLabel_en"] if pd.notna(wd_row["altLabel_en"]) else "",
            # その他でGold BookにはあってWikidataにない項目は空で追加
            "id": "",
            "altLabels": "",
            "relatedTerms": "",
            "chemicals": "",
            "abbrevs": "",
            "contains": "",
            "synonyms": "",
            "contexts": "",
            "math": "",
            "symbols": "",
            "processes": "",
        })

# JSON-LD形式で保存
with open("knowledge_graph_test.jsonld", "w", encoding="utf-8") as f:
    json.dump(knowledge_graph, f, ensure_ascii=False, indent=2)