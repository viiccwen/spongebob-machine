# 派星機

[zh-tw version](README.md) | [english version](README.en.md)

<p align="center">
   <img src="sharp-head.jpg" width="60%"></img>
</p>

* 跟朋友聊天不知道傳什麼？
* 想要一個比較『懂自己』的派星機？

那你來對了，這是一個基於 **NLP / LLM** 分析使用者輸入語意，跟章魚哥一樣懂你的 [Telegram Bot](https://t.me/spongebob_machine_bot) 🙌

## 使用方式

[馬上加入！](https://t.me/spongebob_machine_bot)

### Bot 指令

- `/start` - 啟動 Bot 並查看歡迎訊息
- `/random` - 隨機獲得一張梗圖

### 互動模式

1. **自由文字輸入**：輸入關鍵字，Bot 會使用相似度搜尋在別名中尋找匹配的梗圖
2. **隨機梗圖**：使用 `/random` 指令獲得隨機梗圖

### 選擇機制

- 當搜尋結果有多張圖片時，Bot 會顯示最多 3 個選項
- 每個選項顯示 `meme_id` 和 `name`
- 使用者可以點擊按鈕選擇想要的圖片
- 如果只有一張圖片，會直接發送

## 搜尋機制

Bot 會進行模糊文字匹配與相似度閾值匹配，根據相似度分數返回最佳匹配的梗圖

## 技術堆疊

- **Bot 框架**: `python-telegram-bot`
- **資料庫**: PostgreSQL + pgvector
- **搜尋**: PostgreSQL 相似度搜尋
- **圖片儲存**: Cloudflare R2（賽博菩薩）
- **別名生成**: OpenAI API


## 協助貢獻

詳見 [`CONTRIBUTING.md`](CONTRIBUTING.md) 了解開發和建置細節。
