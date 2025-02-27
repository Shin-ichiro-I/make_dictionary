# Making Original Knowledge Graph

## How to create KG

1. Gold Bookの各エントリについて
    - Wikidataで`label_en`が一致するエントリを検索
      - 一致するエントリがあれば統合
      - 一致するエントリがなければGold Bookのエントリを追加

2. WikidataのエントリでGold Bookにないものを追加
    - Gold Bookの`title`に一致するエントリがないか確認
      - 一致するエントリがなければWikidataのエントリを追加

## Merged Column Name

```
"@id": wd_row["item"],
"title": wd_label,
"definitions": gb_entry.get("definitions", []),
"label_ja": wd_row["label_ja"] if pd.notna(wd_row["label_ja"]) else "",
"altLabel_ja": wd_row["altLabel_ja"] if pd.notna(wd_row["altLabel_ja"]) else "",
"altLabel_en": wd_row["altLabel_en"] if pd.notna(wd_row["altLabel_en"]) else "",
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
```

- wd_row[...] : from Wikidata
- gb_entry.get(...) : from Gold Book
