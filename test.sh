#!/bin/bash
# Run backend tests inside the Docker container
echo "Running tests in the labpilot-api container..."
docker compose exec api pytest "$@"
