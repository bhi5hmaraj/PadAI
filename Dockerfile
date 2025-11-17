# Build stage for frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend

COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

COPY frontend/ ./
RUN npm run build

# Production stage
FROM python:3.11-slim

# Install bd CLI robustly (detect arch, verify ELF magic)
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends curl ca-certificates; \
    rm -rf /var/lib/apt/lists/*; \
    arch="$(dpkg --print-architecture || echo amd64)"; \
    uname_m="$(uname -m || echo x86_64)"; \
    base="https://github.com/steveyegge/beads/releases/latest/download"; \
    for name in "bd-linux-$arch" "bd-linux-$uname_m" "bd-linux-amd64" "bd-linux-x86_64" "bd-linux-arm64" "bd-linux-aarch64" "bd-linux" "bd"; do \
      url="$base/$name"; echo "Attempting to download $url"; \
      if curl -fsSL "$url" -o /usr/local/bin/bd; then \
        chmod +x /usr/local/bin/bd || true; \
        if head -c 4 /usr/local/bin/bd | od -An -t x1 | tr -d ' \n' | grep -qi '^7f454c46$'; then \
          echo "bd installed from $url"; \
          /usr/local/bin/bd --help >/dev/null 2>&1 || true; \
          break; \
        else \
          echo "Downloaded file is not an ELF executable; trying next candidate"; \
        fi; \
      fi; \
    done; \
    if ! [ -x /usr/local/bin/bd ] || ! head -c 4 /usr/local/bin/bd | od -An -t x1 | tr -d ' \n' | grep -qi '^7f454c46$'; then \
      echo "ERROR: Failed to install bd CLI"; exit 1; \
    fi

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

# Expose default Cloud Run port (honors PORT env variable at runtime)
EXPOSE 8080

# Health check (simple HTTP GET on root)
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD sh -c 'curl -fsS "http://localhost:${PORT:-8080}/" >/dev/null || exit 1'

# Run server (exec-form recommended for signal handling)
CMD ["python", "-m", "server.main"]
