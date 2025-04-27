# Makefile for Telegram Bot Docker management

# Variables
IMAGE_NAME = telegram-bot
CONTAINER_NAME = telegram-bot-container

.PHONY: build run stop clean logs

restart: stop build run

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

# Combined commands
deploy: build run

restart: stop run
