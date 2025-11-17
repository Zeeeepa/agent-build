#!/bin/bash
# Don't use set -e

# DBX SDK template: Install dependencies
# This template has package.json with custom install script for frontend

echo "Installing dependencies..." >&2

if [ ! -f "package.json" ]; then
    echo "❌ No package.json found" >&2
    exit 1
fi

# Install root dependencies (skip custom install script to avoid frontend issues)
if npm install --ignore-scripts 2>&1 >/dev/null; then
    # Install frontend dependencies if frontend exists
    if [ -d "frontend" ]; then
        cd frontend && npm install 2>&1 >/dev/null && cd .. || true
    fi
    echo "✅ Dependencies installed" >&2
    exit 0
else
    echo "❌ Dependency installation failed" >&2
    exit 1
fi
