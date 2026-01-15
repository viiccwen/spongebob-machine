## 一、整體系統目標（先定義你在做什麼）

> **使用者用自然語言輸入一句話，Bot 會「理解情緒 / 意圖」，並派發最適合的海綿寶寶梗圖**

例如：

* 使用者：「我快被 deadline 壓死」
* Bot → 傳送「海綿寶寶崩潰 / 眼神死」梗圖
* 使用者：「今天超爽」
* Bot → 傳送「彩虹海綿寶寶」

---

## 二、整體系統架構（高層）

```text
Telegram User
     │
     ▼
Telegram Bot (python-telegram-bot)
     │
     ▼
NLP 處理層
  ├─ Intent / Emotion 分析
  ├─ 關鍵字擴充
  └─ 相似語意搜尋
     │
     ▼
Meme Selector
  ├─ 梗圖 metadata
  ├─ 分數排序
  └─ 隨機 / Top-k 抽選
     │
     ▼
Image Sender
```

---

## 三、專案資料夾架構

```text
spongebob-meme-bot/
├── bot/
│   ├── main.py              # Bot 啟動點
│   ├── handlers/
│   │   ├── start.py
│   │   ├── message.py       # 接收使用者輸入
│   │   └── callback.py
│   └── keyboards.py
│
├── nlp/
│   ├── intent.py            # 意圖 / 情緒分類
│   ├── embedding.py         # sentence embedding
│   └── keyword_expansion.py
│
├── meme/
│   ├── selector.py          # 梗圖選擇邏輯
│   ├── dataset.py           # 讀取 metadata
│   └── scoring.py
│
├── data/
│   ├── images/
│   │   ├── angry/
│   │   ├── happy/
│   │   ├── tired/
│   │   └── sarcastic/
│   ├── memes.json           # 梗圖標註資料
│   └── embeddings.npy       # 預先算好的向量
│
├── tools/
│   ├── label_tool.py        # 半自動標註工具
│   └── build_embedding.py
│
├── pyproject.toml
└── README.md
```

---

## 四、前期「照片標註」策略（重點）

### 1️⃣ 梗圖不是只有「一個 label」

你**一定要多標籤（multi-label）**，否則 NLP 會很難發揮。

### 📌 每張梗圖建議標註：

```json
{
  "id": "sb_023",
  "file": "images/tired/sb_023.jpg",
  "emotion": ["tired", "despair"],
  "intent": ["complain", "burnout"],
  "tone": ["sarcastic"],
  "keywords": [
    "累",
    "好煩",
    "不想做了",
    "下班",
    "人生好難"
  ],
  "caption": "我真的不行了"
}
```

### 建議的標註維度

| 類型       | 說明                                    |
| -------- | ------------------------------------- |
| emotion  | happy / angry / sad / tired / crazy   |
| intent   | complain / celebrate / mock / comfort |
| tone     | sarcastic / cute / dark               |
| keywords | 口語、梗語、近義詞                             |
| caption  | 人類可讀描述                                |

👉 **這個設計超重要**，後面 NLP 才好玩。

---

## 五、前期如何「快速標註」而不累死自己

### ✅ 方法一：半自動 CLI 標註（推薦）

```bash
python tools/label_tool.py images/
```

互動式：

```text
Image: sb_023.jpg
emotion? [tired/angry/happy]: tired
intent? [complain/celebrate]: complain
tone? [sarcastic/cute]: sarcastic
keywords (comma): 累, 不行了, 下班
```

👉 直接輸出 JSON

---

### ✅ 方法二：用 LLM 幫你「初標」

你可以這樣做：

1. 把圖片 + OCR / caption 丟給 GPT
2. 產生 **初始 label**
3. 你只要「修正」

這在資料量 >100 張時非常有價值。

---

## 六、使用者如何「取得照片」（核心互動設計）

### 模式一：自由輸入（最帥）

```text
User: 我真的快撐不下去了
```

流程：

1. NLP → 偵測

   * emotion: tired / sad
   * intent: complain
2. 梗圖篩選
3. 回傳圖片 + 一句嘴砲

---

### 模式二：選單輔助（新手友善）

```text
你今天怎麼了？
[ 😫 好累 ]
[ 😡 生氣 ]
[ 😆 爽啦 ]
```

👉 直接對應 intent，**不走 NLP**
👉 新手保證成功率高

---

### 模式三：梗圖抽卡（派星機）

```text
/派星
```

* 從 Top-N 熱門 meme 隨機
* 或依最近對話情緒加權

---

## 七、NLP 技術設計

### 🔵 Level 2（Embedding 語意搜尋 ⭐推薦）

1. 使用 Sentence-BERT / OpenAI Embedding
2. 每張梗圖 → 向量
3. 使用者輸入 → 向量
4. cosine similarity 找最像的 meme

```text
"我快被老闆榨乾"
≈
"累到懷疑人生"
```

👉 **這一層就是你履歷的亮點**

## 八、Bot 回覆設計（讓它「有靈魂」）

```python
responses = {
  "tired": [
    "來，這張給你 😭",
    "你需要這張",
    "社畜懂你"
  ]
}
```

📌 圖片 + 一句話，比單純傳圖好太多。

---

## 九、你這個專案「可以怎麼包裝」

### 在作品集 / README 說：

* ✅ Telegram Bot 工程
* ✅ NLP（embedding / intent）
* ✅ Dataset 標註設計
* ✅ 多標籤情緒建模
* ✅ 實際互動產品
