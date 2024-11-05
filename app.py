from flask import Flask, render_template, request
import pandas as pd
import gspread
from google.auth import default

app = Flask(__name__)

# Google Sheetsの認証
creds, _ = default()
gc = gspread.authorize(creds)

@app.route('/')
def home():
    # スプレッドシートとトレーナーのリストを取得
    spreadsheet_id = request.args.get('spreadsheet_id')
    if spreadsheet_id:
        spreadsheet = gc.open_by_key(spreadsheet_id)
        sheets = spreadsheet.worksheets()
        sheet_names = [sheet.title for sheet in sheets]
    else:
        sheet_names = []
    return render_template('index.html', sheet_names=sheet_names)

@app.route('/get_trainers')
def get_trainers():
    sheet_name = request.args.get('sheet_name')
    spreadsheet_id = request.args.get('spreadsheet_id')
    spreadsheet = gc.open_by_key(spreadsheet_id)
    sheet = spreadsheet.worksheet(sheet_name)
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
    trainers = df['トレーナー'].unique()
    return {'trainers': trainers.tolist()}

@app.route('/generate_html', methods=['POST'])
def generate_html():
    spreadsheet_id = request.form['spreadsheet_id']
    sheet_name = request.form['sheet_name']
    trainer_name = request.form['trainer_name']
    spreadsheet = gc.open_by_key(spreadsheet_id)
    sheet = spreadsheet.worksheet(sheet_name)
    data = sheet.get_all_values()
    df = pd.DataFrame(data[1:], columns=data[0])
     # 選択されたトレーナーのデータをフィルタリング
    trainer_data = df[df['トレーナー'] == trainer_name]
    html_output = generate_html_tables(trainer_data)
    return render_template('result.html', html_output=html_output)

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
