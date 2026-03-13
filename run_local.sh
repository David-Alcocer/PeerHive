#!/bin/bash

# Define colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting PeerHive Locally without Docker${NC}\n"

echo -e "${BLUE}1. Make sure you have MongoDB running locally on mongodb://localhost:27017${NC}"
echo -e "${BLUE}   or update the MONGO_URL in backend/app/main.py / environment variables.${NC}\n"

# Backend
echo -e "${GREEN}Starting backend (FastAPI) on port 8000...${NC}"
cd backend
export MONGO_URL="mongodb://127.0.0.1:27017"
../.venv/bin/uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Frontend
echo -e "${GREEN}Starting frontend on port 3000...${NC}"
python3 -m http.server 3000 &
FRONTEND_PID=$!

echo -e "\n${GREEN}Servicios iniciados!${NC}"
echo -e "🔗 Frontend: http://localhost:3000"
echo -e "🔗 Backend API: http://localhost:8000"
echo -e "\n${BLUE}Presiona Ctrl+C para detener todos los servicios.${NC}"

# Wait for process exit or interrupt
trap "echo -e '\nDeteniendo servicios...'; kill $FRONTEND_PID $BACKEND_PID; exit 0" SIGINT SIGTERM
wait $FRONTEND_PID $BACKEND_PID
