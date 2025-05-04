# Makefile for Telegram Bot Docker management

# Variables
IMAGE_NAME = telegram-bot
CONTAINER_NAME = telegram-bot-container
TEST_CMD = pytest -v test_bot.py

.PHONY: build run stop clean logs test help

help:
	@echo "Telegram Bot Management System"
	@echo ""
	@echo "Available commands:"
	@echo "  make build      - Build Docker image"
	@echo "  make run        - Run container in detached mode"
	@echo "  make stop       - Stop and remove container"
	@echo "  make clean      - Remove Docker image"
	@echo "  make logs       - Show container logs"
	@echo "  make test       - Run tests with coverage"
	@echo "  make deploy     - Build and run (alias for build + run)"
	@echo "  make restart    - Stop, build and run"
	@echo "  make help       - Show this help message"
	@echo ""
	@echo "Environment variables required for run:"
	@echo "  TOKEN      - Telegram bot token"
	@echo "  CHAT_ID    - Telegram chat ID"

build:
	@echo "Building Docker image..."
	docker build -t $(IMAGE_NAME) .

run:
	@echo "Starting bot container..."
	docker run -d \
		--name $(CONTAINER_NAME) \
		-e TOKEN=$(TOKEN) \
		-e CHAT_ID=$(CHAT_ID) \
		--restart unless-stopped \
		$(IMAGE_NAME)

stop:
	@echo "Stopping container..."
	-docker stop $(CONTAINER_NAME)
	@echo "Removing container..."
	-docker rm $(CONTAINER_NAME)

clean:
	@echo "Removing Docker image..."
	-docker rmi $(IMAGE_NAME)

logs:
	@echo "Showing logs..."
	docker logs -f $(CONTAINER_NAME)

shell:
	@docker exec -it telegram-bot-container bash

test:
	@echo "Running tests..."
	@docker exec -it telegram-bot-container $(TEST_CMD)

# Combined commands
deploy: build run

restart: stop build run
