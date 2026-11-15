# 總經黑板

依第三章「資產市場、貨幣與物價」及第四章「IS–LM 與總需求」製作的個人總經講義網站。深色數位黑板風格，每個核心概念一頁，含譬喻、假設、推導、例題、常見錯誤與考前重點。所有題目答案預設收合。

## 開啟網站

無 npm 或後端依賴。在本資料夾執行 `python3 -m http.server 8000`，瀏覽 `http://localhost:8000`。亦可直接開啟 index.html，完整驗證建議使用 HTTP。

公式直接使用瀏覽器原生 MathML Core，無外部字型或 CDN 依賴。現代瀏覽器支援；過舊瀏覽器可能無法正確排版。`assets/js/math-config.js` 記錄選用方式，共用 CSS 控制顯示。

## 新增講義

1. AI 先讀 AGENTS.md；Claude 可由 CLAUDE.md 進入。
2. 確認章節與來源，複製 templates/note-template.html 至 notes/chNN/英文主題.html。
3. 按模板填入內容，清除所有佔位文字，加入必要圖形；全部詳解使用不帶 open 的 details。
4. 更新首頁卡片、共用側欄（首頁、現有講義與模板）、來源索引、相關概念連結及 CHANGELOG。
5. 執行 `python3 scripts/check.py`，再檢查手機、桌面、MathML 與鍵盤展開。
6. Sites 發布前執行 `python3 scripts/build.py`，靜態輸出為 dist/。源檔位於根目錄，dist 是可重建輸出，不手改。

## GitHub Pages

將本專案根目錄的完整內容上傳至自己的 GitHub 儲存庫，保留 index.html、assets/、notes/、兩份規則與模板的相對位置。以根目錄作為 Pages 發布來源，或在自訂部署流程中發布 dist/。網站目前尚未建立使用者的 GitHub Repository，因此沒有可填報的 GitHub 連結；發布後將真實網址補於本節。

- GitHub Repository：尚未建立。
- GitHub Pages：尚未發布。
- 本次 Sites 發布結果：以交付訊息的實際網址為準。私人網址尚不能當作公開作業網址。

## 範圍與限制

共八篇核心概念、十六道自編題目。是核心整理，並非逐頁翻譯。第三章貨幣總計數統計與第四章各經驗指標尚未逐項製作。

不附原始課堂 PDF；頁面列出來源及頁碼。自編線性模型與數值不冒充教師題目。i/r、P/π、離散精確成長率與近似均有明示。

閱讀紀錄僅存在目前瀏覽器的 localStorage；更換裝置不會同步，已讀不表示已精熟。搜尋在首頁依標題與摘要比對。

## 專案規則與可重用性

AGENTS.md 規範教學結構與修改界線；CLAUDE.md 指向同一規則。八篇講義共用一套 CSS、MathML 設定與題目展開結構。新講義應重用模板而非另造版型。
