# SpongeBob Meme Machine

A Telegram bot that sends SpongeBob memes based on user input using PostgreSQL's `pg_trgm` similarity search.

## Features

- 🤖 Telegram Bot integration
- 🔍 Semantic search using PostgreSQL `pg_trgm` extension
- ☁️ Cloudflare R2 for image storage
- 🤖 OpenAI API for automatic alias generation
- 📊 PostgreSQL + pgvector + pg_trgm for database operations
- 📝 Excel-based meme data import

## Project Structure

```
spongebob-machine/
├── src/                    # Source code (src-layout)
│   ├── bot/               # Bot handlers and logic
│   │   ├── handlers/     # Message and command handlers
│   │   ├── main.py        # Bot entry point
│   │   └── utils.py       # Utility functions (R2 integration)
│   ├── meme/              # Meme selection logic
│   │   ├── selector.py    # Meme selection
│   │   └── dataset.py    # Dataset management (pg_trgm search)
│   └── db/                # Database models
│       ├── models.py      # SQLAlchemy models
│       └── connection.py  # DB connection
├── tools/                 # Utility tools
│   └── import_xlsx.py     # Excel import with OpenAI alias generation
├── scripts/               # Scripts
│   └── init_db.py         # Database initialization
├── data/                  # Data files
│   └── image_lists.xlsx   # Meme metadata (ID, Name, Aliases)
├── docker-compose.yml     # Docker setup
└── main.py                # Application entry point
```

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose
- Cloudflare R2 account (for image storage)
- OpenAI API key (for alias generation, optional)

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd spongebob-machine
```

2. Install dependencies with uv:
```bash
uv sync
```

3. Set up environment variables:
```bash
cp env.example .env
# Edit .env and configure:
# - TELEGRAM_BOT_TOKEN
# - DATABASE_URL
# - R2_ACCOUNT_ID, R2_ACCESS_KEY_ID, R2_SECRET_ACCESS_KEY, R2_ENDPOINT_URL
# - OPENAI_API_KEY (optional, for alias generation)
```

4. Start PostgreSQL with Docker Compose:
```bash
docker-compose up -d
```

5. Initialize the database:
```bash
uv run python scripts/init_db.py
```

6. Upload images to Cloudflare R2:
   - Images should be uploaded to `spongebob-memes/{meme_id}.jpg`
   - For example: `spongebob-memes/SK0001.jpg`, `spongebob-memes/SS0002.jpg`

7. Import meme data from Excel:
```bash
uv run python tools/import_xlsx.py data/image_lists.xlsx
```

   The import tool will:
   - Read meme IDs and names from Excel
   - Automatically generate aliases using OpenAI API (if aliases are empty)
   - Import data to PostgreSQL

8. Run the bot:
```bash
uv run python main.py
```

## Usage

### Bot Commands

- `/start` - Start the bot and see welcome message
- `/random` - Get a random meme

### Interaction Modes

1. **Free Text Input**: Type your feelings or keywords, and the bot will find a matching meme using `pg_trgm` similarity search on aliases
2. **Random Meme**: Use `/random` command for a random meme

## Database Schema

The `memes` table contains:
- `id`: Auto-increment primary key
- `meme_id`: Unique meme identifier (e.g., SK0001, SS0002)
- `name`: Meme name
- `aliases`: Array of search aliases (used for similarity search)

## Adding New Memes

1. **Prepare Excel file** (`data/image_lists.xlsx`):
   - Column A: Meme ID (e.g., SK0001, SS0002)
   - Column B: Name
   - Column C: Aliases (comma-separated, optional)
     - If empty, aliases will be automatically generated using OpenAI API

2. **Upload image to R2**:
   - Upload image to `spongebob-memes/{meme_id}.jpg`
   - Example: For meme ID `SK0001`, upload to `spongebob-memes/SK0001.jpg`

3. **Import to database**:
```bash
uv run python tools/import_xlsx.py data/image_lists.xlsx
```

   Use `--update` flag to update existing memes:
```bash
uv run python tools/import_xlsx.py data/image_lists.xlsx --update
```

## Search Mechanism

The bot uses PostgreSQL's `pg_trgm` extension for fuzzy text matching:

- Searches through `aliases` array using trigram similarity
- Similarity threshold: 0.3 (configurable in code)
- Returns the best matching meme based on similarity score

## Technology Stack

- **Bot Framework**: python-telegram-bot
- **Database**: PostgreSQL + pgvector + pg_trgm
- **Search**: PostgreSQL `pg_trgm` similarity
- **Image Storage**: Cloudflare R2 (S3-compatible)
- **Alias Generation**: OpenAI API
- **ORM**: SQLAlchemy
- **Package Manager**: uv
- **Build System**: hatchling (src-layout)

## Environment Variables

See `env.example` for all required environment variables:

- `TELEGRAM_BOT_TOKEN`: Telegram bot token
- `DATABASE_URL`: PostgreSQL connection string
- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`: Cloudflare R2 credentials
- `OPENAI_API_KEY`: OpenAI API key (for alias generation)
- `OPENAI_MODEL`: OpenAI model to use (default: gpt-4o-mini)

## Development

### Running Pre-commit Checks

```bash
uv run pre-commit run --all-files
```

### Makefile Commands

```bash
make install      # Install dependencies with uv
make setup        # Full setup (install + start db + init db)
make start-db     # Start PostgreSQL with Docker Compose
make stop-db      # Stop PostgreSQL
make init-db      # Initialize database
make run          # Run the bot
make import-xlsx  # Import memes from Excel file
make pre-commit   # Run pre-commit checks
```

## License

MIT
