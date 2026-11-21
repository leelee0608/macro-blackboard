"""Render the persisted Wiki and derive the slide deck from its concept blocks.
No API key required. Source ingestion/interpretation is performed by the LLM workflow;
this renderer reproduces the reviewed publication, it does not pretend to ingest anew.
"""
from pathlib import Path
import json,html
R=Path(__file__).resolve().parents[1];W=R/'wiki'
data=json.loads((W/'knowledge.json').read_text());run=json.loads((W/'run.json').read_text());plan=json.loads((W/'slide-plan.json').read_text())
S={x['id']:x for x in data['sources']};C={x['id']:x for x in data['concepts']}
e=html.escape
def p(t):return '<p>'+e(t)+'</p>'
def ul(xs):return '<ul>'+''.join('<li>'+e(x)+'</li>' for x in xs)+'</ul>'
def nav(pre):return f'<nav class="topnav" aria-label="主要導覽"><a class="wordmark" href="{pre}index.html">m. <span>總經黑板 / LLM WIKI</span></a><div><a href="{pre}index.html">知識庫</a><a href="{pre}workflow.html">流程與紀錄</a><a href="{pre}../slides/money/index.html">教學簡報</a></div></nav>'
def shell(title,body,pre='./'):
 return f'<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}｜總經 Wiki</title><link rel="stylesheet" href="{pre}wiki.css"></head><body><a class="skip" href="#main">跳至內容</a>{nav(pre)}<main id="main" class="wrap">{body}</main><footer class="wrap foot">來源可追溯，假設要說明。<br>更新 2026-11-21 · 原始課堂 PDF 未公開 · <a href="{pre}../index.html">返回總經講義網站</a></footer></body></html>'
def source_links(ids,pre='../'):return ' · '.join(f'<a href="{pre}sources/{sid.lower()}.html">{sid} {e(S[sid]["title"])}</a>' for sid in ids)
for s in S.values():
 b=f'<div class="eyebrow">SOURCE NOTE / {s["id"]} / {s["kind"]}</div><h1>{e(s["title"])}</h1><p class="lead">{e(s["summary"])}</p><dl>'
 for key,label in [('filename','資料名稱'),('author','作者／提供方式'),('date','日期'),('locator','實際採用位置'),('method','取得與核對方式')]:b+=f'<dt>{label}</dt><dd>{e(str(s[key]))}</dd>'
 if 'sha256' in s:b+=f'<dt>原始檔指紋 SHA-256</dt><dd class="hash">{s["sha256"]}</dd><dt>完整檔案頁數</dt><dd>{s["pages"]} 頁</dd>'
 b+='</dl><h2>解讀邊界</h2>'+p(s['limit'])
 if s.get('url'):b+=f'<p><a class="button" href="{s["url"]}">開啟官方原文</a></p>'
 b+='<h2>這份資料更新了哪些概念？</h2><div class="links">'+''.join(f'<a href="../concepts/{cid}.html">{e(C[cid]["title"])}</a>' for cid in s['concepts'])+'</div><p class="muted">摘要為 AI 整理；只有列出的段落／頁碼被用於本次教學，未宣稱逐字 ingest 全部資料。</p>'
 (W/'sources'/f'{s["id"].lower()}.html').write_text(shell(s['title'],b,'../'))
for c in C.values():
 b=f'<div class="eyebrow">CONCEPT / 綜合概念筆記</div><h1>{e(c["title"])}</h1><p class="lead">{e(c["question"])}</p><section><h2>核心解釋</h2>{p(c["claim"])}</section><section class="callout"><h2>生活譬喻</h2>{p(c["analogy"])}<p class="muted">譬喻與模型限制：{e(c["limit"])}</p></section><h2>教學素材</h2>'
 for k,v in c['blocks'].items():
  if k in ('main','body','points'):continue
  b+=(ul(v) if isinstance(v,list) else p(v))
 b+='<h2>來源依據</h2><p>'+source_links(c['sources'])+'</p><p class="muted">S01–S03 為課堂資料；S04–S05 為課外補充。生活譬喻、線性圖與數值為自編，不是老師指定題目。</p><h2>相鄰概念</h2><div class="links">'+''.join(f'<a href="{cid}.html">{e(C[cid]["title"])}</a>' for cid in c['related'])+'</div>'
 indices=[str(i+1) for i,s in enumerate(plan) if c['id'] in s['concepts']]
 b+=f'<h2>簡報如何使用這一頁？</h2><p>對應第 {"、".join(indices)} 張投影片。</p><a class="button" href="../../slides/money/index.html#slide-{indices[0]}">查看教學簡報</a>'
 (W/'concepts'/f'{c["id"]}.html').write_text(shell(c['title'],b,'../'))
rows=''.join(f'<tr><td><a href="sources/{s["id"].lower()}.html">{s["id"]}</a></td><td>{e(s["title"])}</td><td>{s["kind"]}</td><td>{e(s["locator"])}</td></tr>' for s in S.values())
b='<div class="eyebrow">A LIVING NOTEBOOK / 貨幣、物價與總供給</div><h1>把五份資料，<br>連成一個能解釋的答案。</h1><p class="lead">為什麼印鈔不一定讓國家更有錢？<br>先分清名目金額、實質資源與時間，再談政策效果。</p><div class="actions"><a class="button" href="../slides/money/index.html">開始教學簡報</a><a href="workflow.html">查看一次實際執行</a></div><div class="metrics"><span><b>5</b> 已整理來源</span><span><b>6</b> 相連概念</span><span><b>12</b> 教學投影片</span></div><h2>從問題走進 Wiki</h2><label class="search-label">搜尋概念 <input id="wiki-search" type="search" placeholder="例如：短期、物價、銀行"></label><p id="wiki-status" class="muted" aria-live="polite">顯示 6 個概念</p><div class="concept-grid">'
for c in C.values():b+=f'<a class="concept-card" href="concepts/{c["id"]}.html"><span>{e(c["question"])}</span><h3>{e(c["title"])}</h3><p>{e(c["blocks"]["body"])}</p><small>來源：{" · ".join(c["sources"])}</small></a>'
b+='</div><h2>來源索引：不是五段剪貼</h2><p>每份資料有獨立摘要、採用位置與限制；概念頁整合多份資料，簡報再引用概念頁。</p><div class="table-scroll"><table><thead><tr><th>ID</th><th>資料</th><th>分類</th><th>採用位置</th></tr></thead><tbody>'+rows+'</tbody></table></div><h2>這個 Wiki 如何繼續累積？</h2><p>新增資料時，先搜尋既有概念。若已有同一概念，就補充來源、假設或修正，不重複新增另一份孤立摘要。修正 Wiki 後，重新檢查引用它的投影片。</p><p>本次由對話中的 AI 進行整理與核對，再用 Python 建置。網站是靜態成果，沒有自動讀取新 PDF 或即時呼叫 LLM 的後端。</p><div class="links"><a href="knowledge.json">可重用知識資料 JSON</a><a href="slide-plan.json">簡報查詢對照</a><a href="run.json">本次執行紀錄 JSON</a><a href="workflow.html">流程與反思</a></div>'
index=shell('貨幣、物價與總供給',b).replace('</body>','<script src="wiki.js"></script></body>');(W/'index.html').write_text(index)
# Real observations; no invented student feedback or autonomous retrieval claims.
issues=''.join(f'<article class="issue"><span class="eyebrow">{x["id"]} / {x["node"]}</span><h3>{e(x["observed"])}</h3>{p(x["action"])}<p class="status">{x["status"]}</p></article>' for x in run['issues'])
ing=''.join(f'<tr><td>{x["source"]}</td><td>{e(x["status"])}</td><td>{e("、".join(x["new_concepts"]) or "—")}</td><td>{e("、".join(x["updated_concepts"]) or "—")}</td></tr>' for x in run['ingestion'])
b='<div class="eyebrow">WORKFLOW / '+run['id']+'</div><h1>先核對，再入庫。<br>讓錯誤停在簡報之前。</h1><p class="lead">五份來源分批整理，合併成六個概念，再查詢 Wiki 產生十二張教學投影片。</p><h2>先討論、後生成</h2>'+ul(run['discussion'])+'<h2>這次實際採用的 graph</h2><ol class="workflow"><li>取得資料<br><small>課堂 PDF + 官方文章</small></li><li>檢查擷取<br><small>公式、圖軸、頁碼、假設</small></li><li>查詢並更新 Wiki<br><small>概念去重、保留來源</small></li><li>查詢 Wiki 生成簡報<br><small>依 slide-plan.json 取用概念</small></li><li>檢查與發布<br><small>內容、計算、引用、操作</small></li></ol><div class="callout"><h3>哪些步驟會重複？</h3><p>每一份來源都重複「取得 → 核對 → 查詢 → 更新」。公式或假設出錯，退回來源核對；文字太難或版面有誤，只重做教學編排與 HTML。修正概念時，重新生成引用它的投影片。</p></div><h2>實際 ingestion 紀錄</h2><div class="table-scroll"><table><thead><tr><th>來源</th><th>狀態</th><th>新增概念</th><th>補充既有概念</th></tr></thead><tbody>'+ing+'</tbody></table></div><h2>本次觀察與處理</h2>'+issues+'<h2>檢查前移：原流程與修訂流程</h2><p><strong>原先討論的概略流程：</strong>'+e(' → '.join(run['workflow_before']))+'</p><p><strong>本次實際修訂：</strong>'+e(' → '.join(run['workflow_after']))+'</p><h2>反思</h2><p>本次教學內容中，資料擷取節點有兩項明確缺漏（R01、R02），另有一項假設需要補明（R03）。因此把公式與圖軸檢查，從最後的簡報審查前移到 Wiki 入庫前。本次只有一次執行，不能推論所有任務中哪個節點最常出錯；下載遭拒則是取得工具的限制，與概念正確性分開記錄。</p><p>這樣設計，是因為錯誤一旦寫入 Wiki，會被多張投影片重複引用。先檢查來源，能避免後面整份重改。尚未收到使用者閱讀初稿後的回饋，不宣稱已完成真人學習成效測試。</p><h2>驗證紀錄</h2><div id="verification">'+(ul(run['verification']) if run['verification'] else p('內容已完成核對；程式及瀏覽器驗證執行後將更新本節。'))+'</div><h2>可重現的範圍</h2><p>執行 python3 scripts/build_wiki.py 可從已整理的 knowledge.json 與 slide-plan.json 重建網站；python3 scripts/check_wiki.py 檢查來源與頁面連結。這些程式不會重新呼叫 LLM，因此可重現建置與檢查，不是重現一次新的 AI 推理。</p><div class="links"><a href="run.json">執行紀錄</a><a href="submission.md">作業繳交文字</a></div>'
(W/'workflow.html').write_text(shell('流程與檢查紀錄',b))
# Teaching deck. Content blocks come from the persisted concepts above.
def block(cid,k='body'):return e(C[cid]['blocks'][k])
def sources_for(ids):return sorted(set(s for c in ids for s in C[c]['sources']))
def trace(ids):return '<div class="trace">Wiki 依據：'+ ' · '.join(f'<a href="../../wiki/concepts/{cid}.html">{e(C[cid]["title"])}</a>' for cid in ids)+'</div>'
def eq():return '<math xmlns="http://www.w3.org/1998/Math/MathML" display="block"><mrow><mi>M</mi><mi>V</mi><mo>=</mo><mi>P</mi><mi>Y</mi></mrow></math>'
# Accurate, synthetic AD/AS coordinates: Y 70..145, P 60..160.
def graph():
 x=lambda Y:70+(Y-70)*6;y=lambda P:360-(P-60)*3
 s='<svg id="as-chart" viewBox="0 0 620 420" role="img" aria-labelledby="chart-title chart-desc"><title id="chart-title">一次需求擴張的短期與長期效果</title><desc id="chart-desc">初始 A：產出100物價100；短期 B：產出110物價110；長期 C：產出100物價120。紫色 LRAS 固定於產出100。自編線性模型。</desc><path d="M70 40V360H560" stroke="#94a8b5" fill="none"/><g fill="#a7bac6" font-size="15"><text x="15" y="30">P 指數</text><text x="345" y="410">Y 每期產出單位</text>'
 for Y in [80,100,120,140]:s+=f'<text x="{x(Y)}" y="383" text-anchor="middle">{Y}</text>'
 for P in [80,100,120,140]:s+=f'<path d="M70 {y(P)}H550" stroke="#293c44"/><text x="60" y="{y(P)+5}" text-anchor="end">{P}</text>'
 s+='</g>'
 for cls,pts,col,dash in [('original-ad',[(70,130),(140,60)],'#769f9f',''),('new-ad',[(70,150),(145,75)],'#5eead4',''),('original-as',[(70,70),(145,145)],'#fde68a',''),('new-as',[(70,90),(140,160)],'#fde68a','stroke-dasharray="8 6"')]:s+=f'<path class="{cls}" d="M{x(pts[0][0])} {y(pts[0][1])}L{x(pts[1][0])} {y(pts[1][1])}" stroke="{col}" stroke-width="3" fill="none" {dash}/>'
 s+=f'<path d="M{x(100)} 40V360" stroke="#b4a4f4" stroke-width="2"/><text x="{x(100)-18}" y="25" fill="#b4a4f4" font-size="15">LRAS</text>'
 for i,(Y,P) in enumerate(C['short-and-long-run']['blocks']['points']):s+=f'<g class="point point-{i}"><circle cx="{x(Y)}" cy="{y(P)}" r="6" fill="#e8edf2"/><text x="{x(Y)+12}" y="{y(P)-10}" fill="#e8edf2" font-size="17">{"ABC"[i]} ({Y}, {P})</text></g>'
 s+='</svg>';return s
slides=[]
for i,item in enumerate(plan,1):
 id=item['id'];ids=item['concepts'];inside=''
 if id=='opening':
  inside='<div class="split cover"><div><div class="kicker">一堂給非經濟系的貨幣課</div><h1>為什麼印鈔<br><em>不一定</em>讓國家<br>更有錢？</h1><p class="intro">把「錢變多」和「生活變好」，<br>分開想清楚。</p><p class="muted">5 份來源 · 約 8–10 分鐘 · 無須總經基礎</p></div><div class="cover-art" aria-label="名目金額增加不等於實際產出增加"><div class="bill"><span>帳戶數字</span><strong>× 2</strong></div><div class="not-equal">≠</div><div class="goods"><span>實際商品與服務</span><strong>× 2 ?</strong></div><p>真正的問題是：<br>我們能生產與買到多少？</p></div></div>'
 elif id=='shop':
  inside='<h2>餐券多一倍，<br>便當就多一倍嗎？</h2><div class="split"><div><p class="big">'+block('money-and-wealth','example')+'</p><p>'+block('money-and-wealth','body')+'</p><p class="muted">譬喻限制：餐券不是完整貨幣制度，價格與生產在現實中都可能調整。</p></div><div class="number-panel"><span>今天的供應</span><strong>100<span>份便當</span></strong><hr><span>明天多印餐券</span><strong class="yellow">200<span>張餐券</span></strong><p>多出的，是請求購買的工具。</p></div></div>'
 elif id=='creation':inside='<h2>'+block('money-creation','main')+'</h2><p class="big">'+block('money-creation')+'</p><div class="balance"><div><span>存款資產</span><strong>＋10 萬</strong></div><div><span>借款負債</span><strong>＋10 萬</strong></div><div><span>當下淨資產變化</span><strong>0</strong></div></div><p>'+block('money-creation','example')+'</p><p class="muted">'+block('money-creation','caution')+'</p>'
 elif id=='equation':inside='<h2>'+block('quantity-equation','main')+'</h2><div class="split"><div><div class="formula">'+eq()+'</div><p>'+block('quantity-equation')+'</p><p class="muted">M：貨幣存量；V：每期流通速度；P：價格；Y：每期實質產出。V = PY/M 是定義，不是因果證明。</p></div><div class="lab"><label for="money">貨幣 M：<output id="money-value">1,000</output> 元</label><input id="money" type="range" min="1000" max="2000" step="100" value="1000"><label for="output">產量 Y：<output id="output-value">100</output> 份／期</label><input id="output" type="range" min="100" max="200" step="10" value="100"><div class="result" aria-live="polite">每份價格 <strong id="price">10.00</strong> 元</div><button id="reset-lab" type="button">重設數值</button><p class="muted">自編示例，固定 V = 1。這是條件式計算，不是預測。</p></div></div>'
 elif id=='demand':inside='<h2>如果不能憑空致富，<br>為什麼還要貨幣政策？</h2><p class="big">'+block('policy-and-demand')+'</p><ol class="chain">'+''.join('<li>'+e(x)+'</li>' for x in C['policy-and-demand']['blocks']['chain'])+'</ol><p class="muted">'+block('policy-and-demand','caution')+'</p>'
 elif id=='sticky':inside='<h2>'+block('sticky-adjustment','main')+'</h2><p class="big">'+block('sticky-adjustment')+'</p><div class="compare"><div><span>合約簽訂時</span><strong>100 ÷ 1 = 100</strong><p>名目工資 ÷ 物價 = 實質工資</p></div><div><span>物價上升，合約尚未改</span><strong>100 ÷ 1.25 = 80</strong><p>實質工資下降 20%</p></div></div><p class="muted">自編數值，固定技術、名目工資，可調整僱用。'+block('sticky-adjustment','caution')+'</p>'
 elif id=='graph':inside='<h2>同一次需求擴張，<br>三個時間點。</h2><div class="split"><div class="chart" data-stage="0">'+graph()+'<p class="legend">青綠：AD　黃：SRAS　紫：LRAS<br>虛線：調整後 SRAS；圖依自編方程式繪製。</p></div><div><div class="stage-controls" aria-label="時間點"><button data-stage="0" aria-pressed="true">初始 A</button><button data-stage="1" aria-pressed="false">短期 B</button><button data-stage="2" aria-pressed="false">長期 C</button></div><p id="stage-text" class="big" aria-live="polite">初始：Y = 100，P = 100</p><p id="stage-explain">需求與供給在自然產出交會。</p><details><summary>查看自編模型與條件</summary><p>'+block('short-and-long-run','assumptions')+'</p></details></div></div>'
 elif id=='longrun':inside='<h2>'+block('short-and-long-run','main')+'</h2><p class="big">'+block('short-and-long-run')+'</p><div class="resources"><div><strong>設備</strong><span>資本</span></div><div><strong>人力</strong><span>勞動</span></div><div><strong>做法</strong><span>技術</span></div></div><p class="muted">課堂長期基準；不宣稱所有理論與情境皆排除政策的長期效果。自然產出不是物理最大產量。</p>'
 elif id=='pitfalls':inside='<h2>回答之前，<br>先分清這三件事。</h2><div class="distinctions"><div><h3>錢的種類</h3><p>現鈔、銀行存款、央行準備金，不能當作同一變數。</p></div><div><h3>水準或變動率</h3><p>P = 120 是物價指數，不是通膨率 120%。一次漲價不等於持續加速通膨。</p></div><div><h3>短期或長期</h3><p>「短期可能增產」與「長期不能只靠名目擴張致富」可以同時成立。</p></div></div>'
 elif id=='quiz':
  qs=[('錢多一倍，物價一定翻倍？','不一定。在交換方程式中還要確認 V、Y；只有它們固定，才可推出同比例變動。'),('借到 10 萬元，淨資產就增加 10 萬元？','不對。當下同時增加存款資產與借款負債，不是憑空增加淨資產。'),('長期產出回到自然水準，代表短期政策完全無用？','不代表。短期可能影響需求、就業及產出；長期模型結論不能取代短期分析。')]
  inside='<h2>先自己回答，<br>再打開解答。</h2><div class="quiz">'+''.join('<article><h3>'+e(q)+'</h3><details><summary>查看解答</summary>'+p(a)+'</details></article>' for q,a in qs)+'</div><p class="muted">自編理解檢查；不是老師考古題。</p>'
 elif id=='recap':inside='<div class="kicker">現在，重新回答開場問題</div><h2>錢能推動交易，<br><em>不能替代生產能力。</em></h2><p class="big">貨幣政策可能在短期影響需求與產出；但在本課堂長期基準下，單靠增加貨幣，不能保證永久增加實際商品與服務。</p><div class="callout"><h3>試著用自己的話說</h3><p>假設朋友說：「政府多印鈔，大家就不用工作了。」你會怎麼用餐券、短期調整與生產能力三個概念回應？</p></div>'
 elif id=='trace':inside='<h2>不是直接把 PDF，<br>換成投影片。</h2><p class="big">5 份來源 → 6 個相連概念 → 12 張教學投影片</p><p>每張投影片底部都能回到 Wiki 概念頁，再追到來源與採用位置。來源變動時，先修 Wiki，再重新檢查簡報。</p><div class="actions"><a class="button" href="../../wiki/index.html">開啟 LLM Wiki</a><a class="button secondary" href="../../wiki/workflow.html">檢查紀錄與反思</a></div><p class="muted">課堂資料：S01 貨幣與物價、S02 IS–LM 與總需求、S03 總供給。<br>課外補充：S04 英格蘭銀行、S05 美國聯準會。<br>本次為對話式 LLM 工作流程；網站不會自動 ingest 新資料。</p>'
 slides.append(f'<section class="slide" id="slide-{i}" aria-label="第 {i} 張：{e(item["label"])}"><div class="slide-inner"><div class="slide-label">{i:02} / {e(item["label"])}</div>{inside}{trace(ids)}</div></section>')
select='<select id="slide-select" aria-label="跳至投影片">'+''.join(f'<option value="{i}">{i:02} {e(s["label"])}</option>' for i,s in enumerate(plan,1))+'</select>'
ht='<!doctype html><html lang="zh-Hant"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="以五份來源建立的總經 LLM Wiki 教學簡報，理解貨幣、購買力與短長期產出。"><title>印鈔能讓國家更有錢嗎？｜總經教學簡報</title><link rel="stylesheet" href="slides.css"><script defer src="slides.js"></script></head><body><a class="skip" href="#slides">跳至簡報</a><header class="deck-header"><a href="../../wiki/index.html">m. <span>總經黑板 · 教學簡報</span></a><div><button id="all-slides">閱讀全部</button><button id="print">列印 / 存成 PDF</button></div></header><main id="slides">'+''.join(slides)+'</main><footer class="deck-controls"><button id="prev" aria-label="上一張投影片">上一張</button>'+select+'<span id="position" aria-live="polite">1 / 12</span><button id="next" aria-label="下一張投影片">下一張</button><progress id="progress" max="12" value="1" aria-label="簡報進度"></progress></footer><noscript><p>JavaScript 未啟用，已顯示全部投影片；互動試算需啟用 JavaScript。</p></noscript></body></html>'
(R/'slides/money/index.html').write_text(ht)
(W/'submission.md').write_text('''# 政大 ［請填學號］ 風保二 王育安 貨幣、物價與總供給

## 1. LLM Wiki 主題與簡介
以「為什麼印鈔不一定讓國家更有錢？」為教學問題，整合三份課堂 PDF 與兩篇官方補充資料，建立六個相互連結的概念頁。對象是未學過總經的大學生。

## 2. LLM Wiki
https://leelee0608.github.io/macro-blackboard/wiki/

## 3. 教學 HTML 簡報
https://leelee0608.github.io/macro-blackboard/slides/money/

## 4. loop / graph
取得資料 → 檢查擷取、公式、圖軸與假設 → 查詢既有概念並更新 Wiki → 查詢 Wiki 形成簡報 → 內容與網頁檢查 → 發布。
每篇來源重複取得與核對；知識問題退回來源／Wiki，表達或排版問題退回簡報。這是對話式 LLM 整理加上程式建置，沒有宣稱部署了自動呼叫 LLM 的後端。

## 5. 實際執行結果
五份來源已整理成來源筆記，六個概念頁含來源與相關概念連結；依 Wiki 產生十二張 HTML 投影片。
實際檢查紀錄：https://leelee0608.github.io/macro-blackboard/wiki/workflow.html

## 6. 反思
本次資料擷取發現兩項教學資訊缺漏：第五章第 37 頁公式沒有出現在擷取文字中，第 14、39 頁圖形座標也未被擷取。另補明交換方程式推出比例關係所需的假設。因此把公式、圖軸及假設的檢查前移到 Wiki 入庫之前，避免錯誤再被多張投影片引用。本次只有一次執行，不能據此推論長期錯誤頻率；尚未完成真人學習成效測試。
''')
print('Built 5 source pages, 6 concept pages, Wiki, workflow and 12-slide deck')
