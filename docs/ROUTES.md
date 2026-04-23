# 路由設計文件：食譜收藏夾系統

本文件基於 PRD、架構與資料庫設計，規劃了系統的 URL 路由、HTTP 方法、處理邏輯與對應的 Jinja2 模板。

## 1. 路由總覽表格

| 功能 | HTTP 方法 | URL 路徑 | 對應模板 | 說明 |
| :--- | :--- | :--- | :--- | :--- |
| **首頁** | GET | `/` | `index.html` | 顯示首頁內容，包含隨機/最新食譜推薦 |
| **食譜列表/搜尋** | GET | `/recipes` | `recipe_list.html` | 列出所有食譜，或依關鍵字顯示搜尋結果 |
| **新增食譜頁面** | GET | `/recipes/new` | `recipe_form.html` | 顯示新增食譜的表單 |
| **建立食譜** | POST | `/recipes` | — | 接收新增表單，存入 DB，成功後重導向 |
| **食譜詳情** | GET | `/recipes/<int:recipe_id>` | `recipe_detail.html` | 顯示單筆食譜的詳細內容（材料與步驟） |
| **切換收藏狀態** | POST | `/recipes/<int:recipe_id>/collect` | — | 將食譜加入收藏或取消收藏，成功後重導向 |
| **我的收藏夾** | GET | `/collections` | `collections.html` | 列出使用者已收藏的所有食譜 |
| **建立使用者(測試用)**| POST | `/users` | — | (MVP 開發用) 簡單建立預設使用者 |

## 2. 每個路由的詳細說明

### 首頁 (`GET /`)
- **輸入**: 無
- **處理邏輯**: 呼叫 `Recipe.get_all()` 取得最新食譜。
- **輸出**: 渲染 `index.html`，傳入 `recipes` 資料。

### 食譜列表/搜尋 (`GET /recipes`)
- **輸入**: URL Query Parameter `?q=keyword` (可選)
- **處理邏輯**: 檢查是否有 `q` 參數。若有，呼叫 `Recipe.search(keyword)`；若無，呼叫 `Recipe.get_all()`。
- **輸出**: 渲染 `recipe_list.html`，傳入 `recipes` 與 `search_query`。

### 新增食譜頁面 (`GET /recipes/new`)
- **輸入**: 無
- **處理邏輯**: 無。
- **輸出**: 渲染 `recipe_form.html`。

### 建立食譜 (`POST /recipes`)
- **輸入**: 表單欄位 `title`, `description`, `ingredients`, `steps`
- **處理邏輯**: 驗證必填欄位。呼叫 `Recipe.create(...)` 存入資料庫。
- **輸出**: 成功則重導向到 `/recipes/<recipe_id>`；失敗則重新渲染 `recipe_form.html` 並顯示錯誤訊息。

### 食譜詳情 (`GET /recipes/<int:recipe_id>`)
- **輸入**: `recipe_id` (從 URL 取得)
- **處理邏輯**: 呼叫 `Recipe.get_by_id(recipe_id)`。若找不到則回傳 404。需判斷當下使用者是否已收藏此食譜。
- **輸出**: 渲染 `recipe_detail.html`，傳入 `recipe` 與 `is_collected`。

### 切換收藏狀態 (`POST /recipes/<int:recipe_id>/collect`)
- **輸入**: `recipe_id` (從 URL 取得), `action` (表單隱藏欄位，值為 'add' 或 'remove')
- **處理邏輯**: 取得目前使用者 ID。根據 `action` 呼叫 `Collection.add()` 或 `Collection.remove()`。
- **輸出**: 成功後重導向回 `/recipes/<recipe_id>`。

### 我的收藏夾 (`GET /collections`)
- **輸入**: 無
- **處理邏輯**: 取得目前使用者 ID。呼叫 `Collection.get_user_collections(user_id)`。
- **輸出**: 渲染 `collections.html`，傳入 `collected_recipes`。

## 3. Jinja2 模板清單

所有模板皆存放在 `app/templates/` 資料夾下，並統一繼承 `base.html` 以共用導覽列。

- `base.html`: 基礎骨架，包含 HTML head、共用 CSS/JS 引入、導覽列與頁腳。
- `index.html`: 首頁，顯示推薦食譜與搜尋框。
- `recipe_list.html`: 食譜清單與搜尋結果。
- `recipe_detail.html`: 顯示材料、步驟與收藏按鈕。
- `recipe_form.html`: 新增食譜的表單。
- `collections.html`: 顯示已收藏食譜列表。
