# ============================================================
#  Project Makefile
#  Manages the full Docker Compose stack:
#    db (PostgreSQL) · backend (FastAPI) · frontend (Vue) · server (Caddy)
# ============================================================

COMPOSE        := docker compose
COMPOSE_FILE   := docker-compose.yml
COMPOSE_FILE_OVERRIDE := docker-compose.override.yml
COMPOSE_FILE_PRODUCTION := docker-compose.prod.yml
ENV_FILE       := .env
POSTGRES_USER := $(shell cat secrets/postgres_user 2>/dev/null || echo appuser)

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
	@grep -Eh '^[a-zA-Z_-]+:.*##' $(MAKEFILE_LIST) \
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
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) build

.PHONY: build-no-cache
build-no-cache: guard-.env ## Build all images without using cache
	@echo -e "$(CYAN)Building all images (no cache)…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) build --no-cache

.PHONY: build-db
build-db: guard-.env ## Build only the db image
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) build db

.PHONY: build-backend
build-backend: guard-.env ## Build only the backend image
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) build backend

.PHONY: build-frontend
build-frontend: guard-.env ## Build only the frontend image
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) build frontend

.PHONY: build-server
build-server: guard-.env ## Build only the server image
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) build server

# ── Start / Stop ─────────────────────────────────────────────
.PHONY: up
up: guard-.env ## Start all services in detached mode
	@echo -e "$(CYAN)Starting all services…$(RESET)"
	$(COMPOSE)  -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) up -d

.PHONY: up-build
up-build: guard-.env ## Build images then start all services
	@echo -e "$(CYAN)Building and starting all services…$(RESET)"
	$(COMPOSE)  -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) up -d --build

.PHONY: down
down: ## Stop and remove all containers (keeps volumes)
	@echo -e "$(YELLOW)Stopping all services…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) down

.PHONY: down-volumes
down-volumes: ## Stop containers AND remove volumes (destructive!)
	@echo -e "$(YELLOW)Stopping services and removing volumes…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) down -v

.PHONY: stop
stop: ## Stop running containers without removing them
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) stop

.PHONY: start
start: guard-.env ## Start existing stopped containers
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) start

.PHONY: restart
restart: guard-.env ## Restart all services
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) restart

# ── Individual service control ───────────────────────────────
.PHONY: restart-backend
restart-backend: guard-.env ## Restart only the backend container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) restart backend

.PHONY: restart-frontend
restart-frontend: guard-.env ## Restart only the frontend container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) restart frontend

.PHONY: restart-server
restart-server: guard-.env ## Restart only the Caddy container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) restart server

.PHONY: restart-db
restart-db: guard-.env ## Restart only the database container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) restart db

# ── Logs ─────────────────────────────────────────────────────
.PHONY: logs
logs: ## Tail logs from all services
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) logs -f

.PHONY: logs-db
logs-db: ## Tail logs from the db container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) logs -f db

.PHONY: logs-backend
logs-backend: ## Tail logs from the backend container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) logs -f backend

.PHONY: logs-frontend
logs-frontend: ## Tail logs from the frontend container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) logs -f frontend

.PHONY: logs-server
logs-server: ## Tail logs from the server (Caddy) container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) logs -f server

# ── Status ───────────────────────────────────────────────────
.PHONY: ps
ps: ## Show container status
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) ps

.PHONY: health
health: ## Show healthcheck status for all containers
	@docker inspect --format '{{.Name}} → {{.State.Health.Status}}' \
		$$($(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) ps -q) 2>/dev/null || \
		echo -e "$(YELLOW)No running containers found$(RESET)"

# ── Shell access ─────────────────────────────────────────────
.PHONY: shell-backend
shell-backend: ## Open a shell in the backend container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) exec backend /bin/bash

.PHONY: shell-frontend
shell-frontend: ## Open a shell in the frontend container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) exec frontend /bin/sh

.PHONY: shell-db
shell-db: ## Open a psql session in the db container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) exec db \
		psql -U $${POSTGRES_USER:-appuser} -d $${POSTGRES_DB:-appdb}

.PHONY: shell-server
shell-server: ## Open a shell in the Caddy container
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) exec server /bin/sh

# ── Database helpers ─────────────────────────────────────────
.PHONY: db-dump
db-dump: guard-.env ## Dump the database to ./db/backup.sql
	@echo -e "$(CYAN)Dumping database…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) exec db \
		pg_dump -U $${POSTGRES_USER:-appuser} $${POSTGRES_DB:-appdb} \
		> db/backup.sql
	@echo -e "$(GREEN)Dump saved to db/backup.sql$(RESET)"

.PHONY: db-restore
db-restore: guard-.env ## Restore database from ./db/backup.sql
	@echo -e "$(CYAN)Restoring database from db/backup.sql…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) exec -T db \
		psql -U $${POSTGRES_USER:-appuser} -d $${POSTGRES_DB:-appdb} \
		< db/backup.sql
	@echo -e "$(GREEN)Restore complete$(RESET)"

.PHONY: populate
populate: ## Creates fake data for testing purposes
	@echo -e "$(YELLOW)Populating database with users$(RESET)"
	docker compose exec backend sh -c '. ../entrypoint.sh && python3 -m utils.seed_score_history'

# ── Cleanup ──────────────────────────────────────────────────
.PHONY: clean
clean: down ## Remove containers, images, and build cache for this project
	@echo -e "$(YELLOW)Removing project images and build cache…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_OVERRIDE) down --rmi local
	docker builder prune -f

.PHONY: prune
prune: ## Remove ALL unused Docker resources system-wide (use with care)
	@echo -e "$(YELLOW)Pruning all unused Docker resources…$(RESET)"
	docker system prune -af --volumes

# ── FrontPage ──────────────────────────────────────────────────
.PHONY: open-https
open-https: guard-.env ## Opens the browser into the vite main page through caddy https
	@echo -e "$(YELLOW)Starting vite in browser$(RESET)"
	xdg-open http://localhost:$${HTTPS_PORT}/

.PHONY: open-http
open-http: guard-.env ## Opens the browser into the vite main page through caddy http
	@echo -e "$(YELLOW)Starting vite in browser$(RESET)"
	xdg-open http://localhost:$${HTTP_PORT}/


# ── Production ──────────────────────────────────────────────────
.PHONY: prod-up
prod-up: guard-.env ## Start all services in detached mode for production
	@echo -e "$(CYAN)Starting all services…$(RESET)"
	$(COMPOSE)  -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_PRODUCTION) up -d

.PHONY: prod-up-build
prod-up-build: guard-.env ## Build images then start all services for production
	@echo -e "$(CYAN)Building and starting all services…$(RESET)"
	$(COMPOSE)  -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_PRODUCTION) up -d --build

.PHONY: prod-down
prod-down: ## Stop and remove all containers for production (keeps volumes)
	@echo -e "$(YELLOW)Stopping all services…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_PRODUCTION) down

.PHONY: prod-down-volumes
prod-down-volumes: ## Stop containers AND remove volumes for production (destructive!)
	@echo -e "$(YELLOW)Stopping services and removing volumes…$(RESET)"
	$(COMPOSE) -f $(COMPOSE_FILE) -f $(COMPOSE_FILE_PRODUCTION) down -v

.PHONY: admin
admin: ## Creates users admin role
	@echo -e "$(YELLOW)Creating admin user$(RESET)"
	docker compose exec backend python3 -m utils.create_admin

.PHONY: init-secrets
init-secrets: ## Creates de necessary secret files, but empty 
	@echo -e "$(YELLOW)Creating admin user$(RESET)"
	@mkdir -p secrets
	@touch secrets/postgres_password secrets/postgres_user secrets/secret_key