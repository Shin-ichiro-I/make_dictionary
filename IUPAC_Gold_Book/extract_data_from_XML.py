import xml.etree.ElementTree as ET
import os
import json

def extract_term_info(xml_file):
    """
    XML ファイルを解析し、用語の情報を抽出する関数

    Args:
        xml_file: XML ファイルのパス

    Returns:
        用語の情報の辞書
    """

    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()

        term_info = {}

        # code 要素から用語 ID を取得
        term_info["id"] = root.find(".//code").text
        # title 要素から用語名を取得
        term_info["title"] = root.find(".//title").text

        # definitions/item/text 要素
        definition_elems = root.findall(".//definitions/item/text")
        if definition_elems:
            term_info["definitions"] = [elem.text.strip() for elem in definition_elems if elem.text]
        else:
            term_info["definitions"] = []

        # altLabel 要素
        term_info["altLabels"] = [elem.text.strip() for elem in root.findall(".//altLabel") if elem.text]

        # relatedTerm 要素
        term_info["relatedTerms"] = [elem.text.strip() for elem in root.findall(".//relatedTerm") if elem.text]

        # chemicals 要素
        term_info["chemicals"] = []
        for chemical_elem in root.findall(".//chemicals/item"):
            chemical_info = {
                "type": chemical_elem.find("type").text.strip() if chemical_elem.find("type").text else None,
                "title": chemical_elem.find("title").text.strip() if chemical_elem.find("title").text else None,
                "file": chemical_elem.find("file").text.strip() if chemical_elem.find("file").text else None
            }
            term_info["chemicals"].append(chemical_info)

        # abbrevs 要素
        term_info["abbrevs"] = [elem.text.strip() for elem in root.findall(".//abbrevs/item") if elem.text]

        # contains/span 要素
        contains_elem = root.find(".//contains")
        if contains_elem is not None:
            term_info["contains"] = [elem.text.strip() for elem in contains_elem.findall("./span") if elem.text]
        else:
            term_info["contains"] = []

        # synonyms 要素
        term_info["synonyms"] = [elem.text.strip() for elem in root.findall(".//synonyms/item") if elem.text]

        # contexts 要素
        term_info["contexts"] = []
        for context_elem in root.findall(".//contexts/*"):
            context_type = context_elem.tag
            context_text = [elem.text.strip() for elem in context_elem.findall(".//item") if elem.text]
            term_info["contexts"].append({context_type: context_text})

        # math 要素
        term_info["math"] = []
        for math_elem in root.findall(".//math/item"):
            math_info = {
                "alttext": math_elem.find("alttext").text.strip() if math_elem.find("alttext").text else None,
                "latex": math_elem.find("latex").text.strip() if math_elem.find("latex").text else None
            }
            term_info["math"].append(math_info)

        # symbols 要素
        term_info["symbols"] = [elem.text.strip() for elem in root.findall(".//symbols/item") if elem.text]

        # processes 要素
        term_info["processes"] = [elem.text.strip() for elem in root.findall(".//processes/item") if elem.text]

        # seealso 要素
        term_info["seealso"] = [elem.text.strip() for elem in root.findall(".//seealso/item") if elem.text]

        # history 要素
        term_info["history"] = []
        for history_elem in root.findall(".//history/item"):
            history_info = {
                "date": history_elem.find("date").text.strip() if history_elem.find("date").text else None,
                "text": history_elem.find("text").text.strip() if history_elem.find("text").text else None
            }
            term_info["history"].append(history_info)

        # haspart 要素
        term_info["haspart"] = [elem.text.strip() for elem in root.findall(".//haspart/item") if elem.text]

        # notes 要素
        term_info["notes"] = [elem.text.strip() for elem in root.findall(".//notes/item") if elem.text]

        return term_info

    except ET.ParseError:
        print(f"Error: Could not parse XML file {xml_file}")
        return None

# XML ファイルが保存されているディレクトリ
xml_dir = 'goldbook_data'

# 抽出した情報を保存する JSON ファイル
output_file = 'goldbook_terms.json'

# 各 XML ファイルについて
term_data = []
for filename in os.listdir(xml_dir):
    if filename.endswith(".xml"):
        xml_file = os.path.join(xml_dir, filename)
        term_info = extract_term_info(xml_file)

        if term_info:
            term_data.append(term_info)

# 抽出した情報を JSON ファイルに保存
with open(output_file, 'w', encoding='utf-8') as f:
    json.dump(term_data, f, ensure_ascii=False, indent=2)

print(f"抽出した情報を {output_file} に保存しました。")