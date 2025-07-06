# Makefile

BASE_NAME = fin-statement-processor-dev
IMAGE_NAME = fin-statement-processor-dev

# Sanitize branch name (replace slashes and dashes with underscores)
RAW_BRANCH := $(shell git rev-parse --abbrev-ref HEAD)
SANITIZED_BRANCH := $(shell echo $(RAW_BRANCH) | sed 's#[/-]#_#g')

CONTAINER_NAME = $(BASE_NAME)-$(SANITIZED_BRANCH)

.PHONY: help build shell run clean rebuild

## Show available commands
help:
	@echo "Available commands for branch: $(RAW_BRANCH)"
	@echo "  make build     - Build and start container: $(CONTAINER_NAME)"
	@echo "  make rebuild   - Rebuild container for current branch"
	@echo "  make shell     - Open a shell in the container"
	@echo "  make run       - Run dev_parse.py inside the container"
	@echo "  make clean     - Remove container for current branch"

## Build image and run container for current branch
build:
	@if docker ps -a --format "{{.Names}}" | grep -q "^$(CONTAINER_NAME)$$"; then \
		echo "❌ Container $(CONTAINER_NAME) already exists. Run 'make rebuild' to replace it."; \
		exit 1; \
	fi
	docker build -f .devcontainer/Dockerfile.dev -t $(IMAGE_NAME) .
	docker run -d \
		--env-file .env \
		--name $(CONTAINER_NAME) \
		-v $(PWD):/app \
		-w /app \
		$(IMAGE_NAME) tail -f /dev/null
	@echo "✅ Container $(CONTAINER_NAME) started."

## Rebuild image and container
rebuild:
	-@docker rm -f $(CONTAINER_NAME)
	@$(MAKE) build

## Open shell in the container
shell:
	@docker exec -it $(CONTAINER_NAME) bash

## Run the dev_parse script
run:
	@docker exec -it $(CONTAINER_NAME) python -m services.dev_parse

## Stop and remove container
clean:
	-@docker rm -f $(CONTAINER_NAME)
