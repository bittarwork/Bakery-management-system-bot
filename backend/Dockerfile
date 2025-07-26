# 🐳 Bakery Backend Dockerfile
# Multi-stage build for production optimization

# Build stage
FROM node:18-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production && npm cache clean --force

# Production stage
FROM node:18-alpine AS production

# Install dumb-init for proper signal handling
RUN apk add --no-cache dumb-init

# Create non-root user
RUN addgroup -g 1001 -S nodejs
RUN adduser -S bakery -u 1001

# Set working directory
WORKDIR /app

# Copy built app from builder stage
COPY --from=builder --chown=bakery:nodejs /app/node_modules ./node_modules
COPY --chown=bakery:nodejs . .

# Create logs and uploads directories
RUN mkdir -p logs uploads && chown -R bakery:nodejs logs uploads

# Switch to non-root user
USER bakery

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
  CMD node healthcheck.js

# Start the application
ENTRYPOINT ["dumb-init", "--"]
CMD ["node", "server.js"] 