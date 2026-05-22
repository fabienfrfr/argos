#!/bin/bash

# Define the model precisely
MODEL="huihui_ai/qwen3.5-abliterated:2b"

echo "Checking if model ${MODEL} is available..."

# Check if the model is already in the tags list
if ! curl -s http://ollama:11434/api/tags | grep -q "${MODEL}"; then
    echo "Model ${MODEL} not found. Initiating download..."
    
    # Trigger the download
    curl -X POST http://ollama:11434/api/pull -d "{\"name\": \"${MODEL}\"}"
    
    # Wait until the download appears in the tags list
    until curl -s http://ollama:11434/api/tags | grep -q "${MODEL}"; do
        echo "Waiting for model download to complete..."
        sleep 5
    done
fi

echo "Model ${MODEL} is ready."

# Ensure Hermes configuration directory exists
mkdir -p /root/.hermes

# Generate the configuration file for Hermes
echo "model: {provider: custom, base_url: http://ollama:11434/v1, default: '${MODEL}'}" > /root/.hermes/config.yaml

# Launch the Hermes gateway
echo "Starting Hermes gateway..."
hermes gateway run