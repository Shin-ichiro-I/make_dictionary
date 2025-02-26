# Extract from IUPAC Gold BooK

## Attention

Gold Bookは、化合物名の国際標準を策定している **International Union of Pure and Applied Chemistry (IUPAC)** が編纂していた辞書であるが、2019年以降は改定が行われていないので、注意が必要である。

登録内容に関する信頼性はWikidataよりも高いと思われるが、収録内容に抜け漏れが多く、辞書としての使い勝手はWikidataよりも悪い。

従って、Wikidataを補完する目的で利用する。

```
from :https://iupac.org/what-we-do/databases/

IUPAC Gold Book

An interactive version of IUPAC Compendium of Chemical Terminology, informally known as the “Gold Book”. On these pages you will find a new browsable the alphabetical index, several thematic indexes, and a search function. Note that in the current version, the compendium of terms in not up-to-date and the latest IUPAC Recommendations and Colour Books have yet to be incorporated. Each term is correct based upon the source cited in its entry. However, the term’s definition may have since been superseded or may not reflect current chemical understanding. This version, launched July 2019, is the result of an update to the technical underpinnings of the Gold Book website to reflect advances in web technology. IUPAC Divisions are currently reviewing all entries and updates of the content will follow.
```

## Functional Design for Gold Book

1. １語句につき１ファイルとなっているXMLファイルを、全てダウンロードする (7,096ファイル)
2. ダウンロードしたXMLファイルの中身を解析し、必要な項目を抽出
3. 抽出したデータをJSON形式で保存

## Gold BookからのXMLファイル抽出方法（Procedure）

1. ULR直叩きで全用語リストをJSON形式で取得 `https://goldbook.iupac.org/terms/index/all/json/`
2. JSONから`term_id`を抽出
3. `term_id`毎にXMLファイル呼び出してダウンロード `https://goldbook.iupac.org/terms/view/{term_id}/xml/download`

## XMLファイルから必要項目を抽出する方法

省略
