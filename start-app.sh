#!/bin/bash
# Launcher script used by StudyDash.app — sets up the proper environment
# and starts both backend and frontend as background processes.

export PATH="/opt/homebrew/bin:/opt/homebrew/sbin:/Library/Frameworks/Python.framework/Versions/3.12/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

PROJECT_DIR="/Users/waiwai/Desktop/Plan"
LOG_DIR="$PROJECT_DIR/backend/data"
mkdir -p "$LOG_DIR"

# Kill any existing processes on our ports to avoid conflicts
kill $(lsof -ti:5001) 2>/dev/null
kill $(lsof -ti:5173) 2>/dev/null
sleep 1

# Start backend
cd "$PROJECT_DIR/backend"
nohup ./venv/bin/python app.py > "$LOG_DIR/backend.log" 2>&1 &
BACKEND_PID=$!

# Start frontend
cd "$PROJECT_DIR/frontend"
nohup npm run dev > "$LOG_DIR/frontend.log" 2>&1 &
FRONTEND_PID=$!

# Verify processes launched successfully
sleep 1
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "Backend failed to start. Check $LOG_DIR/backend.log" >&2
    exit 1
fi

if ! kill -0 $FRONTEND_PID 2>/dev/null; then
    echo "Frontend failed to start. Check $LOG_DIR/frontend.log" >&2
    exit 1
fi

echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
