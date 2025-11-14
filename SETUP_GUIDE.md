# agent-build Setup Guide with Z.ai Integration

**Complete guide for setting up agent-build with Claude Code using Z.ai API**

---

## Table of Contents
1. [System Architecture & Data Flows](#1-system-architecture--data-flows)
2. [Required Environment Variables](#2-required-environment-variables)
3. [Z.ai Configuration](#3-zai-configuration)
4. [Installation Steps](#4-installation-steps)
5. [Usage Examples](#5-usage-examples)
6. [Troubleshooting](#6-troubleshooting)

---

## 1. System Architecture & Data Flows

### 1.1 Complete Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│  "Generate a Databricks dashboard for sales analytics"          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE                                   │
│  - Interprets user intent                                        │
│  - Uses Z.ai API (glm-4.6 model)                                │
│  - Decides to call MCP tool: scaffold_data_app                  │
└────────────────────────┬────────────────────────────────────────┘
                         │ MCP Protocol (JSON-RPC over stdio)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    EDDA_MCP SERVER                               │
│  - Receives tool call via stdin                                  │
│  - Authenticates with environment variables                      │
│  - Routes to appropriate handler                                 │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              DATABRICKS SCHEMA DISCOVERY                         │
│  1. databricks_list_tables → Get table names                    │
│  2. databricks_describe_table → Get columns & types             │
│  3. databricks_query → Sample data for validation               │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 TEMPLATE SELECTION                               │
│  - Choose: React + TypeScript + tRPC + Drizzle                 │
│  - Load templates from edda_templates/                          │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              DAGGER SANDBOX (CODE GENERATION)                    │
│  - Create isolated container                                     │
│  - Fill templates with schema-specific code:                    │
│    • Generate Drizzle ORM schemas                               │
│    • Create tRPC routers (one per table)                        │
│    • Generate React components (tables, forms)                  │
│    • Add tests and deployment config                            │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              VALIDATION PIPELINE (9 METRICS)                     │
│  ✓ 1. Build Success (npm run build)                            │
│  ✓ 2. Runtime (server starts)                                  │
│  ✓ 3. Type Safety (no 'any' types)                             │
│  ✓ 4. Tests Pass (npm test)                                    │
│  ✓ 5. DB Connectivity (connects to Databricks)                 │
│  ✓ 6. Data Returned (queries execute)                          │
│  ✓ 7. UI Renders (Playwright checks)                           │
│  ✓ 8. Runnable Locally (npm run dev works)                     │
│  ✓ 9. Deployable (databricks bundle deploy)                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                 EVENT STORE (edda_mq)                            │
│  - Record all generation steps                                   │
│  - Enable replay for debugging                                   │
│  - Audit trail for compliance                                    │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│               RESPONSE TO CLAUDE CODE                            │
│  - Generated application code                                    │
│  - Validation report (9 metrics)                                │
│  - Deployment instructions                                       │
└────────────────────────┬────────────────────────────────────────┘
                         │ MCP Protocol (JSON-RPC over stdio)
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE                                   │
│  - Presents results to user                                      │
│  - Offers to deploy or make modifications                       │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         USER                                     │
│  - Reviews generated application                                 │
│  - Approves deployment or requests changes                       │
└─────────────────────────────────────────────────────────────────┘
```

### 1.2 Multi-Agent Flow (Cost Optimization)

When exploring Databricks schemas, agent-build uses a **specialist agent** to reduce costs:

```
┌─────────────────────────────────────────────────────────────────┐
│              MAIN AGENT (Claude Opus / glm-4.6)                 │
│  - High-quality generation                                       │
│  - Expensive per token                                           │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ "Need to explore Databricks tables"
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│         SPECIALIST AGENT (Claude Haiku / glm-4.5-air)           │
│  - Fast exploration                                              │
│  - Cheap per token (70% cost reduction)                         │
│  - Lists tables, describes schemas                              │
└────────────────────────┬────────────────────────────────────────┘
                         │
                         │ Returns: Schema information
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────┐
│              MAIN AGENT (Claude Opus / glm-4.6)                 │
│  - Uses schema to generate high-quality code                    │
└─────────────────────────────────────────────────────────────────┘
```

**Configuration:**
- Main agent: `glm-4.6` (ANTHROPIC_DEFAULT_OPUS_MODEL)
- Specialist: `glm-4.5-air` (ANTHROPIC_DEFAULT_HAIKU_MODEL)

---

## 2. Required Environment Variables

### 2.1 Z.ai API Configuration (REQUIRED)

```bash
# Z.ai API Authentication
export ANTHROPIC_AUTH_TOKEN="YOUR_Z_AI_API_KEY_HERE"
# ⚠️ SECURITY: This is your Z.ai API key. Keep it secret!
# Purpose: Authenticates Claude Code with Z.ai API
# Used by: Claude Code → Z.ai API calls

# Z.ai Base URL
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
# Purpose: Routes Anthropic API calls to Z.ai instead
# Used by: Claude Code API client

# API Timeout
export API_TIMEOUT_MS="3000000"
# Purpose: 3000 seconds (50 minutes) timeout for long-running operations
# Used by: HTTP client in Claude Code
# Why so long: Code generation can take 30-60 seconds + validation
```

### 2.2 Model Mappings (REQUIRED for multi-agent)

```bash
# Default model for "Claude Opus" requests
export ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.6"
# Purpose: Map "opus" requests to Z.ai's glm-4.6 model
# Used by: Main agent for high-quality generation

# Default model for "Claude Sonnet" requests
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.6"
# Purpose: Map "sonnet" requests to glm-4.6
# Used by: Fallback for medium-quality tasks

# Default model for "Claude Haiku" requests
export ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"
# Purpose: Map "haiku" requests to glm-4.5-air (cheaper, faster)
# Used by: Specialist agent for Databricks exploration
```

### 2.3 GitHub Integration (REQUIRED for deployment)

```bash
# GitHub Personal Access Token
export GITHUB_TOKEN="YOUR_GITHUB_PAT_HERE"
# ⚠️ SECURITY: This is your GitHub PAT. Keep it secret!
# Purpose: Push generated code, create repositories
# Used by: edda_mcp when deploying apps
# Scopes needed: repo (full control)
```

### 2.4 Databricks Configuration (REQUIRED for data apps)

```bash
# Databricks Workspace URL
export DATABRICKS_HOST="https://your-workspace.databricks.com"
# Purpose: Connect to your Databricks workspace
# Used by: edda_integrations/databricks.rs
# Example: https://adb-1234567890123456.7.azuredatabricks.net

# Databricks Authentication Token
export DATABRICKS_TOKEN="YOUR_DATABRICKS_TOKEN_HERE"
# ⚠️ SECURITY: This is your Databricks PAT. Keep it secret!
# Purpose: Authenticate with Databricks SQL API
# Used by: databricks_query, databricks_list_tables tools
# How to get: User Settings → Access Tokens → Generate New Token

# Databricks SQL Warehouse ID (OPTIONAL)
export DATABRICKS_WAREHOUSE_ID="1234567890abcdef"
# Purpose: Specify which SQL warehouse to use
# Used by: SQL query execution
# How to get: SQL Warehouses → Click warehouse → Copy ID from URL
# If not set: Uses default warehouse
```

### 2.5 Logging & Debugging (OPTIONAL)

```bash
# Rust Logging Level
export RUST_LOG="edda=debug,edda_mcp=trace"
# Purpose: Control verbosity of edda_mcp logs
# Levels: error, warn, info, debug, trace
# Used by: tracing framework in Rust
# Default: info

# Event Store Location (OPTIONAL)
export EDDA_EVENT_STORE_PATH="/path/to/event_store.db"
# Purpose: Customize SQLite database location
# Used by: edda_mq event store
# Default: ~/.local/share/edda/events.db
```

### 2.6 Environment Variables Summary

| Variable | Required | Purpose | Default |
|----------|----------|---------|---------|
| `ANTHROPIC_AUTH_TOKEN` | ✅ Yes | Z.ai API authentication | None |
| `ANTHROPIC_BASE_URL` | ✅ Yes | Route to Z.ai API | None |
| `API_TIMEOUT_MS` | ⚠️ Recommended | Prevent timeout on long operations | 60000 |
| `ANTHROPIC_DEFAULT_OPUS_MODEL` | ⚠️ Recommended | Main agent model | claude-opus-3 |
| `ANTHROPIC_DEFAULT_SONNET_MODEL` | ⚠️ Recommended | Medium tasks model | claude-sonnet-3.5 |
| `ANTHROPIC_DEFAULT_HAIKU_MODEL` | ⚠️ Recommended | Specialist agent model | claude-haiku-3 |
| `GITHUB_TOKEN` | ✅ Yes | Push code, create repos | None |
| `DATABRICKS_HOST` | ✅ Yes* | Databricks workspace URL | None |
| `DATABRICKS_TOKEN` | ✅ Yes* | Databricks authentication | None |
| `DATABRICKS_WAREHOUSE_ID` | ❌ No | SQL warehouse ID | Auto-detect |
| `RUST_LOG` | ❌ No | Logging verbosity | info |
| `EDDA_EVENT_STORE_PATH` | ❌ No | Event store location | ~/.local/share/edda/ |

*Required only for Databricks data applications

---

## 3. Z.ai Configuration

### 3.1 What is Z.ai?

Z.ai is a **proxy service** that:
- Provides access to advanced Chinese AI models (GLM-4.6, GLM-4.5-air)
- Implements Anthropic API compatibility
- Allows using these models with tools expecting Claude API

**Model Comparison:**

| Model | Z.ai Name | Anthropic Equivalent | Use Case |
|-------|-----------|---------------------|----------|
| GLM-4.6 | `glm-4.6` | Claude Opus 3 | High-quality generation |
| GLM-4.5 | `glm-4.5` | Claude Sonnet 3.5 | Medium tasks |
| GLM-4.5-air | `glm-4.5-air` | Claude Haiku 3 | Fast, cheap tasks |

### 3.2 Setting Up Z.ai Environment

**Option 1: Shell Configuration (~/.bashrc or ~/.zshrc)**

```bash
# Add to ~/.bashrc or ~/.zshrc
# Z.ai Claude Code Configuration
export ANTHROPIC_AUTH_TOKEN="YOUR_Z_AI_API_KEY_HERE"
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export API_TIMEOUT_MS="3000000"

# Model mappings
export ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.6"
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"

# GitHub
export GITHUB_TOKEN="YOUR_GITHUB_PAT_HERE"

# Databricks
export DATABRICKS_HOST="https://your-workspace.databricks.com"
export DATABRICKS_TOKEN="dapi1234567890abcdef"
export DATABRICKS_WAREHOUSE_ID="1234567890abcdef"  # Optional

# Reload configuration
source ~/.bashrc  # or source ~/.zshrc
```

**Option 2: .env File (Project-specific)**

```bash
# Create .env in your project root
cat > .env << 'ENVFILE'
# Z.ai Configuration
ANTHROPIC_AUTH_TOKEN=YOUR_Z_AI_API_KEY_HERE
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic
API_TIMEOUT_MS=3000000

# Model Mappings
ANTHROPIC_DEFAULT_OPUS_MODEL=glm-4.6
ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.6
ANTHROPIC_DEFAULT_HAIKU_MODEL=glm-4.5-air

# GitHub
GITHUB_TOKEN=YOUR_GITHUB_PAT_HERE

# Databricks
DATABRICKS_HOST=https://your-workspace.databricks.com
DATABRICKS_TOKEN=dapi1234567890abcdef
DATABRICKS_WAREHOUSE_ID=1234567890abcdef
ENVFILE

# Load .env file
export $(cat .env | xargs)
```

**Option 3: direnv (Automatic loading)**

```bash
# Install direnv
# macOS: brew install direnv
# Linux: apt-get install direnv

# Add to shell config
echo 'eval "$(direnv hook bash)"' >> ~/.bashrc  # or zsh

# Create .envrc in project
cat > .envrc << 'ENVFILE'
export ANTHROPIC_AUTH_TOKEN="YOUR_Z_AI_API_KEY_HERE"
export ANTHROPIC_BASE_URL="https://api.z.ai/api/anthropic"
export API_TIMEOUT_MS="3000000"
export ANTHROPIC_DEFAULT_OPUS_MODEL="glm-4.6"
export ANTHROPIC_DEFAULT_SONNET_MODEL="glm-4.6"
export ANTHROPIC_DEFAULT_HAIKU_MODEL="glm-4.5-air"
export GITHUB_TOKEN="YOUR_GITHUB_PAT_HERE"
export DATABRICKS_HOST="https://your-workspace.databricks.com"
export DATABRICKS_TOKEN="dapi1234567890abcdef"
ENVFILE

# Allow direnv to load .envrc
direnv allow
```

### 3.3 Verifying Z.ai Configuration

```bash
# Test that environment variables are set
echo $ANTHROPIC_AUTH_TOKEN | head -c 10  # Should print: 665b963943
echo $ANTHROPIC_BASE_URL  # Should print: https://api.z.ai/api/anthropic
echo $ANTHROPIC_DEFAULT_OPUS_MODEL  # Should print: glm-4.6

# Test Z.ai API directly (optional)
curl -X POST https://api.z.ai/api/anthropic/v1/messages \
  -H "x-api-key: $ANTHROPIC_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "glm-4.6",
    "max_tokens": 100,
    "messages": [{"role": "user", "content": "Hello"}]
  }'
# Should return JSON with model response
```

