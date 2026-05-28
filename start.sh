#!/bin/sh
set -e

# Start kagimcp on internal port 8081
kagimcp --http --host 0.0.0.0 --port 8081 &

# Wait for kagimcp to be ready
sleep 3

# Start proxy on Railway's $PORT (default 8080)
exec uvicorn proxy:app --host 0.0.0.0 --port "${PORT:-8080}"
