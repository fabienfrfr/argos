FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential git curl \
    && rm -rf /var/lib/apt/lists/*

RUN useradd -m -u 1001 argos
USER argos
WORKDIR /home/argos

# Install AutoGluon Assistant
RUN pip install --no-cache-dir autogluon.assistant

# Important: expose port
EXPOSE 8000

# Launch MCP server directly (no CLI dependency)
CMD ["python3", "-m", "autogluon.mcp.server.server", "--host", "0.0.0.0", "--port", "8000"]