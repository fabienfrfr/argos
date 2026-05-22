FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git build-essential curl && \
    rm -rf /var/lib/apt/lists/*

# Install Hermes and AutoGluon Assistant via pip
RUN pip install --no-cache-dir hermes-agent git+https://github.com/autogluon/autogluon-assistant.git

# Set the working directory
WORKDIR /app

# Copy the init script and ensure it is executable
COPY init.sh /app/init.sh
RUN chmod +x /app/init.sh

# Set the entrypoint to the init script
ENTRYPOINT ["/bin/bash", "/app/init.sh"]