from .recipe_routes import recipe_bp
from .user_routes import user_bp

def register_blueprints(app):
    """將所有的 Blueprint 註冊到 Flask app 中"""
    app.register_blueprint(recipe_bp)
    app.register_blueprint(user_bp)
