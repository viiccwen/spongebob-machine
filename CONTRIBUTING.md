# 開發指南 (Contributing Guide)

本文檔包含專案的開發和建置細節。

## 目錄

- [開發環境設定](#開發環境設定)
- [專案結構](#專案結構)
- [開發工作流程](#開發工作流程)
- [建置和部署](#建置和部署)
- [測試](#測試)
- [程式碼風格](#程式碼風格)
- [提交規範](#提交規範)

## 開發環境設定

### 前置需求

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) 套件管理器
- Docker 和 Docker Compose
- Git

### 初始設定

1. **複製儲存庫**：
```bash
git clone <repository-url>
cd spongebob-machine
```

2. **安裝依賴**：
```bash
make install
# 或
uv sync
```

3. **設定環境變數**：
```bash
cp env.example .env
# 編輯 .env 檔案，填入必要的環境變數
```

4. **啟動資料庫**：
```bash
make start-db
# or
docker-compose up -d
```

5. **初始化資料庫**：
```bash
make init-db
# or
uv run python scripts/init_db.py
```

6. **匯入測試資料**（選用）：
```bash
make import-xlsx
# or
uv run python tools/import_xlsx.py data/image_lists.xlsx
```

## 專案結構

```
spongebob-machine/
├── src/                    # 原始碼 (src-layout)
│   ├── bot/               # Bot 相關程式碼
│   │   ├── handlers/      # 訊息處理器
│   │   │   ├── start.py   # /start 指令處理
│   │   │   ├── message.py # 文字訊息處理
│   │   │   ├── random.py  # /random 指令處理
│   │   │   └── callback.py # 回調查詢處理
│   │   ├── main.py        # Bot 入口點
│   │   ├── utils.py       # 工具函數（R2 整合）
│   │   └── logger.py      # 日誌配置
│   ├── meme/              # 梗圖選擇邏輯
│   │   ├── selector.py    # 梗圖選擇器
│   │   └── dataset.py     # 資料集管理
│   └── db/                 # 資料庫相關
│       ├── models.py      # SQLAlchemy 模型
│       ├── connection.py  # 資料庫連線
│       └── user_queries.py # 使用者查詢操作
├── tools/                  # 工具程式
│   └── import_xlsx.py     # Excel 匯入工具
├── scripts/                # 腳本
│   └── init_db.py         # 資料庫初始化
├── data/                   # 資料檔案
│   └── image_lists.xlsx   # 梗圖元資料
├── docker-compose.yml      # Docker Compose 配置
├── Dockerfile              # Docker 建置檔案
├── .dockerignore           # Docker 忽略檔案
├── .pre-commit-config.yaml # Pre-commit 配置
├── pyproject.toml          # 專案配置
├── Makefile                # Make 指令
└── main.py                 # 應用程式入口點
```

## 開發工作流程

### 執行 Bot

```bash
make run
# 或
uv run python main.py
```

### Makefile 指令

```bash
make help          # 顯示所有可用指令
make install       # 使用 uv 安裝依賴
make setup         # 完整設定（安裝 + 啟動資料庫 + 初始化資料庫）
make start-db      # 使用 Docker Compose 啟動 PostgreSQL
make stop-db       # 停止 PostgreSQL
make init-db       # 初始化資料庫（啟用 pg_trgm 擴展）
make run           # 執行 Bot
make import-xlsx   # 從 Excel 檔案匯入梗圖
make pre-commit    # 執行 pre-commit 檢查
```

### 資料庫操作

#### 初始化資料庫
```bash
make init-db
```

這會：
- 啟用 `pg_trgm` 擴展
- 建立所有資料表（memes, users, user_queries）

#### 重置資料庫（開發用）
```bash
make stop-db
docker volume rm spongebob-machine_postgres_data
make start-db
make init-db
```

### 匯入梗圖資料

```bash
# 匯入新資料
make import-xlsx

# 更新現有資料
uv run python tools/import_xlsx.py data/image_lists.xlsx --update
```

## 建置和部署

### Docker 建置

#### 建置鏡像
```bash
docker build -t spongebob-machine .
```

#### 執行容器
```bash
docker run --env-file .env spongebob-machine
```

#### 使用 Docker Compose（包含資料庫）
可以擴展 `docker-compose.yml` 來包含 Bot 服務：

```yaml
services:
  bot:
    build: .
    env_file: .env
    depends_on:
      - postgres
    restart: unless-stopped
```

### 生產環境部署

1. **設定環境變數**：
   - 確保所有必要的環境變數都已設定
   - `DEBUG=false` 用於生產環境
   - 設定適當的 `DAILY_QUERY_LIMIT`

2. **建置 Docker 鏡像**：
```bash
docker build -t spongebob-machine:latest .
```

3. **執行容器**：
```bash
docker run -d \
  --name spongebob-bot \
  --env-file .env \
  --restart unless-stopped \
  spongebob-machine:latest
```

4. **監控日誌**：
```bash
docker logs -f spongebob-bot
```

## 測試

### 執行 Pre-commit 檢查

```bash
make pre-commit
# 或
uv run pre-commit run --all-files
```

### 手動測試

1. **測試 Bot 指令**：
   - `/start` - 應該顯示歡迎訊息
   - `/random` - 應該返回隨機梗圖

2. **測試文字搜尋**：
   - 輸入各種關鍵字測試搜尋功能
   - 測試找不到結果的情況

3. **測試選擇機制**：
   - 測試多選項選擇
   - 測試單一結果直接發送

4. **測試速率限制**：
   - 測試每日查詢限制
   - 測試限制重置機制

## 程式碼風格

### Python 風格指南

專案使用以下工具確保程式碼品質：

- **Black**: 程式碼格式化
- **Ruff**: 程式碼檢查和 linting
- **MyPy**: 類型檢查

### 類型提示

- 盡可能使用類型提示
- SQLAlchemy 模型使用 `Mapped` 類型
- 函數參數和返回值都應該有類型提示

### 命名規範

- 函數和變數：`snake_case`
- 類別：`PascalCase`
- 常數：`UPPER_SNAKE_CASE`
- 私有成員：前綴 `_`

### 文件字串

所有公開函數和類別都應該有文件字串：

```python
def function_name(param: str) -> bool:
    """
    函數描述。

    Args:
        param: 參數描述

    Returns:
        返回值描述
    """
    pass
```

## 提交規範

專案使用 [Conventional Commits](https://www.conventionalcommits.org/) 規範：

### 提交類型

- `feat`: 新功能
- `fix`: 錯誤修復
- `refactor`: 程式碼重構
- `chore`: 建置過程、依賴、配置變更
- `docs`: 文件更新
- `test`: 測試相關
- `style`: 程式碼風格變更（格式化、linting）
- `perf`: 效能改善
- `ci`: CI/CD 流程變更

### 提交格式

```
<type>(<scope>): <summary>

<optional body>

<optional footer>
```

### 範例

```
feat(bot): add rate limiting for daily queries

- Add daily_query_count and last_reset_date to User model
- Implement check_and_update_rate_limit function
- Add rate limit check in message and random handlers

Closes #123
```

```
fix(search): lower similarity threshold to improve hit rate

Change threshold from 0.3 to 0.2 to return more results
```

```
refactor(db): migrate from Column to mapped_column

Use SQLAlchemy 2.0 style mapped_column for better type inference
```

## 資料庫遷移

當修改資料庫模型時：

1. **更新模型** (`src/db/models.py`)
2. **執行初始化腳本**（會自動建立新表/欄位）：
```bash
make init-db
```

注意：目前沒有使用 Alembic 進行遷移，直接使用 `Base.metadata.create_all()`。

## 日誌配置

日誌配置在 `src/bot/logger.py`：

- **Production** (`DEBUG=false`): `WARNING` 層級
- **Development** (`DEBUG=true`): `DEBUG` 層級

外部套件的日誌層級設為 `WARNING` 以減少噪音。

## 環境變數

### 必要變數

- `TELEGRAM_BOT_TOKEN`: Telegram Bot Token
- `DATABASE_URL`: PostgreSQL 連線字串

### 選用變數

- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`: Cloudflare R2 憑證
- `R2_BUCKET_NAME`: R2 儲存桶名稱（預設：spongebob-memes）
- `OPENAI_API_KEY`: OpenAI API 金鑰（用於別名生成）
- `OPENAI_MODEL`: OpenAI 模型（預設：gpt-4o-mini）
- `DAILY_QUERY_LIMIT`: 每日查詢限制（預設：100）
- `DEBUG`: 除錯模式（預設：false）

## 疑難排解

### 資料庫連線問題

- 確認 PostgreSQL 容器正在執行：`docker-compose ps`
- 檢查 `DATABASE_URL` 是否正確
- 確認資料庫已初始化：`make init-db`

### 圖片載入失敗

- 確認 R2 憑證正確
- 檢查圖片是否已上傳到正確路徑：`spongebob-memes/{meme_id}.jpg`
- 檢查 R2 儲存桶名稱是否正確

### 搜尋結果為空

- 確認資料已匯入：檢查 `memes` 表
- 檢查 `aliases` 欄位是否有資料
- 嘗試降低相似度閾值（在 `dataset.py` 中）

## 貢獻流程

1. Fork 儲存庫
2. 建立功能分支：`git checkout -b feature/your-feature`
3. 進行變更並提交（遵循提交規範）
4. 執行 pre-commit 檢查：`make pre-commit`
5. 推送分支：`git push origin feature/your-feature`
6. 建立 Pull Request

## 授權

MIT License
