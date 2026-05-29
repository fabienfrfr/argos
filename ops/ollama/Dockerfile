FROM ollama/ollama:latest

# Create non-root user
RUN useradd -m -u 1001 argos

# Install curl
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

# Prepare directory with correct permissions
RUN mkdir -p /home/argos/.ollama && chown -R argos:argos /home/argos

WORKDIR /home/argos

COPY init.sh /home/argos/init.sh
RUN chmod +x /home/argos/init.sh

USER argos

ENTRYPOINT ["/bin/bash", "/home/argos/init.sh"]