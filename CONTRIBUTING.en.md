# Contributing Guide

This document contains development and build details for the project.

## Table of Contents

- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Development Workflow](#development-workflow)
- [Build and Deployment](#build-and-deployment)
- [Testing](#testing)
- [Code Style](#code-style)
- [Commit Convention](#commit-convention)

## Development Environment Setup

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) package manager
- Docker and Docker Compose
- Git

### Initial Setup

1. **Clone the repository**:
```bash
git clone <repository-url>
cd spongebob-machine
```

2. **Install dependencies**:
```bash
make install
# or
uv sync
```

3. **Set up environment variables**:
```bash
cp env.example .env
# Edit .env file and fill in required environment variables
```

4. **Start the database**:
```bash
make start-db
# or
docker-compose up -d
```

5. **Initialize the database**:
```bash
make init-db
# or
uv run python scripts/init_db.py
```

6. **Import test data** (optional):
```bash
make import-xlsx
# or
uv run python tools/import_xlsx.py data/image_lists.xlsx
```

## Project Structure

```
spongebob-machine/
├── src/                    # Source code (src-layout)
│   ├── bot/               # Bot-related code
│   │   ├── handlers/      # Message handlers
│   │   │   ├── start.py   # /start command handler
│   │   │   ├── message.py # Text message handler
│   │   │   ├── random.py  # /random command handler
│   │   │   └── callback.py # Callback query handler
│   │   ├── main.py        # Bot entry point
│   │   ├── utils.py       # Utility functions (R2 integration)
│   │   └── logger.py      # Logging configuration
│   ├── meme/              # Meme selection logic
│   │   ├── selector.py    # Meme selector
│   │   └── dataset.py     # Dataset management
│   └── db/                 # Database-related
│       ├── models.py      # SQLAlchemy models
│       ├── connection.py  # Database connection
│       └── user_queries.py # User query operations
├── tools/                  # Utility tools
│   └── import_xlsx.py     # Excel import tool
├── scripts/                # Scripts
│   └── init_db.py         # Database initialization
├── data/                   # Data files
│   └── image_lists.xlsx   # Meme metadata
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile              # Docker build file
├── .dockerignore           # Docker ignore file
├── .pre-commit-config.yaml # Pre-commit configuration
├── pyproject.toml          # Project configuration
├── Makefile                # Make commands
└── main.py                 # Application entry point
```

## Development Workflow

### Running the Bot

```bash
make run
# or
uv run python main.py
```

### Makefile Commands

```bash
make help          # Show all available commands
make install       # Install dependencies with uv
make setup         # Full setup (install + start db + init db)
make start-db      # Start PostgreSQL with Docker Compose
make stop-db       # Stop PostgreSQL
make init-db       # Initialize database (enable pg_trgm extension)
make run           # Run the bot
make import-xlsx   # Import memes from Excel file
make pre-commit    # Run pre-commit checks
```

### Database Operations

#### Initialize Database
```bash
make init-db
```

This will:
- Enable `pg_trgm` extension
- Create all tables (memes, users, user_queries)

#### Reset Database (for development)
```bash
make stop-db
docker volume rm spongebob-machine_postgres_data
make start-db
make init-db
```

### Import Meme Data

```bash
# Import new data
make import-xlsx

# Update existing data
uv run python tools/import_xlsx.py data/image_lists.xlsx --update
```

## Build and Deployment

### Docker Build

#### Build Image
```bash
docker build -t spongebob-machine .
```

#### Run Container
```bash
docker run --env-file .env spongebob-machine
```

#### Using Docker Compose (with database)
You can extend `docker-compose.yml` to include the Bot service:

```yaml
services:
  bot:
    build: .
    env_file: .env
    depends_on:
      - postgres
    restart: unless-stopped
```

### Production Deployment

1. **Set environment variables**:
   - Ensure all required environment variables are set
   - `DEBUG=false` for production environment
   - Set appropriate `DAILY_QUERY_LIMIT`

2. **Build Docker image**:
```bash
docker build -t spongebob-machine:latest .
```

3. **Run container**:
```bash
docker run -d \
  --name spongebob-bot \
  --env-file .env \
  --restart unless-stopped \
  spongebob-machine:latest
```

4. **Monitor logs**:
```bash
docker logs -f spongebob-bot
```

## Testing

### Running Pre-commit Checks

```bash
make pre-commit
# or
uv run pre-commit run --all-files
```

Pre-commit will execute:
- Trim trailing whitespace
- Fix end of files
- Check YAML format
- Check for large files
- Black code formatting
- Ruff code checking
- MyPy type checking

### Manual Testing

1. **Test Bot commands**:
   - `/start` - Should display welcome message
   - `/random` - Should return random meme

2. **Test text search**:
   - Input various keywords to test search functionality
   - Test cases where no results are found

3. **Test selection mechanism**:
   - Test multiple option selection
   - Test single result direct sending

4. **Test rate limiting**:
   - Test daily query limit
   - Test limit reset mechanism

## Code Style

### Python Style Guide

The project uses the following tools to ensure code quality:

- **Black**: Code formatting
- **Ruff**: Code checking and linting
- **MyPy**: Type checking

### Type Hints

- Use type hints whenever possible
- SQLAlchemy models use `Mapped` type
- Function parameters and return values should have type hints

### Naming Conventions

- Functions and variables: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_SNAKE_CASE`
- Private members: prefix with `_`

### Docstrings

All public functions and classes should have docstrings:

```python
def function_name(param: str) -> bool:
    """
    Function description.

    Args:
        param: Parameter description

    Returns:
        Return value description
    """
    pass
```

## Commit Convention

The project uses [Conventional Commits](https://www.conventionalcommits.org/) specification:

### Commit Types

- `feat`: A new feature
- `fix`: A bug fix
- `refactor`: Code refactoring
- `chore`: Build process, dependencies, config changes
- `docs`: Documentation updates
- `test`: Test-related
- `style`: Code style changes (formatting, linting)
- `perf`: Performance improvements
- `ci`: CI/CD pipeline changes

### Commit Format

```
<type>(<scope>): <summary>

<optional body>

<optional footer>
```

### Examples

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

## Database Migration

When modifying database models:

1. **Update models** (`src/db/models.py`)
2. **Run initialization script** (will automatically create new tables/columns):
```bash
make init-db
```

Note: Currently not using Alembic for migrations, directly using `Base.metadata.create_all()`.

## Logging Configuration

Logging configuration is in `src/bot/logger.py`:

- **Production** (`DEBUG=false`): `WARNING` level
- **Development** (`DEBUG=true`): `DEBUG` level

External package log levels are set to `WARNING` to reduce noise.

## Environment Variables

### Required Variables

- `TELEGRAM_BOT_TOKEN`: Telegram Bot Token
- `DATABASE_URL`: PostgreSQL connection string

### Optional Variables

- `R2_ACCOUNT_ID`, `R2_ACCESS_KEY_ID`, `R2_SECRET_ACCESS_KEY`, `R2_ENDPOINT_URL`: Cloudflare R2 credentials
- `R2_BUCKET_NAME`: R2 bucket name (default: spongebob-memes)
- `OPENAI_API_KEY`: OpenAI API key (for alias generation)
- `OPENAI_MODEL`: OpenAI model (default: gpt-4o-mini)
- `DAILY_QUERY_LIMIT`: Daily query limit (default: 100)
- `DEBUG`: Debug mode (default: false)

## Troubleshooting

### Database Connection Issues

- Verify PostgreSQL container is running: `docker-compose ps`
- Check if `DATABASE_URL` is correct
- Verify database is initialized: `make init-db`

### Image Loading Failures

- Verify R2 credentials are correct
- Check if images are uploaded to correct path: `spongebob-memes/{meme_id}.jpg`
- Check if R2 bucket name is correct

### Empty Search Results

- Verify data is imported: check `memes` table
- Check if `aliases` field has data
- Try lowering similarity threshold (in `dataset.py`)

## Contribution Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make changes and commit (following commit convention)
4. Run pre-commit checks: `make pre-commit`
5. Push branch: `git push origin feature/your-feature`
6. Create Pull Request

## License

MIT License
