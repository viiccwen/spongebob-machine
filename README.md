# SpongeBob Meme Machine

A Telegram bot that sends SpongeBob memes based on user emotions and intents using NLP and semantic search.

## Features

- 🤖 Telegram Bot integration
- 🧠 NLP-based intent and emotion analysis
- 🔍 Semantic search using sentence embeddings
- 🎯 Multi-label meme classification
- 📊 PostgreSQL + pgvector for vector storage

## Project Structure

```
spongebob-machine/
├── bot/                    # Bot handlers and logic
│   ├── handlers/          # Message and command handlers
│   └── keyboards.py       # Inline keyboard definitions
├── nlp/                   # NLP processing
│   ├── intent.py         # Intent/emotion analysis
│   ├── embedding.py      # Sentence embeddings
│   └── keyword_expansion.py
├── meme/                  # Meme selection logic
│   ├── selector.py       # Meme selection
│   ├── dataset.py        # Dataset management
│   └── scoring.py        # Meme scoring
├── db/                    # Database models
│   ├── models.py         # SQLAlchemy models
│   └── connection.py     # DB connection
├── data/                  # Data files
│   ├── images/           # Meme images
│   └── memes.json        # Meme metadata
├── tools/                 # Utility tools
│   ├── label_tool.py    # Labeling tool
│   └── build_embedding.py
└── docker-compose.yml     # Docker setup
```

## Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose

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
cp .env.example .env
# Edit .env and add your TELEGRAM_BOT_TOKEN
```

4. Start PostgreSQL with Docker Compose:
```bash
docker-compose up -d
```

5. Initialize the database:
```python
from db.connection import init_db
init_db()
```

6. Prepare your meme data:
   - Add meme images to `data/images/`
   - Use the labeling tool to create metadata:
```bash
python tools/label_tool.py data/images/
```

7. Build embeddings (optional):
```bash
python tools/build_embedding.py
```

8. Run the bot:
```bash
python bot/main.py
```

## Usage

### Bot Commands

- `/start` - Start the bot and see welcome message
- `/派星` - Get a random meme

### Interaction Modes

1. **Free Text Input**: Type your feelings and the bot will find a matching meme
2. **Button Selection**: Use inline buttons to quickly select by emotion
3. **Random Meme**: Use `/派星` command for a random meme

## Development

### Adding New Memes

1. Place images in `data/images/<emotion>/`
2. Use the labeling tool:
```bash
python tools/label_tool.py data/images/
```

### Meme Metadata Format

```json
{
  "id": "sb_023",
  "file": "images/tired/sb_023.jpg",
  "emotion": ["tired", "despair"],
  "intent": ["complain", "burnout"],
  "tone": ["sarcastic"],
  "keywords": ["累", "好煩", "不想做了", "下班", "人生好難"],
  "caption": "我真的不行了"
}
```

## Technology Stack

- **Bot Framework**: python-telegram-bot
- **NLP**: sentence-transformers
- **Database**: PostgreSQL + pgvector
- **ORM**: SQLAlchemy
- **Package Manager**: uv

## License

MIT
