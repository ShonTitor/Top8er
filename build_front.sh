#!/bin/bash

# Navigate to the frontend directory
cd frontend

# Install the required Node packages (uses lockfile exactly)
npm ci

# Build the frontend assets
npm run build

# Clear old assets and copy the new build
rm -rf ../static/assets
mkdir -p ../static/assets
cp -r dist/assets/* ../static/assets

echo "Frontend build complete and assets copied to static folder."
