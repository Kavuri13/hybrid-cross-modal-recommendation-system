# Multi-stage Dockerfile - Unified Frontend + Backend
# Stage 1: Build Frontend
FROM node:18-alpine AS frontend-builder

WORKDIR /app/frontend
COPY frontend/package.json frontend/package-lock.json* ./
RUN npm ci

COPY frontend/ ./
ARG NEXT_PUBLIC_API_URL=/api/v1
ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

# Stage 2: Build Final Image
FROM python:3.10-slim

WORKDIR /app

# Install system dependencies including nginx, supervisor
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    libgomp1 \
    nginx \
    supervisor \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r backend/requirements.txt

# Copy backend code
COPY backend/ ./backend/

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/frontend/.next/standalone ./frontend/
COPY --from=frontend-builder /app/frontend/.next/static ./frontend/.next/static

# Create necessary directories
RUN mkdir -p /app/data/images /app/index /var/log/supervisor

# Configure nginx
COPY nginx/nginx.unified.conf /etc/nginx/nginx.conf

# Configure supervisord
RUN printf '[supervisord]\n\
nodaemon=true\n\
logfile=/var/log/supervisor/supervisord.log\n\
pidfile=/var/run/supervisord.pid\n\
\n\
[program:backend]\n\
command=uvicorn app.main:app --host 127.0.0.1 --port 8000 --workers 2\n\
directory=/app/backend\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/supervisor/backend.err.log\n\
stdout_logfile=/var/log/supervisor/backend.out.log\n\
\n\
[program:frontend]\n\
command=node server.js\n\
directory=/app/frontend\n\
autostart=true\n\
autorestart=true\n\
environment=PORT="3000",HOSTNAME="127.0.0.1",NODE_ENV="production"\n\
stderr_logfile=/var/log/supervisor/frontend.err.log\n\
stdout_logfile=/var/log/supervisor/frontend.out.log\n\
\n\
[program:nginx]\n\
command=/usr/sbin/nginx -g "daemon off;"\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/supervisor/nginx.err.log\n\
stdout_logfile=/var/log/supervisor/nginx.out.log\n\
' > /etc/supervisor/conf.d/supervisord.conf

# Expose port 80 (nginx)
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD curl -f http://localhost/api/v1/health || exit 1

# Run supervisord
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
