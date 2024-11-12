import json
from flask import Flask, render_template, request, jsonify, flash, redirect, url_for
from markupsafe import Markup
from bs4 import BeautifulSoup
import html


app = Flask(__name__)
app.secret_key = 'your_secret_key'  # フラッシュメッセージのために必要

@app.route('/')
def index():
    try:
        # ダミーデータの読み込み
        with open('sample-ELITE4.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # シート名のリストを取得
        sheet_names = list(data.keys())

    except FileNotFoundError:
        flash('データファイルが見つかりませんでした。')
        return redirect(url_for('index'))
    except json.JSONDecodeError:
        flash('データファイルの読み込みに失敗しました。')
        return redirect(url_for('index'))

    return render_template('index.html', sheet_names=sheet_names)

@app.route('/get_trainers', methods=['POST'])
def get_trainers():
    data = request.get_json()
    sheet_name = request.form['sheet_name']
    try:
        # ダミーデータの読み込み
        with open('sample-ELITE4.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 選択されたシート名に対応するトレーナー名のリストを取得
        trainers = list(set(entry['トレーナー'] for entry in data[sheet_name]))

    except FileNotFoundError:
        return jsonify({'error': 'データファイルが見つかりませんでした。'}), 404
    except json.JSONDecodeError:
        return jsonify({'error': 'データファイルの読み込みに失敗しました。'}), 400

    return jsonify(trainers)

@app.route('/', methods=["GET", "POST"])
def new_index():
    stylesheet = """
<style>
.table-elite-four {
width: auto; /* ブラウザに合わせて適度に */
max-width: 100%; /* 最大幅を100%に */
border-collapse: collapse;
font-size: 12px; /* テキストサイズを12pxに */
margin: 0 auto; /* 中央揃え */
}

.table-elite-four th, .table-elite-four td {
border: 1px solid #000; /* 罫線1px */
padding: 8px;
}

.table-elite-four th {
background-color: #ffbd59;
text-align: center;
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
    try:
        # ダミーデータの読み込み
        with open('sample-ELITE4.json', 'r', encoding='utf-8') as f:
            data = json.load(f)

        # フォームからの入力を取得
        sheet_name = request.form['sheet_name']
        trainer_name = request.form['trainer_name']

        # トレーナー名でフィルタリング
        filtered_data = [entry for entry in data[sheet_name] if entry['トレーナー'] == trainer_name]

        if not filtered_data:
            flash('指定されたトレーナーのデータが見つかりませんでした。')
            return redirect(url_for('index'))

        # HTMLテーブルを生成
        # html_output = f"<h2>{trainer_name}</h2>\n"
        html_output = "<table class='table-elite-four'><tbody>\n"

        # ポケモン名と性別
        html_output += "<tr>\n"
        for entry in filtered_data:
            pokemon = entry['ポケモン']
            gender = entry.get('せいべつ', '')
            if gender:
                pokemon += f" ({gender})"
            html_output += f"    <th><alt='{pokemon}'></th>\n"
        html_output += "</tr>\n"

        # ポケモン名と性別（セル内）
        html_output += "<tr>\n"
        for entry in filtered_data:
            pokemon = entry['ポケモン']
            gender = entry.get('せいべつ', '')
            if gender:
                pokemon += f" ({gender})"
            html_output += f"    <td align='center'>{pokemon}</td>\n"
        html_output += "</tr>\n"

        # レベル
        html_output += "<tr>\n"
        for entry in filtered_data:
            level = entry['レベル']
            html_output += f"    <td align='center'>Lv.{level}</td>\n"
        html_output += "</tr>\n"

        # とくせい（なかったら表示しない）
        abilities_exist = any('とくせい' in entry for entry in filtered_data)
        if abilities_exist:
            html_output += "<tr>\n"
            for entry in filtered_data:
                ability = entry.get('とくせい', '')
                html_output += f"    <td align='center'>{ability}</td>\n"
            html_output += "</tr>\n"

        # わざ
        html_output += "<tr>\n"
        for entry in filtered_data:
            html_output += "    <td><ul>\n"
            for i in range(1, 5):
                move = entry.get(f'わざ{i}', '')
                if move:
                    html_output += f"        <li>{move}</li>\n"
            html_output += "    </ul></td>\n"
        html_output += "</tr>\n"

        html_output += "</tbody></table>\n"

        # BeautifulSoupで整形
        soup = BeautifulSoup(html_output, 'html.parser')
        pretty_html_output = soup.prettify()

    except FileNotFoundError:
        flash('データファイルが見つかりませんでした。')
        return redirect(url_for('index'))
    except json.JSONDecodeError:
        flash('データファイルの読み込みに失敗しました。')
        return redirect(url_for('index'))

    pretty_html_output = pretty_html_output + stylesheet
    return render_template('index.html', html_output=pretty_html_output, sheet_name=sheet_name, trainer_name=trainer_name)

if __name__ == '__main__':
    app.run(debug=True)
