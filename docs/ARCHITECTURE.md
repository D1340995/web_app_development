# 系統架構文件：食譜收藏夾系統

## 1. 技術架構說明

本專案採用典型的 Web 應用程式架構，前端由伺服器端渲染，後端負責業務邏輯與資料存取。

- **選用技術與原因**：
  - **後端：Python + Flask**。Flask 是一個輕量級的微框架，適合快速開發 MVP，並且有極高的靈活性。
  - **模板引擎：Jinja2**。內建於 Flask 中，能夠將後端資料安全、動態地渲染到 HTML 頁面上，無需額外建立前端應用程式框架。
  - **資料庫：SQLite (透過 sqlite3 或 SQLAlchemy)**。內建於 Python 且無需額外架設資料庫伺服器，非常適合輕量級應用與初期開發。

- **Flask MVC 模式說明**：
  雖然 Flask 原生不強迫使用特定的架構模式，但我們將採用類似 MVC (Model-View-Controller) 的概念來組織程式碼：
  - **Model (資料庫模型)**：負責定義資料結構（如：食譜、使用者、收藏紀錄）並處理與 SQLite 資料庫的溝通。
  - **View (視圖/模板)**：由 Jinja2 負責，負責呈現 HTML 畫面給使用者。
  - **Controller (路由)**：由 Flask 的 Route 負責，接收瀏覽器的請求 (Request)，向 Model 查詢或更新資料，然後將結果交給 View 進行渲染。

## 2. 專案資料夾結構

為了讓程式碼好維護，我們將專案結構劃分如下：

```text
web_app_development/
├── app/                      ← 應用程式主目錄
│   ├── models/               ← 資料庫模型 (Model)
│   │   ├── __init__.py
│   │   ├── recipe.py         ← 食譜相關資料表定義與操作
│   │   └── user.py           ← 使用者與收藏相關資料表定義與操作
│   ├── routes/               ← Flask 路由 (Controller)
│   │   ├── __init__.py
│   │   ├── recipe_routes.py  ← 食譜 CRUD、搜尋、推薦路由
│   │   └── user_routes.py    ← 收藏與使用者相關路由
│   ├── templates/            ← Jinja2 HTML 模板 (View)
│   │   ├── base.html         ← 基礎共用模板（含導覽列、頁首尾）
│   │   ├── index.html        ← 首頁（含推薦食譜）
│   │   ├── recipe_list.html  ← 食譜列表與搜尋結果
│   │   ├── recipe_detail.html← 單一食譜頁面（含材料與步驟）
│   │   └── recipe_form.html  ← 新增/編輯食譜表單
│   └── static/               ← 靜態資源檔案
│       ├── css/
│       │   └── style.css     ← 樣式表
│       ├── js/
│       │   └── main.js       ← 互動指令碼
│       └── images/           ← 網站圖片與使用者上傳圖片
├── instance/                 ← 運行時產生的檔案
│   └── database.db           ← SQLite 資料庫檔案
├── docs/                     ← 專案文件
│   ├── PRD.md                ← 產品需求文件
│   └── ARCHITECTURE.md       ← 系統架構文件
├── requirements.txt          ← Python 依賴套件清單
└── app.py                    ← 專案入口點（啟動 Flask 伺服器）
```

## 3. 元件關係圖

以下是系統運作的元件關係圖，顯示了資料如何從資料庫傳遞到使用者的瀏覽器。

```mermaid
graph TD
    Browser[瀏覽器 (使用者)] -->|發送 HTTP Request| Route(Flask Route Controller)
    Route -->|查詢 / 更新資料| Model(Model 資料庫模型)
    Model -->|讀寫| DB[(SQLite 資料庫)]
    DB -->|回傳資料| Model
    Model -->|回傳資料物件| Route
    Route -->|將資料傳入模板| View(Jinja2 模板)
    View -->|渲染 HTML| Route
    Route -->|回傳 HTTP Response| Browser
```

## 4. 關鍵設計決策

1. **不採用前後端分離，直接使用 Jinja2 渲染**：
   考量到這是個 MVP 專案，且重點在於食譜資料的呈現與搜尋，使用 Flask 搭配 Jinja2 可以大幅減少前端開發的時間，並簡化部署流程，適合初期的快速迭代。
2. **採用 SQLite 作為資料庫**：
   本系統預計初期為個人或小型社群使用，資料量不大且寫入頻率適中。SQLite 無需安裝與設定資料庫伺服器，直接以單一檔案 (`database.db`) 儲存，備份與遷移都非常方便。
3. **路由與模型拆分**：
   為了避免將所有程式碼寫在單一的 `app.py` 中造成維護困難，我們特別將專案拆分出 `models/` 與 `routes/` 資料夾。未來若要新增功能（如新增食材管理、會員系統等），只需在對應資料夾新增檔案即可，達到關注點分離（Separation of Concerns）。
4. **統一定義 base.html**：
   在 `templates/` 中建立一個 `base.html` 作為母版，統一全站的 header (如搜尋列) 與 footer。其他頁面只要繼承此模板即可，不僅減少重複程式碼，也能確保各頁面風格的一致性。
