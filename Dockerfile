# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Copy backend code
COPY backend /app/backend

# Install package
RUN pip install --no-cache-dir /app/backend

EXPOSE 8080
CMD ["chatagent", "serve", "--host", "0.0.0.0", "--port", "8080"]
