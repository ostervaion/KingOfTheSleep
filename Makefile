# ============================================================
#  Project Makefile
#  Manages the full Docker Compose stack:
#    db (PostgreSQL) · backend (FastAPI) · frontend (Vue) · server (Caddy)
# ============================================================

COMPOSE        := docker compose
COMPOSE_FILE   := docker-compose.yml
ENV_FILE       := .env

# Colours
GREEN  := \033[0;32m
YELLOW := \033[0;33m
CYAN   := \033[0;36m
RED    := \033[0;31m
RESET  := \033[0m

.DEFAULT_GOAL := help


ifneq ("$(wildcard $(ENV_FILE))","")
    include $(ENV_FILE)
    export
endif

.PHONY: guard-.env
guard-.env:
	@if [ ! -f $(ENV_FILE) ]; then \
		echo -e "$(RED)Error: You don't have an .env file created!$(RESET)"; \
		echo -e "$(YELLOW)Please run 'make env' first to generate it.$(RESET)"; \
		exit 1; \
	fi

# ── Help ─────────────────────────────────────────────────────
.PHONY: help
help: ## Show this help message
	@echo ""
	@echo -e "$(CYAN)Available targets:$(RESET)"
	@grep -E '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) \
		| awk 'BEGIN {FS = ":.*##"}; {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}'
	@echo ""

# ── Environment ──────────────────────────────────────────────
.PHONY: env
env: ## Copy .env.example to .env (skips if .env already exists)
	@if [ -f $(ENV_FILE) ]; then \
		echo -e "$(YELLOW)$(ENV_FILE) already exists – skipping.$(RESET)"; \
	else \
		cp .env.example $(ENV_FILE); \
		echo -e "$(GREEN)Created $(ENV_FILE) from .env.example$(RESET)"; \
	fi

# ── Build ────────────────────────────────────────────────────
.PHONY: build
build: guard-.env ## Build all Docker images
	@echo -e "$(CYAN)Building all images…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) build

.PHONY: build-no-cache
build-no-cache: guard-.env ## Build all images without using cache
	@echo -e "$(CYAN)Building all images (no cache)…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) build --no-cache

.PHONY: build-db
build-db: guard-.env ## Build only the db image
	$(COMPOSE) -f $(COMPOSE_FILE) build db

.PHONY: build-backend
build-backend: guard-.env ## Build only the backend image
	$(COMPOSE) -f $(COMPOSE_FILE) build backend

.PHONY: build-frontend
build-frontend: guard-.env ## Build only the frontend image
	$(COMPOSE) -f $(COMPOSE_FILE) build frontend

.PHONY: build-server
build-server: guard-.env ## Build only the server image
	$(COMPOSE) -f $(COMPOSE_FILE) build server

# ── Start / Stop ─────────────────────────────────────────────
.PHONY: up
up: guard-.env ## Start all services in detached mode
	@echo -e "$(CYAN)Starting all services…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) up -d

.PHONY: up-build
up-build: guard-.env ## Build images then start all services
	@echo -e "$(CYAN)Building and starting all services…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) up -d --build

.PHONY: down
down: ## Stop and remove all containers (keeps volumes)
	@echo -e "$(YELLOW)Stopping all services…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) down

.PHONY: down-volumes
down-volumes: ## Stop containers AND remove volumes (destructive!)
	@echo -e "$(YELLOW)Stopping services and removing volumes…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) down -v

.PHONY: stop
stop: ## Stop running containers without removing them
	$(COMPOSE) -f $(COMPOSE_FILE) stop

.PHONY: start
start: guard-.env ## Start existing stopped containers
	$(COMPOSE) -f $(COMPOSE_FILE) start

.PHONY: restart
restart: guard-.env ## Restart all services
	$(COMPOSE) -f $(COMPOSE_FILE) restart

# ── Individual service control ───────────────────────────────
.PHONY: restart-backend
restart-backend: guard-.env ## Restart only the backend container
	$(COMPOSE) -f $(COMPOSE_FILE) restart backend

.PHONY: restart-frontend
restart-frontend: guard-.env ## Restart only the frontend container
	$(COMPOSE) -f $(COMPOSE_FILE) restart frontend

.PHONY: restart-server
restart-server: guard-.env ## Restart only the Caddy container
	$(COMPOSE) -f $(COMPOSE_FILE) restart server

.PHONY: restart-db
restart-db: guard-.env ## Restart only the database container
	$(COMPOSE) -f $(COMPOSE_FILE) restart db

# ── Logs ─────────────────────────────────────────────────────
.PHONY: logs
logs: ## Tail logs from all services
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f

.PHONY: logs-db
logs-db: ## Tail logs from the db container
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f db

.PHONY: logs-backend
logs-backend: ## Tail logs from the backend container
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f backend

.PHONY: logs-frontend
logs-frontend: ## Tail logs from the frontend container
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f frontend

.PHONY: logs-server
logs-server: ## Tail logs from the server (Caddy) container
	$(COMPOSE) -f $(COMPOSE_FILE) logs -f server

# ── Status ───────────────────────────────────────────────────
.PHONY: ps
ps: ## Show container status
	$(COMPOSE) -f $(COMPOSE_FILE) ps

.PHONY: health
health: ## Show healthcheck status for all containers
	@docker inspect --format '{{.Name}} → {{.State.Health.Status}}' \
		$$($(COMPOSE) -f $(COMPOSE_FILE) ps -q) 2>/dev/null || \
		echo -e "$(YELLOW)No running containers found$(RESET)"

# ── Shell access ─────────────────────────────────────────────
.PHONY: shell-backend
shell-backend: ## Open a shell in the backend container
	$(COMPOSE) -f $(COMPOSE_FILE) exec backend /bin/bash

.PHONY: shell-frontend
shell-frontend: ## Open a shell in the frontend container
	$(COMPOSE) -f $(COMPOSE_FILE) exec frontend /bin/sh

.PHONY: shell-db
shell-db: ## Open a psql session in the db container
	$(COMPOSE) -f $(COMPOSE_FILE) exec db \
		psql -U $${POSTGRES_USER:-appuser} -d $${POSTGRES_DB:-appdb}

.PHONY: shell-server
shell-server: ## Open a shell in the Caddy container
	$(COMPOSE) -f $(COMPOSE_FILE) exec server /bin/sh

# ── Database helpers ─────────────────────────────────────────
.PHONY: db-dump
db-dump: guard-.env ## Dump the database to ./db/backup.sql
	@echo -e "$(CYAN)Dumping database…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) exec db \
		pg_dump -U $${POSTGRES_USER:-appuser} $${POSTGRES_DB:-appdb} \
		> db/backup.sql
	@echo -e "$(GREEN)Dump saved to db/backup.sql$(RESET)"

.PHONY: db-restore
db-restore: guard-.env ## Restore database from ./db/backup.sql
	@echo -e "$(CYAN)Restoring database from db/backup.sql…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) exec -T db \
		psql -U $${POSTGRES_USER:-appuser} -d $${POSTGRES_DB:-appdb} \
		< db/backup.sql
	@echo -e "$(GREEN)Restore complete$(RESET)"

# ── Cleanup ──────────────────────────────────────────────────
.PHONY: clean
clean: down ## Remove containers, images, and build cache for this project
	@echo -e "$(YELLOW)Removing project images and build cache…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) down --rmi local
	docker builder prune -f

.PHONY: prune
prune: ## Remove ALL unused Docker resources system-wide (use with care)
	@echo -e "$(YELLOW)Pruning all unused Docker resources…$(RESET)"
	docker system prune -af --volumes

.PHONY: open-https
open-https: guard-.env ## Opens the browser into the vite main page through caddy https
	@echo -e "$(YELLOW)Starting vite in browser$(RESET)"
	xdg-open http://localhost:$${HTTPS_PORT}/

.PHONY: open-http
open-http: guard-.env ## Opens the browser into the vite main page through caddy http
	@echo -e "$(YELLOW)Starting vite in browser$(RESET)"
	xdg-open http://localhost:$${HTTP_PORT}/