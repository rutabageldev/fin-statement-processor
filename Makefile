# Makefile for Ledgerly Multi-Container Development

.PHONY: help up down build rebuild logs shell-backend shell-frontend shell-postgres test clean status health

## Show available commands
help:
	@echo "🚀 Ledgerly Development Commands"
	@echo ""
	@echo "Core Commands:"
	@echo "  make up        - Start all services (docker compose up -d)"
	@echo "  make down      - Stop all services (docker compose down)"
	@echo "  make build     - Build all services (docker compose build)"
	@echo "  make rebuild   - Rebuild all services from scratch"
	@echo "  make logs      - Show logs for all services"
	@echo ""
	@echo "Service Shell Access:"
	@echo "  make shell-backend   - Open shell in backend container"
	@echo "  make shell-frontend  - Open shell in frontend container"
	@echo "  make shell-postgres  - Open psql shell in database"
	@echo ""
	@echo "Development:"
	@echo "  make test      - Run backend tests in container"
	@echo "  make status    - Show status of all services"
	@echo "  make health    - Check health of all services"
	@echo "  make clean     - Clean up containers, volumes, and images"

## Start all development services
up:
	@echo "🚀 Starting Ledgerly development environment..."
	docker compose up -d
	@echo "✅ All services started. Access:"
	@echo "   Frontend: http://localhost:3000"
	@echo "   Backend:  http://localhost:8000"
	@echo "   API Docs: http://localhost:8000/docs"
	@echo "   MinIO:    http://localhost:9001 (admin/admin)"

## Stop all services
down:
	@echo "🛑 Stopping all services..."
	docker compose down

## Build all services
build:
	@echo "🔨 Building all services..."
	docker compose build

## Rebuild all services from scratch
rebuild:
	@echo "🔄 Rebuilding all services from scratch..."
	docker compose down
	docker compose build --no-cache
	docker compose up -d

## Show logs for all services
logs:
	docker compose logs -f

## Open shell in backend container
shell-backend:
	@echo "🐚 Opening shell in backend container..."
	docker compose exec backend bash

## Open shell in frontend container
shell-frontend:
	@echo "🐚 Opening shell in frontend container..."
	docker compose exec frontend bash

## Open PostgreSQL shell
shell-postgres:
	@echo "🐚 Opening PostgreSQL shell..."
	docker compose exec postgres psql -U postgres -d ledgerly

## Run backend tests
test:
	@echo "🧪 Running backend tests..."
	docker compose exec backend pytest

## Show service status
status:
	@echo "📊 Service Status:"
	docker compose ps

## Check service health
health:
	@echo "🏥 Health Check Results:"
	@docker compose ps --format "table {{.Names}}\t{{.Status}}" | grep -E "(healthy|unhealthy|starting)"

## Clean up everything
clean:
	@echo "🧹 Cleaning up containers, volumes, and images..."
	@echo "⚠️  This will remove all data. Press Ctrl+C to cancel, Enter to continue..."
	@read
	docker compose down -v --rmi all
	@echo "✅ Cleanup complete"
