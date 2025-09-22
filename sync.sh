#!/bin/bash
# save as deploy-and-run.sh

PI_USER="bobvork"
PI_HOST="rpizero"
PI_PROJECT_DIR="/home/bobvork/weather"
LOCAL_PROJECT_DIR="./src"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}Syncing code to Pi...${NC}"
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' --exclude='.venv' \
  $LOCAL_PROJECT_DIR $PI_USER@$PI_HOST:$PI_PROJECT_DIR/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Sync completed successfully${NC}"
    echo -e "${BLUE}Executing on Pi...${NC}"
    
    # Execute your code - adjust this line based on your project type
    ssh $PI_USER@$PI_HOST "cd $PI_PROJECT_DIR && python3 run.py"
    
else
    echo "Sync failed, not executing"
    exit 1
fi
