#!/bin/bash
# save as deploy-and-run.sh

PI_USER="bobvork"
PI_HOST="rpizero"
PI_PROJECT_DIR="/home/bobvork/weather"
LOCAL_PROJECT_DIR="."

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Parse command line arguments
RUN_SCRIPT=false
if [[ "$1" == "--run" ]]; then
    RUN_SCRIPT=true
fi

echo -e "${BLUE}Syncing code to Pi...${NC}"
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' --exclude='.venv' \
  $LOCAL_PROJECT_DIR $PI_USER@$PI_HOST:$PI_PROJECT_DIR/

if [ $? -eq 0 ]; then
    echo -e "${GREEN}Sync completed successfully${NC}"

    if [ "$RUN_SCRIPT" = true ]; then
        echo -e "${BLUE}Executing on Pi...${NC}"
    
        # Execute your code - adjust this line based on your project type
        ssh $PI_USER@$PI_HOST "cd $PI_PROJECT_DIR && python3 src/run.py"
    else
        echo -e "${GREEN}Sync only - use --run flag to execute${NC}"
    fi
    
else
    echo "Sync failed, not executing"
    exit 1
fi
