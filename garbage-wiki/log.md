# 更新紀錄

## [2026-11-10] setup | 建立 wiki 架構與 SCHEMA
- 決定：以台灣為主、每篇 ingest 前逐一討論、交付網頁版。
- 架構以法定五類為主軸，強制分類三類另頁對照。

## [2026-11-10] ingest | 〔S1〕一般廢棄物回收清除處理辦法
- 新增：S1、cat-bulky、cat-recyclable、cat-hazardous、cat-food、cat-general、concept-legal-categories、law-regulation、local-differences
- 待釐清：第二條廚餘定義有兩種版本寫法。
- 下一篇：環境部回收項目與排出方式。

## [2026-11-10] ingest | 〔S2〕一般廢棄物回收項目排出方式
- 新增：S2；物品群組 9 頁（item-paper、item-iron、item-aluminum、item-glass、item-plastic、item-disc、item-phone、item-cooking-oil、item-mandatory）；易混淆單品 6 頁（item-receipt、item-pressurized-can、item-gas-cylinder、item-plastic-bag、item-styrofoam、item-lithium-battery）；概念 concept-prep
- 更新：cat-recyclable、cat-general、cat-hazardous、cat-food、local-differences、concept-legal-categories、S1、index
- 釐清：S1 廚餘定義的另一寫法為歷史版本用語，⚠ 改為 ✔。
- 補充：S1 第 13 條排出原則。
- 新待釐清：鏡子與陶瓷「不可回收」後的去處（item-glass）；法定有害垃圾的家戶範圍（cat-hazardous）。
- 下一篇：廚餘分類規定。

## [2026-11-10] ingest | 〔S3〕環境部廚餘分類說明、〔S4〕環境部廚餘去化專案報告
- 決定：廚餘拆成兩篇來源；全 wiki 總數定為 5 篇，第 5 篇選較重要的主題。
- 決定：時效性內容新舊規定並列，標明生效期間。
- 新增：S3、S4、item-food-raw-cooked、policy-food-waste-pig
- 改寫：cat-food（改用熟廚餘、生廚餘，舊稱對照）
- 更新：local-differences、index
- 待辦：2027-01-01 後重新 lint policy-food-waste-pig，確認全面禁止已生效。
- 待釐清：縣市廚餘是否仍分生熟收運（目前僅有媒體報導）。

## [2026-11-10] ingest | 〔S5〕居家針頭與廢藥品的處理
- 決定：第 5 篇選居家醫療廢棄物（理由：易混淆物品多已由 S2 涵蓋；有害垃圾頁缺內容；涉及安全）。
- 新增：S5、item-needle、item-medicine
- 改寫：cat-hazardous（改為「法定定義＋實務管道對照表」）
- 更新：item-mandatory、law-regulation（2026-06 廢清法修正、罰則）、local-differences（台北市檢收站）、cat-general、index
- 新舊衝突：針頭處理的環保署舊說法與環境部 2026-09 新說法並列，建議依新說法。
- 新待釐清：中央對廢藥品是否有新規定；廢清法修正案條號與生效日。

## [2026-11-10] lint | 第一次健康檢查
- 程式檢查：斷鏈 0、孤兒頁 0、未列 index 0、無引用頁 0。
- 內容修正：判斷順序中「有害垃圾交專用車」與實務不符，已改寫；concept-prep 補上針頭。
- 待釐清 5 項、時效提醒 2 項、來源品質注意 2 項、覆蓋缺口 3 項，詳見 lint-2026-11-10。

## [2026-11-10] maintenance | raw 檔名改為英數
- 原因：中文檔名在部分解壓縮工具（如 Windows 內建）會顯示為空資料夾或亂碼。
- 變更：S1–S5 的 raw 檔改為英數檔名，wiki 內引用同步更新；內容不變。

## [2026-11-10] maintenance | 新增 AGENTS.md
- 原因：Karpathy 模式的第三層是給代理人的設定檔（AGENTS.md 或 CLAUDE.md）。原本的 SCHEMA.md 只有內容規則，缺少操作步驟。
- 新增：AGENTS.md（必讀檔案、ingest／query／lint 步驟、禁止事項、待辦）
- 修正：scripts/build.py 與 scripts/lint.py 改用相對路徑，在任何電腦解壓縮後都能執行。

## [2026-11-10] maintenance | 依討論改寫 AGENTS.md，實施來源政策
- 決定：在 claude.ai 維護；以上傳的 zip 為準，收工時給 zip 並更新網站。
- 決定：修改分兩級。可直接做：錯字、連結、lint 找到的內容矛盾、有官方依據時 ⚠ 改 ✔。其餘需要同意。
- 決定：新來源只收政府機關原始文件；既有非官方內容保留並標「◇ 非官方」。
- 改寫：AGENTS.md（新增開工與收工流程、兩級修改表、來源政策）
- 更新：SCHEMA.md（第 6 條 ◇ 標記）；lint.py（統計 ◇，健康檢查報告不列入過期字樣檢查）；build.py 與 template.html（◇ 樣式）
- 標記 ◇：cat-hazardous、concept-legal-categories、concept-prep、item-needle、item-medicine、law-regulation、local-differences、S5
- 釐清：S1 條文網址改以環境部主管法規系統為準（✔）。
- 更新：lint-2026-11-10 的來源品質段落。

## [2026-11-10] fix | 廚餘「分類方式不變」的引用錯誤（製作簡報時發現）
- 問題：item-food-raw-cooked 把「生熟分類方式不變」標為 S4，但 S4 未提及；該說法僅見於媒體報導。cat-food、policy-food-waste-pig、local-differences 的「仍分生熟」也把禁令前的 S3 寫成現況。
- 修正（屬可直接做：lint 找到的內容錯誤）：改寫為「禁令前的說明分生熟〔S3〕；禁令後是否調整 ⚠ 依縣市公告」。
