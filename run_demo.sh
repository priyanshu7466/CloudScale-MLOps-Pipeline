#!/bin/bash
# Simple demo commands (run locally after configuring .env)
echo "Starting demo..."
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
