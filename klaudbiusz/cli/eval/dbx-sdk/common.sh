#!/bin/bash

# Common functions for DBX SDK eval scripts

install_dependencies() {
    if [ -f "package.json" ]; then
        if [ ! -d "node_modules" ]; then
            echo "Installing dependencies..." >&2
            npm install >&2 || { echo "❌ Failed to install dependencies" >&2; exit 1; }
        fi
    fi
}
