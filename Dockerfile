# Build stage for frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Production stage
FROM python:3.11-slim

# Install bd CLI using official install script
ENV PATH="/root/.local/bin:${PATH}"
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates bash tar xz-utils; \
    rm -rf /var/lib/apt/lists/*; \
    curl -fsSL https://raw.githubusercontent.com/steveyegge/beads/main/scripts/install.sh -o /tmp/install_bd.sh; \
    bash /tmp/install_bd.sh; \
    if ! command -v bd >/dev/null 2>&1; then echo "bd not found in PATH after install"; exit 1; fi; \
    bd --help >/dev/null 2>&1 || true

WORKDIR /app

# Copy backend files
COPY server/requirements.txt ./server/requirements.txt
RUN pip install --no-cache-dir -r ./server/requirements.txt

COPY server/ ./server/

# Copy Beads workspace (if present) into an internal workspace path
COPY .beads /workspace/.beads

# Copy built frontend
COPY --from=frontend-builder /app/frontend/dist ./frontend/dist

# Set workspace path
ENV WORKSPACE_PATH=/workspace
ENV BEADS_DIR=/workspace/.beads
ENV PORT=8080

# Expose default Cloud Run port (honors PORT env variable at runtime)
EXPOSE 8080

# Health check (simple HTTP GET on root)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD sh -c 'curl -fsS "http://localhost:${PORT}/" >/dev/null || exit 1'

# Run server (exec-form recommended for signal handling)
CMD ["python", "-m", "server.main"]
