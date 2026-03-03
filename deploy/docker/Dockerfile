FROM node:22-slim

# Install OpenClaw globally
RUN npm install -g @anthropic/openclaw && \
    mkdir -p /home/node/.openclaw/workspace

# Copy workspace files
COPY --chown=node:node . /home/node/.openclaw/workspace/

USER node
WORKDIR /home/node/.openclaw/workspace

EXPOSE 18789

ENTRYPOINT ["openclaw", "gateway", "start", "--foreground"]
