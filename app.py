import json
from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_trainers')
def generate_html():
    with open('sample-ELITE4.json', 'r', encoding='utf-8') as f:
        dummy_data = json.load(f)

    spreadsheet_id = dummy_data['spreadsheet_id']
    sheet_name = dummy_data['sheet_name']
    data = dummy_data['data']

    # データをテンプレートに渡してレンダリング
    return render_template('result.html', data=data)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/generate_html', methods=['POST'])


def generate_html_tables(trainer_data):
    # トレーナーデータに基づくHTMLテーブルを生成
    html_output = "<table>"
    for index, row in trainer_data.iterrows():
        html_output += "<tr>"
        for val in row:
            html_output += f"<td>{val}</td>"
        html_output += "</tr>"
    html_output += "</table>"
    return html_output
if __name__ == '__main__':
    app.run(debug=True)
