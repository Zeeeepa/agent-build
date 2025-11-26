#!/bin/bash
set -e

# Validate the app using Playwright tests

# Check if playwright is installed
if ! npx playwright --version >/dev/null 2>&1; then
  echo "❌ Playwright not installed. Installing..." >&2
  npx playwright install --with-deps
fi

# Run Playwright tests (must exist in tests/ or playwright.config.*)
if [ -d "tests" ] || [ -f "playwright.config.ts" ] || [ -f "playwright.config.js" ]; then
  echo "Running Playwright tests..." >&2
  npx playwright test
else
  echo "❌ No Playwright tests or config found." >&2
  exit 1
fi