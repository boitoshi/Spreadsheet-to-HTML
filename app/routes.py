from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from .utils.json_handler import load_data, get_sheet_names, get_trainers, get_entries
from .utils.html_generator import generate_html_table

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def index():
    try:
        # デバッグ用にログを追加
        print("Loading JSON file...")
        data = load_data('sample-ELITE4.json')
        sheet_names = get_sheet_names(data)
        print(f"Sheet names: {sheet_names}")  # デバッグ用
        return render_template('index.html', sheet_names=sheet_names)
    except Exception as e:
        print(f"Error loading JSON: {str(e)}")  # デバッグ用
        flash(f'エラーが発生しました: {str(e)}')
        return redirect(url_for('main.index'))

@main_bp.route('/get_trainers', methods=['POST'])
def get_trainers_route():
    sheet_name = request.form.get('sheet_name')
    if not sheet_name:
        return jsonify({'error': 'シート名が指定されていません。'}), 400
    try:
        sheet_name = request.form.get('sheet_name')
        if not sheet_name:
            return jsonify({'error': 'シート名が指定されていません。'}), 400
            
        data = load_data('sample-ELITE4.json')
        trainers = get_trainers(data, sheet_name)
        
        # デバッグ用ログ
        print(f"Sheet name: {sheet_name}")
        print(f"Trainers: {trainers}")
        
        return jsonify(trainers)
    except Exception as e:
        print(f"Error in get_trainers_route: {str(e)}")
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500

@main_bp.route('/generate_html', methods=['POST'])
def generate_html_route():
    try:
        sheet_name = request.form.get('sheet_name')
        trainer_name = request.form.get('trainer_name')
        
        if not all([sheet_name, trainer_name]):
            return jsonify({'error': 'シート名とトレーナー名は必須です。'}), 400
            
        data = load_data('sample-ELITE4.json')
        entries = get_entries(data, sheet_name, trainer_name)
        html_output = generate_html_table(entries)
        
        return jsonify({'html_output': html_output})
        
    except Exception as e:
        print(f"Error in generate_html: {str(e)}")  # デバッグ用
        return jsonify({'error': f'エラーが発生しました: {str(e)}'}), 500
