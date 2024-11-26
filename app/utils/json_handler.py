import json
import os

def load_data(json_file):
    """指定されたJSONファイルを読み込み、データを返す関数"""
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    json_path = os.path.join(root_dir, json_file)
    
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        raise FileNotFoundError(f"ファイルが見つかりません: {json_path}")
    except json.JSONDecodeError:
        raise ValueError(f"JSONの読み込みに失敗しました: {json_path}")

def get_sheet_names(data):
    """データからシート名のリストを取得"""
    return list(data.keys())

def get_trainers(data, sheet_name):
    """指定されたシート名からトレーナー名のリストを取得"""
    if sheet_name in data:
        trainers = list(set(entry['トレーナー'] for entry in data[sheet_name]))
        return trainers
    else:
        return []
    
    # # 重複を除きながら出現順を維持する場合
    # if sheet_name in data:
    #     seen = []
    #     for entry in data[sheet_name]:
    #         if entry['トレーナー'] not in seen:
    #             seen.append(entry['トレーナー'])
    #     return seen
    # else:
    #     return []

def get_entries(data, sheet_name, trainer_name):
    """指定されたシート名とトレーナー名に一致するエントリのリストを取得"""
    if sheet_name in data:
        entries = [entry for entry in data[sheet_name] if entry['トレーナー'] == trainer_name]
        return entries
    else:
        return []
