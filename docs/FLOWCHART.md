# 流程圖文件：線上算命系統

本文件根據 PRD 與系統架構，視覺化了使用者的操作路徑（User Flow）以及系統內部的資料流動歷程（System Sequence Diagram），並附上主要功能的路由設計。

## 1. 使用者流程圖（User Flow）

以下流程圖說明使用者從進入網站開始，可能會經歷的操作路徑：

```mermaid
flowchart LR
    A([使用者造訪首頁]) --> B[首頁介紹與功能選單]
    
    B -->|點擊「開始占卜」| C[占卜/抽籤頁面]
    B -->|點擊「歷史紀錄」| D[歷史紀錄清單頁]
    
    C -->|送出表單/點擊抽籤| E[等待動畫]
    E -->|後端處理完成| F[展示占卜結果與解析]
    
    F -->|點擊「儲存結果」| G[寫入紀錄]
    G -->|成功提示| F
    
    F -->|點擊「分享結果」| H[複製結果連結或圖文]
    H -->|分享給朋友| F
    
    F -->|點擊「重新占卜」| C
    
    D -->|瀏覽過去紀錄| I[點選單筆紀錄查看詳情]
```

## 2. 系統序列圖（Sequence Diagram）

以下序列圖詳述「使用者執行抽籤並點選儲存」時，系統背後的運作流程：

```mermaid
sequenceDiagram
    actor User as 使用者
    participant Browser as 使用者瀏覽器
    participant Route as Flask Route
    participant Model as Model
    participant DB as SQLite 資料庫

    User->>Browser: 在抽籤頁面點擊「開始抽籤」
    Browser->>Route: POST /divination/draw
    Route->>Route: 執行亂數演算法，抽出對應籤詩/結果
    Route-->>Browser: 回傳包含結果的 HTML 畫面 (Jinja2)
    Browser-->>User: 展示抽籤結果與解析
    
    User->>Browser: 覺得很準，點擊「儲存結果」
    Browser->>Route: POST /divination/save (傳送結果資料)
    Route->>Model: 呼叫 save_history(user_id, result_data)
    Model->>DB: INSERT INTO history 表格 ...
    DB-->>Model: 寫入成功
    Model-->>Route: 寫入成功確認
    Route-->>Browser: 回傳成功狀態 (或重新載入頁面)
    Browser-->>User: 顯示「已成功儲存」提示
```

## 3. 功能清單對照表

根據上述流程與架構需求，系統預計會實作以下對應的 URL 路徑與 HTTP 請求方法：

| 功能名稱 | URL 路徑 | HTTP 方法 | 說明 |
| :--- | :--- | :--- | :--- |
| 首頁 | `/` | GET | 顯示系統介紹、主要功能入口提示 |
| 抽籤/占卜頁面 | `/divination` | GET | 呈現抽籤介面，可加入注意事項或求籤表單 |
| 執行抽籤邏輯 | `/divination/draw` | POST | 接收抽籤請求，進行後端抽籤邏輯並回傳結果 |
| 儲存算命結果 | `/divination/save` | POST | 將使用者想要保留的算命結果寫入歷史紀錄資料庫中 |
| 歷史紀錄頁面 | `/history` | GET | 查詢該使用者過去儲存過的所有結果並列表呈現 |
| 顯示單一結果 | `/result/<id>` | GET | 呈現特定一筆結果資料（可作為「分享算命結果」的共用網址） |
