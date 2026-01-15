.PHONY: help install setup start-db stop-db init-db run label build-embeddings

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies with uv"
	@echo "  make setup        - Full setup (install + start db + init db)"
	@echo "  make start-db     - Start PostgreSQL with Docker Compose"
	@echo "  make stop-db      - Stop PostgreSQL"
	@echo "  make init-db      - Initialize database with pgvector"
	@echo "  make run          - Run the bot"
	@echo "  make label        - Run labeling tool"
	@echo "  make build-embeddings - Build embeddings for memes"

install:
	uv sync

setup: install start-db
	@echo "Waiting for database to be ready..."
	@sleep 5
	@python scripts/init_db.py

start-db:
	docker-compose up -d

stop-db:
	docker-compose down

init-db:
	python scripts/init_db.py

run:
	python main.py

label:
	python tools/label_tool.py data/images/

build-embeddings:
	python tools/build_embedding.py

pre-commit:
	pre-commit run --all-files
