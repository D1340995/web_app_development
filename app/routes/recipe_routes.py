from flask import Blueprint

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    GET /
    首頁：顯示首頁內容與最新或推薦的食譜。
    輸出：渲染 index.html
    """
    pass

@recipe_bp.route('/recipes')
def list_recipes():
    """
    GET /recipes
    食譜列表：列出所有食譜，或根據 URL Query Parameter (?q=keyword) 進行搜尋。
    輸出：渲染 recipe_list.html
    """
    pass

@recipe_bp.route('/recipes/new')
def new_recipe_form():
    """
    GET /recipes/new
    新增食譜頁面：顯示供使用者填寫的食譜表單。
    輸出：渲染 recipe_form.html
    """
    pass

@recipe_bp.route('/recipes', methods=['POST'])
def create_recipe():
    """
    POST /recipes
    建立食譜：接收新增表單資料，驗證後存入資料庫。
    輸出：成功則重導向至食譜詳情頁，失敗則重載 recipe_form.html 顯示錯誤訊息。
    """
    pass

@recipe_bp.route('/recipes/<int:recipe_id>')
def recipe_detail(recipe_id):
    """
    GET /recipes/<int:recipe_id>
    食譜詳情：顯示指定 ID 食譜的名稱、材料、步驟與簡介。
    錯誤處理：找不到時回傳 404。
    輸出：渲染 recipe_detail.html
    """
    pass
