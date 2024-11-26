from bs4 import BeautifulSoup

def generate_html_table(entries):
    """エントリのリストからHTMLテーブルを生成する関数"""
    stylesheet = """
<style>
.table-elite-four {
width: auto; /* ブラウザに合わせて適度に */
max-width: 100%; /* 最大幅を100%に */
border-collapse: collapse;
font-size: 12px; /* テキストサイズを12pxに */
margin: 0 auto; /* 中央揃え */
text-align: center;
}

.table-elite-four th, .table-elite-four td {
border: 1px solid #000; /* 罫線1px */
padding: 8px;
}

.table-elite-four th {
background-color: #ffbd59;
}

.table-elite-four td {
background-color: #fffaf2;
}

td ul {
margin: 0;
padding-left: 0;  /* 左側のパディングをリセット */
list-style-position: inside;  /* リストのマーカー（•など）をテキストの内側に表示 */
}

@media screen and (max-width: 600px) {
.table-elite-four {
width: 100%; /* モバイルでは幅を100%に */
font-size: 10px; /* テキストサイズを小さく */
}

.table-elite-four th, .table-elite-four td {
padding: 4px; /* パディングを小さく */
}
}
</style>
"""
    if not entries:
        return f"<p>データが見つかりませんでした。</p>{stylesheet}"
    
    # HTMLテーブルを生成
    html_output = "<table class='table-elite-four'><tbody>"

    # ポケモン名と性別
    html_output += "<tr>"
    for entry in entries:
        pokemon = entry['ポケモン']
        gender = entry.get('せいべつ', '')
        if gender:
            pokemon += f"({gender})"
        html_output += f"<th><img src='path/to/{pokemon}.png alt='{pokemon}'></th>" # シングルクォートとダブルクォートの組み合わせ
    html_output += "</tr>"

    # ポケモン名と性別（セル内）
    html_output += "<tr>"
    for entry in entries:
        pokemon = entry['ポケモン']
        gender = entry.get('せいべつ', '')
        if gender:
            pokemon += f"({gender})"
        html_output += f"<td>{pokemon}</td>"
    html_output += "</tr>"

    # レベル
    html_output += "<tr>"
    for entry in entries:
        level = entry['レベル']
        html_output += f"<td>{level}</td>"
    html_output += "</tr>"

    # とくせい（なかったら表示しない）
    abilities_exist = any('とくせい' in entry for entry in entries)
    if abilities_exist:
        html_output += "<tr>"
        for entry in entries:
            ability = entry.get('とくせい', '')
            html_output += f"<td>{ability}</td>"
        html_output += "</tr>"

    # わざ
    html_output += "<tr>"
    for entry in entries:
        html_output += "<td><ul>"
        for i in range(1, 5):
            move = entry.get(f'わざ{i}', '')
            if move:
                html_output += f"<li>{move}</li>"
        html_output += "</ul></td>"
    html_output += "</tr>"

    html_output += "</tbody></table>"

    # スタイルシートとテーブルを結合
    full_html_output = f"{html_output}{stylesheet}"

    # BeautifulSoupで整形　prettify()でインデントを整える
    soup = BeautifulSoup(full_html_output, 'html.parser')
    pretty_html_output = soup.prettify()

    return pretty_html_output
