# --- Variables ---

ENV_FILE=.env
## --- Hermes ---
HERMES_API_KEY=change_me
## --- Ollama ---
OLLAMA_BASE_URL=http://ollama:11434/v1
OLLAMA_MODEL=wild-llm
## --- MCP ---
MCP_SERVER_URL=http://mlzero:8000/mcp/
## --- System ---
COMPOSE_PROJECT_NAME=argos

# --- Feature ---

.env: ## Create default environment file
	@test -f $(ENV_FILE) || (echo "\
	HERMES_API_KEY=$(HERMES_API_KEY)\n\
	OLLAMA_BASE_URL=$(OLLAMA_BASE_URL)\n\
	OLLAMA_MODEL=$(OLLAMA_MODEL)\n\
	MCP_SERVER_URL=$(MCP_SERVER_URL)\n\
	COMPOSE_PROJECT_NAME=$(COMPOSE_PROJECT_NAME)" > $(ENV_FILE) && echo "✅ .env created")

code-map: ## Export project structure to JSON
	uv run python3 libs/code_mapper.py --to-json

##@ Maintenance
clean: ## Remove python caches and temporary files
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .venv .ruff_cache .mypy_cache
	@# Remove legacy VS Code Snap environment injections that break devpod/devbox sessions
	-sed -i '/snap\/code/d' ~/.profile ~/.bashrc ~/.bash_aliases 2>/dev/null

nuke: ## ☢️  Wipe EVERYTHING
	@echo "Nuking system..."
	@docker stop $$(docker ps -aq) 2>/dev/null || true
	@docker rm $$(docker ps -aq) 2>/dev/null || true
	@docker volume rm $$(docker volume ls -q) 2>/dev/null || true
	@docker system prune -af --volumes
	@echo "✅ Reset complete."

#  Automatically collect all targets with descriptions for .PHONY
ALL_TARGETS := $(shell grep -E '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) | cut -d: -f1)

.PHONY: $(ALL_TARGETS)