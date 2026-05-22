# argos

Autonomous local ML assistant powered by **AutoGluon** and **Hermes**.

## Quick Start

1. **Start services:**
```bash
docker compose up -d
```


2. **Pull the model:**
   ```bash
   docker exec -it argos-ollama ollama pull qwen3.5:9b
```

3. **Access interface:**
Open http://localhost:8080 in your browser.

**Testing**

docker logs argos-hermes
docker exec -it argos-hermes hermes chat
curl http://localhost:11434/api/tags

## Components

* **Ollama:** LLM runtime.
* **MLZero (AutoGluon):** MCP tool server.
* **Hermes:** Agent orchestration.

## Configuration

All services are managed via docker-compose.yml. Use .env for custom environment variables.