# 總經黑板

個人總體經濟學講義網站，依課堂第三至五章整理十四個核心概念與二十八道自編題目。採深色黑板風格，內容包含概念與生活譬喻、模型假設、公式推導、必要圖形、收合解答、常見錯誤與考前重點。

- GitHub Repository：https://github.com/leelee0608/macro-blackboard
- GitHub Pages：https://leelee0608.github.io/macro-blackboard/
- 發布來源：main 分支、根目錄。網站使用相對路徑，不需要後端。

## 本機預覽與驗證

在專案根目錄執行 `python3 -m http.server 8000`，開啟 `http://localhost:8000`。
執行 `python3 scripts/check.py` 檢查頁面連結、資源、題目收合及數值例題。
`python3 scripts/build.py` 可建立 dist 靜態輸出；GitHub Pages 直接從根目錄發布時不需執行此步驟。

## 檔案結構與後續擴充

- index.html：首頁。
- notes/ch03/、notes/ch04/ 與 notes/ch05/：每個概念一頁的講義。
- assets/css/、assets/js/、assets/figures/ch04/、assets/figures/ch05/：共用樣式、互動及圖形。
- templates/note-template.html：新講義模板；複製至 notes/chNN/ 後再填入內容。
- references/README.md：課堂資料索引。
- AGENTS.md：完整開發與教學規則。CLAUDE.md 指向同一文件。

AI 新增講義前須閱讀 AGENTS.md，重用模板及共用資源，同步更新首頁、相關連結與來源紀錄。上傳時務必保留資料夾層級，不能將子資料夾檔案全部放到根目錄。

## 技術與限制

公式使用瀏覽器原生 MathML Core，設定記於 assets/js/math-config.js，無 CDN 依賴。閱讀紀錄僅儲存在目前瀏覽器。講義是核心概念整理，並非教材逐頁翻譯；原始 PDF 未包含在公開專案。來源頁碼與自編題目標記見各篇講義。

## LLM Wiki 作業（2026-11-21）

主題：為什麼印鈔不一定讓國家更有錢？三份課堂 PDF 與兩篇官方補充，整理為六個概念與十二張教學投影片。

- [Wiki](https://leelee0608.github.io/macro-blackboard/wiki/)
- [教學 HTML 簡報](https://leelee0608.github.io/macro-blackboard/slides/money/)
- [流程、實際檢查與反思](https://leelee0608.github.io/macro-blackboard/wiki/workflow.html)
- [繳交文字](wiki/submission.md)

新增資料：核對原文 → 更新 wiki/knowledge.json 的來源及概念 → 更新 wiki/slide-plan.json → 寫入 wiki/run.json 真實紀錄 → 執行 python3 scripts/build_wiki.py → python3 scripts/check_wiki.py。發布前亦執行原有 scripts/check.py、scripts/build.py。Python 建置重用已整理知識，不會自動呼叫 LLM。原始教材不公開。
