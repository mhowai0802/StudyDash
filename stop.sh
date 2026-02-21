#!/bin/bash
# Stop the StudyDash backend and frontend

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================="
echo "  StudyDash - Stopping Application"
echo "========================================="

stopped=0

# Kill backend
if [ -f "$PROJECT_DIR/.backend.pid" ]; then
    PID=$(cat "$PROJECT_DIR/.backend.pid")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID" 2>/dev/null
        echo "  Stopped backend (PID $PID)"
        stopped=$((stopped + 1))
    fi
    rm -f "$PROJECT_DIR/.backend.pid"
fi

# Kill frontend
if [ -f "$PROJECT_DIR/.frontend.pid" ]; then
    PID=$(cat "$PROJECT_DIR/.frontend.pid")
    if kill -0 "$PID" 2>/dev/null; then
        kill "$PID" 2>/dev/null
        echo "  Stopped frontend (PID $PID)"
        stopped=$((stopped + 1))
    fi
    rm -f "$PROJECT_DIR/.frontend.pid"
fi

# Fallback: find and kill by port if PID files are missing
if [ $stopped -eq 0 ]; then
    BACKEND_PID=$(lsof -ti:5001 2>/dev/null)
    FRONTEND_PID=$(lsof -ti:5173 2>/dev/null)

    if [ -n "$BACKEND_PID" ]; then
        kill $BACKEND_PID 2>/dev/null
        echo "  Stopped backend on port 5001 (PID $BACKEND_PID)"
        stopped=$((stopped + 1))
    fi

    if [ -n "$FRONTEND_PID" ]; then
        kill $FRONTEND_PID 2>/dev/null
        echo "  Stopped frontend on port 5173 (PID $FRONTEND_PID)"
        stopped=$((stopped + 1))
    fi
fi

if [ $stopped -eq 0 ]; then
    echo "  No running servers found."
else
    echo ""
    echo "  All servers stopped. Your data is safe in the database."
fi

echo "========================================="
