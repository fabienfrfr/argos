# argos

Autonomous local ML assistant powered by **Hermes**, **Ollama**, and **AutoGluon (MLZero)**. 

> **🚧 WORK IN PROGRESS** 

## Overview

Argos is a self-hosted agent system that combines:

* **Hermes** → agent orchestration + Web UI
* **Ollama** → local LLM inference (with Vulkan)
* **MLZero (AutoGluon MCP)** → ML/Data tool server

Everything runs locally via Docker.



## Quick Start

### 1. Start services (First time)

```bash
docker compose up -d --build
```




### 2. Open the interface

```
http://localhost:8787
```


## Basic Checks

```bash
# Hermes logs
docker logs argos-hermes

# Direct agent CLI
docker exec -it argos-hermes hermes chat

# Ollama API
curl http://localhost:11434/api/tags

# Run model directly
docker exec -it argos-ollama ollama run wild-llm --think=false
```



## Key Design Choices

* **Single container for Hermes + WebUI**
  * avoids agent detection issues
  * keeps state consistent (`~/.hermes`)
* **Shared state volume**
  * persistent memory, config, skills
* **Gateway-based communication**
  * WebUI talks to Hermes via API (`:8642`)



## Configuration

* `.env` → runtime variables
* `docker-compose.yml` → orchestration
* `ops/*` → service definitions

