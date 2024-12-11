#!/bin/bash

# Navigate to the frontend directory
cd frontend

# Install the required Node packages
npm install

# Build the frontend assets
npm run build

# Ensure the static/assets directory exists
mkdir -p ../static/assets

# Copy the built assets to the static folder
cp -r dist/assets/* ../static/assets

echo "Frontend build complete and assets copied to static folder."