#!/bin/bash

# --- Configuration ---

# Select model based on env var
if [ "${TEST:-0}" -eq 1 ]; then
  FULL_NAME="huihui_ai/qwen3.5-abliterated:2b"
else
  FULL_NAME="huihui_ai/Qwen3.6-abliterated:35b" # Qwen/Qwen3.6-35B-A3B 
fi

echo "Selected model: $FULL_NAME"

ALIAS="wild-llm"
SYSTEM_PROMPT="You are a direct assistant. Answer concisely and immediately. Immediately follow with a 5-word self-critique."
# SYSTEM_PROMPT="You are a direct assistant. Answer in ONE sentence maximum. If using a tool, provide ONLY the tool call. Otherwise, follow with a 5-word self-critique."

# --- Security Warning ---
echo "--------------------------------------------------------"
echo "⚠️  WARNING: Using $FULL_NAME"
echo "This is an unaligned/de-restricted version of Qwen."
echo "Use responsibly."
echo "--------------------------------------------------------"

# Start the Ollama server in the background
ollama serve &

# Wait until the Ollama API is responsive
until curl -s http://localhost:11434/api/tags > /dev/null; do
    sleep 2
done

# Ensure the base model is pulled ("run" used to get manifest)
echo "Ensuring model $FULL_NAME is pulled..."
ollama run "$FULL_NAME" --think=false "ping" > /dev/null 2>&1

# Create a custom model with the system prompt on the fly
# We use a temporary Modelfile to inject the system instructions
echo "Creating aliased model '$ALIAS' with system prompt..."
echo "FROM $FULL_NAME" > /tmp/Modelfile
echo "SYSTEM \"$SYSTEM_PROMPT\"" >> /tmp/Modelfile

# Remove any existing alias and create the new one
ollama rm "$ALIAS" 2>/dev/null
ollama create "$ALIAS" -f /tmp/Modelfile
rm /tmp/Modelfile

echo "Model ready as: $ALIAS"
echo "Run with nothink : ollama run $ALIAS --think=false"

# Keep the container running
wait