from flask import Blueprint

user_bp = Blueprint('user', __name__)

@user_bp.route('/recipes/<int:recipe_id>/collect', methods=['POST'])
def toggle_collection(recipe_id):
    """
    POST /recipes/<int:recipe_id>/collect
    切換收藏狀態：將指定的食譜加入使用者的收藏夾，或從中移除。
    輸入：表單中可夾帶 action (add 或 remove)。
    輸出：處理完成後重導向回該食譜詳情頁。
    """
    pass

@user_bp.route('/collections')
def my_collections():
    """
    GET /collections
    我的收藏夾：列出目前使用者已收藏的所有食譜。
    輸出：渲染 collections.html
    """
    pass

@user_bp.route('/users', methods=['POST'])
def create_test_user():
    """
    POST /users
    建立使用者(測試用)：快速建立一個預設使用者以便測試收藏功能。
    輸出：重導向回首頁。
    """
    pass
