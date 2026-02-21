#!/bin/bash
# Start both the backend and frontend for StudyDash

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "========================================="
echo "  StudyDash - Starting Application"
echo "========================================="

# Start backend
echo "[1/2] Starting Flask backend..."
cd "$PROJECT_DIR/backend"
./venv/bin/python app.py &
BACKEND_PID=$!
echo "       Backend PID: $BACKEND_PID"

# Start frontend
echo "[2/2] Starting React frontend..."
cd "$PROJECT_DIR/frontend"
npm run dev &
FRONTEND_PID=$!
echo "       Frontend PID: $FRONTEND_PID"

# Save PIDs so stop.sh can find them
echo "$BACKEND_PID" > "$PROJECT_DIR/.backend.pid"
echo "$FRONTEND_PID" > "$PROJECT_DIR/.frontend.pid"

echo ""
echo "========================================="
echo "  Both servers are running!"
echo "  Backend:  http://localhost:5001"
echo "  Frontend: http://localhost:5173"
echo ""
echo "  Press Ctrl+C to stop both servers"
echo "  Or run: ./stop.sh"
echo "========================================="

# Wait for Ctrl+C, then clean up both
trap "echo ''; echo 'Shutting down...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm -f '$PROJECT_DIR/.backend.pid' '$PROJECT_DIR/.frontend.pid'; echo 'Done.'; exit 0" INT TERM

wait
