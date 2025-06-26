#!/bin/bash

# Build the frontend
cd frontend
npm install
npm run build

# Move the built frontend to backend directory
cd ..
mkdir -p backend/frontend
cp -r frontend/dist/* backend/frontend/

echo "Build complete! Frontend built and moved to backend/frontend/" 