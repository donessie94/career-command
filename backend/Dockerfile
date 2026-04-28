FROM python:3.12-slim

# Everything inside the container will happen from /app
WORKDIR /app

# Don't write .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# Send Python output straight to terminal without buffering
ENV PYTHONUNBUFFERED=1

# build-essential / gcc:
# Needed for compiling some Python packages if required
#
# libpq-dev:
# PostgreSQL client headers/libs for psycopg and related packages
#
# curl:
# Useful for debugging inside container if needed
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first so Docker can cache dependency installs
COPY requirements.txt /tmp/requirements.txt

# Upgrade pip and install backend dependencies
RUN pip install --upgrade pip && pip install -r /tmp/requirements.txt

# Django dev server will run on 8000
EXPOSE 8000