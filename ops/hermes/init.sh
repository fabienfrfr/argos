#!/bin/bash
set -e

MODEL="wild-llm"
OLLAMA_URL="http://ollama:11434/v1"
MCP_SERVER_NAME="mlzero"
MCP_SERVER_URL="http://mlzero:8000/mcp/"

echo "Waiting for Ollama..."
until curl -s "$OLLAMA_URL/models" > /dev/null; do sleep 2; done

echo "Waiting for MCP..."
until curl -s "$MCP_SERVER_URL" > /dev/null; do sleep 2; done

# Install agent if missing (idempotent)
if [ ! -d "/home/argos/.hermes/hermes-agent" ]; then
    echo "Installing hermes-agent repo..."
    git clone https://github.com/NousResearch/hermes-agent \
        /home/argos/.hermes/hermes-agent
fi



# Config
hermes config set model.provider custom
hermes config set model.base_url "$OLLAMA_URL"
hermes config set model.default "$MODEL"
hermes config set model.extra_body '{"chat_template_kwargs": {"enable_thinking": false}}'

# Tools whitelist
ALLOWED_TOOLS="terminal file code_execution memory"

hermes tools list | grep "✓ enabled" | awk '{print $3}' | while read tool; do
    if [[ ! " $ALLOWED_TOOLS " =~ " $tool " ]]; then
        hermes tools disable "$tool" 2>/dev/null || true
    fi
done

# MCP (idempotent strict)
if ! hermes mcp list | awk '{print $1}' | grep -qx "$MCP_SERVER_NAME"; then
    printf "n\ny\n" | hermes mcp add "$MCP_SERVER_NAME" --url "$MCP_SERVER_URL"
fi

# API
hermes config set API_SERVER_ENABLED true
hermes config set API_SERVER_KEY "$HERMES_API_KEY"
hermes config set API_SERVER_PORT 8642

# WebUI
export HERMES_WEBUI_CHAT_BACKEND=gateway
export HERMES_WEBUI_GATEWAY_BASE_URL=http://localhost:8642
export HERMES_WEBUI_GATEWAY_API_KEY=$HERMES_API_KEY
export HERMES_WEBUI_AGENT_DIR=/home/argos/.hermes/hermes-agent
export HERMES_WEBUI_HOST=0.0.0.0


# Launch Gateway and WebUI
hermes gateway run &
cd /home/argos/webui
python3 server.py
