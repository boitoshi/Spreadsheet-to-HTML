from flask import Flask
from app.routes import main_bp # ブループリントの登録

def create_app():
    app = Flask(__name__)
    app.secret_key = 'your_secret_key'  # 必要に応じて設定を読み込む

    app.register_blueprint(main_bp)

    # エラーハンドラの登録
    from app.handlers import register_error_handlers
    register_error_handlers(app)

    return app
