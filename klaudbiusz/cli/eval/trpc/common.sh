#!/bin/bash

# Common functions for tRPC eval scripts

install_dependencies() {
    echo "Ensuring dependencies are installed..." >&2

    # Check if root package.json has install:all script
    if [ -f "package.json" ] && grep -q '"install:all"' package.json 2>/dev/null; then
        echo "Running npm run install:all..." >&2
        npm run install:all >&2 || { echo "❌ Failed to install dependencies" >&2; exit 1; }
    else
        # Install server dependencies if needed
        if [ -d "server" ] && [ -f "server/package.json" ]; then
            if [ ! -d "server/node_modules" ]; then
                echo "Installing server dependencies..." >&2
                cd server && npm install >&2 && cd .. || { echo "❌ Failed to install server dependencies" >&2; exit 1; }
            fi
        fi

        # Install client dependencies if needed (try both client/ and frontend/)
        if [ -d "client" ] && [ -f "client/package.json" ]; then
            if [ ! -d "client/node_modules" ]; then
                echo "Installing client dependencies..." >&2
                cd client && npm install >&2 && cd .. || { echo "❌ Failed to install client dependencies" >&2; exit 1; }
            fi
        elif [ -d "frontend" ] && [ -f "frontend/package.json" ]; then
            if [ ! -d "frontend/node_modules" ]; then
                echo "Installing frontend dependencies..." >&2
                cd frontend && npm install >&2 && cd .. || { echo "❌ Failed to install frontend dependencies" >&2; exit 1; }
            fi
        fi
    fi
}
