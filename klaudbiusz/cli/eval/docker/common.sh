#!/bin/bash

# Common functions for Docker eval scripts

install_dependencies() {
    echo "Ensuring dependencies are installed..." >&2

    # Check if root package.json has install:all script (trpc style)
    if [ -f "package.json" ] && grep -q '"install:all"' package.json 2>/dev/null; then
        echo "Running npm run install:all..." >&2
        npm run install:all >&2 || { echo "❌ Failed to install dependencies" >&2; exit 1; }
    elif [ -f "package.json" ] && [ ! -d "node_modules" ]; then
        # Root-level app (dbx-sdk style)
        echo "Installing dependencies..." >&2
        npm install >&2 || { echo "❌ Failed to install dependencies" >&2; exit 1; }
    else
        # Install server/client separately if they exist
        if [ -d "server" ] && [ -f "server/package.json" ] && [ ! -d "server/node_modules" ]; then
            echo "Installing server dependencies..." >&2
            cd server && npm install >&2 && cd .. || { echo "❌ Failed to install server dependencies" >&2; exit 1; }
        fi

        if [ -d "client" ] && [ -f "client/package.json" ] && [ ! -d "client/node_modules" ]; then
            echo "Installing client dependencies..." >&2
            cd client && npm install >&2 && cd .. || { echo "❌ Failed to install client dependencies" >&2; exit 1; }
        fi
    fi
}
