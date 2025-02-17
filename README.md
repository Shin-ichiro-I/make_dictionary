# make_dictionary
Powered by Gemini 2.0 Flash

## data source
 - Wikidata

## functional design
1. 辞書のスコープ：高分子化学に特化する（のちに有機化学、無機化学などに拡張）
2. Wikidataから抽出するデータ：
    - 化学物質の名称（日本語、英語の両方）
    - 化学物質の同義語、類義語（慣用句とIUPAC名も類義語とみなす）
    - 上位と下位概念
3. 辞書の形式：JSON形式
4. データ抽出・加工ツール：Python
5. 類義語の定義
    - wdt:P460 (類義語): 最も直接的な類義語を表すプロパティです。
    - wdt:P1889 (同義語): ほぼ同じ意味を持つ語を表します。
    - wdt:P1424 (別名): 異なる名称で呼ばれる場合に使われます。慣用名、略称、商品名なども含まれる可能性があります。
    - wdt:P1709 (ブランド): 商品名を表します。高分子材料の商品名も含まれる可能性があります。
    - IUPAC名と慣用名は、同じ物質を指す場合は類義語とみなす。
    - 略称は、正式名称の類義語とみなす。
    - 商品名は、正式名称(または慣用名)の類義語とみなす。
6. クエリ
```
SELECT ?item ?label_ja ?label_en ?altLabel_ja ?altLabel_en ?synonym_ja ?synonym_en ?hypernym ?hyponym ?iupac_name_ja ?iupac_name_en WHERE {
  ?item wdt:P279 wd:Q11344 . # 化学物質

  # 日本語の名称
  OPTIONAL { ?item rdfs:label ?label_ja . FILTER (LANG(?label_ja) = "ja") } 

  # 英語の名称
  OPTIONAL { ?item rdfs:label ?label_en . FILTER (LANG(?label_en) = "en") } 

  # 日本語の別名
  OPTIONAL { ?item skos:altLabel ?altLabel_ja . FILTER (LANG(?altLabel_ja) = "ja") } 

  # 英語の別名
  OPTIONAL { ?item skos:altLabel ?altLabel_en . FILTER (LANG(?altLabel_en) = "en") } 

  # 日本語の類義語
  OPTIONAL { ?item wdt:P460 ?synonym_ja . FILTER (LANG(?synonym_ja) = "ja") } 
  OPTIONAL { ?item wdt:P1889 ?synonym_ja . FILTER (LANG(?synonym_ja) = "ja") } 
  OPTIONAL { ?item wdt:P1424 ?synonym_ja . FILTER (LANG(?synonym_ja) = "ja") } 
  OPTIONAL { ?item wdt:P1709 ?synonym_ja . FILTER (LANG(?synonym_ja) = "ja") } 

  # 英語の類義語
  OPTIONAL { ?item wdt:P460 ?synonym_en . FILTER (LANG(?synonym_en) = "en") } 
  OPTIONAL { ?item wdt:P1889 ?synonym_en . FILTER (LANG(?synonym_en) = "en") } 
  OPTIONAL { ?item wdt:P1424 ?synonym_en . FILTER (LANG(?synonym_en) = "en") } 
  OPTIONAL { ?item wdt:P1709 ?synonym_en . FILTER (LANG(?synonym_en) = "en") } 

  OPTIONAL { ?item wdt:P279 ?hypernym . } # 上位概念
  OPTIONAL { ?item wdt:P279 ?hyponym . } # 下位概念

  # IUPAC名 (日本語)
  OPTIONAL {
    ?item wdt:P231 ?cas_number . # CAS登録番号を取得
    ?iupac_item wdt:P231 ?cas_number ; # 同じCAS登録番号を持つアイテムを検索
                rdfs:label ?iupac_name_ja . # IUPAC名を取得
    FILTER (LANG(?iupac_name_ja) = "ja")
  }

  # IUPAC名 (英語)
  OPTIONAL {
    ?item wdt:P231 ?cas_number . # CAS登録番号を取得
    ?iupac_item wdt:P231 ?cas_number ; # 同じCAS登録番号を持つアイテムを検索
                rdfs:label ?iupac_name_en . # IUPAC名を取得
    FILTER (LANG(?iupac_name_en) = "en")
  }
}
```  
