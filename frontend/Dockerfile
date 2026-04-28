FROM node:22-alpine

# Frontend project files will live in /app inside the container
WORKDIR /app

# Copy package files first for better Docker layer caching
#
# This assumes package.json / package-lock.json will exist after
# bootstrapping the Vite React app.
COPY package*.json ./

# Install frontend dependencies
RUN if [ -f package.json ]; then npm install; else mkdir -p /app; fi

# Vite dev server runs on 5173
EXPOSE 5173