#!/bin/bash
# Start Python backend
cd backend
python main.py &

# Start	React frontend
cd ../frontend
npm start

# Additional
cd ../backend
