FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl git build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user & workdir
RUN useradd -m -u 1001 argos && \
    mkdir -p /home/argos/.hermes && \
    chown -R argos:argos /home/argos
WORKDIR /home/argos


# Install Hermes + WebUI
RUN pip install --no-cache-dir -U mcp hermes-agent aiohttp websockets
# Clone WebUI
RUN git clone https://github.com/nesquena/hermes-webui.git /home/argos/webui


ENV PATH="/home/argos/.local/bin:${PATH}"

COPY init.sh /home/argos/init.sh
RUN chmod +x /home/argos/init.sh

USER argos

ENTRYPOINT ["/bin/bash", "/home/argos/init.sh"]