#!/bin/bash
#
# Quick Start Script for agent-build Enterprise Setup
# ===================================================
# 
# This script will:
# 1. Clone the repository
# 2. Checkout the tested PR branch
# 3. Run the enterprise setup script
#
# Usage: bash quick_start.sh
#

set -e  # Exit on error

echo "=================================="
echo "agent-build Enterprise Setup"
echo "Quick Start Script"
echo "=================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
REPO_URL="https://github.com/Zeeeepa/agent-build.git"
BRANCH="codegen-bot/code-quality-analysis-1763105613"
CLONE_DIR="agent-build"

# Step 1: Clone repository
echo -e "${BLUE}Step 1/3: Cloning repository...${NC}"
if [ -d "$CLONE_DIR" ]; then
    echo -e "${YELLOW}Directory $CLONE_DIR already exists. Using existing directory.${NC}"
    cd "$CLONE_DIR"
    git fetch origin
else
    git clone "$REPO_URL" "$CLONE_DIR"
    cd "$CLONE_DIR"
fi
echo -e "${GREEN}✓ Repository ready${NC}"
echo ""

# Step 2: Checkout PR branch
echo -e "${BLUE}Step 2/3: Checking out PR branch...${NC}"
git checkout "$BRANCH"
echo -e "${GREEN}✓ Branch checked out: $BRANCH${NC}"
echo ""

# Step 3: Display options
echo -e "${BLUE}Step 3/3: Ready to run enterprise setup!${NC}"
echo ""
echo "Available commands:"
echo ""
echo "  1. Run system tests (recommended first):"
echo "     ${GREEN}python3 enterprise_setup.py --test${NC}"
echo ""
echo "  2. Show help and all options:"
echo "     ${GREEN}python3 enterprise_setup.py --help${NC}"
echo ""
echo "  3. Show version:"
echo "     ${GREEN}python3 enterprise_setup.py --version${NC}"
echo ""
echo "  4. Create a backup:"
echo "     ${GREEN}python3 enterprise_setup.py --backup${NC}"
echo ""
echo "  5. List available backups:"
echo "     ${GREEN}python3 enterprise_setup.py --list-backups${NC}"
echo ""
echo "=================================="
echo ""

# Offer to run tests
read -p "Would you like to run system tests now? [Y/n] " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] || [[ -z $REPLY ]]; then
    echo ""
    echo -e "${GREEN}Running system tests...${NC}"
    echo ""
    python3 enterprise_setup.py --test
    echo ""
    echo -e "${GREEN}✓ Tests complete!${NC}"
    echo ""
    echo "Next steps:"
    echo "  - Run full setup (coming soon in full version)"
    echo "  - Check documentation: cat README.md"
    echo "  - View PR: https://github.com/Zeeeepa/agent-build/pull/1"
else
    echo ""
    echo "Skipped tests. You can run them later with:"
    echo "  ${GREEN}python3 enterprise_setup.py --test${NC}"
fi

echo ""
echo -e "${GREEN}Setup complete! 🎉${NC}"
echo ""
echo "You are now in: $(pwd)"
echo "Current branch: $(git branch --show-current)"
echo ""
