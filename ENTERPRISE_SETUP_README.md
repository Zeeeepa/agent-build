# Enterprise Setup Script - README

**Automated Deployment System for agent-build**

---

## Overview

`enterprise_setup.py` is a comprehensive, production-ready setup script that automates the entire deployment pipeline for agent-build. It handles environment configuration, repository cloning, dependency installation, build processes, and integration testing.

### Key Features

✅ **Interactive Configuration** - Guided prompts for all environment variables  
✅ **Validation** - Real-time validation of credentials and connectivity  
✅ **Multi-Repository** - Clones and analyzes all necessary repositories  
✅ **Automated Build** - Compiles Rust binaries with progress indicators  
✅ **Integration Testing** - Tests Databricks, GitHub, and Z.ai APIs  
✅ **Beautiful CLI** - Colored output with clear progress indicators  
✅ **Error Handling** - Graceful failures with detailed error logs  
✅ **Documentation** - Generates comprehensive deployment reports  

---

## Quick Start

### Prerequisites

- Python 3.7+ (included in most systems)
- Git (for repository cloning)
- Internet connection

### One-Command Setup

```bash
python3 enterprise_setup.py
```

The script will guide you through the entire setup process!

---

## Features Breakdown

### 1. Interactive Environment Configuration

The script prompts for all necessary variables with:
- **Required variables** - Must be provided
- **Optional variables** - Use defaults or customize
- **Secret masking** - Passwords/tokens hidden during input
- **Format validation** - Ensures correct formats (URLs, tokens, etc.)
- **Real-time testing** - Validates Databricks connectivity

**Required Variables:**
- `ANTHROPIC_AUTH_TOKEN` - Z.ai API key
- `ANTHROPIC_BASE_URL` - Z.ai base URL (default provided)
- `GITHUB_TOKEN` - GitHub Personal Access Token
- `DATABRICKS_HOST` - Databricks workspace URL
- `DATABRICKS_TOKEN` - Databricks PAT

**Optional Variables (with defaults):**
- `API_TIMEOUT_MS` - API timeout (default: 3000000)
- `MODEL` - Default LLM model (default: glm-4.6)
- `ANTHROPIC_DEFAULT_OPUS_MODEL` - Main agent model
- `ANTHROPIC_DEFAULT_SONNET_MODEL` - Medium tasks model
- `ANTHROPIC_DEFAULT_HAIKU_MODEL` - Specialist agent model
- `DATABRICKS_WAREHOUSE_ID` - SQL warehouse ID
- `RUST_LOG` - Logging level (default: info)

### 2. Configuration Files Generated

**`.env` File:**
```bash
# agent-build Enterprise Configuration
# Generated: 2025-11-14 13:45:00
# DO NOT COMMIT THIS FILE TO VERSION CONTROL

# === REQUIRED VARIABLES ===

# Z.ai API Key for Claude Code
ANTHROPIC_AUTH_TOKEN=your_token_here

# Z.ai API Base URL
ANTHROPIC_BASE_URL=https://api.z.ai/api/anthropic

# ... (all configured variables)
```

**`.env.example` Template:**
```bash
# agent-build Environment Variables Template
# Copy to .env and fill in your values

# Z.ai API Key for Claude Code
ANTHROPIC_AUTH_TOKEN=

# GitHub Personal Access Token
GITHUB_TOKEN=

# ... (all variables with descriptions)
```

### 3. Workspace Setup

Creates organized workspace structure:

```
~/.agent-build/
├── repos/
│   └── agent-build/         # Cloned repositories
├── logs/
│   └── errors.log          # Error logs
├── documentation_index.json # Documentation catalog
└── deployment_report.md    # Final deployment report
```

### 4. Repository Management

- Clones agent-build repository with `--depth=1` for speed
- Updates existing repositories with `git pull`
- Analyzes all documentation files (README.md, docs/, etc.)
- Generates documentation index JSON

### 5. Dependency Checking

Verifies presence of:
- **Rust/Cargo** - For building MCP server
- **Docker** - For Dagger sandbox execution

Provides installation instructions if missing.

### 6. Automated Build Process

```
Building edda_mcp server...
⚠ This may take 5-10 minutes on first build...
✓ Installed edda_mcp to ~/.local/bin/edda_mcp
```

- Compiles Rust with `cargo build --release`
- 10-minute timeout protection
- Installs binary to `~/.local/bin/`
- Makes binary executable

### 7. Integration Testing

Tests three critical integrations:

**Databricks:**
```
✓ Databricks: ✓ (3 catalogs)
```
- Lists Unity Catalog catalogs
- Validates authentication
- Confirms warehouse access

**GitHub:**
```
✓ GitHub: ✓ (user: username)
```
- Validates PAT
- Retrieves username
- Confirms API access

**Z.ai API:**
```
✓ Z.ai API: ✓
```
- Tests API endpoint
- Validates authentication
- Confirms model access

### 8. Deployment Report

Generates comprehensive markdown report:

```markdown
# agent-build Enterprise Deployment Report

**Generated:** 2025-11-14 13:45:00

## Configuration
- Variables configured: 12
- Workspace: ~/.agent-build
- Repositories: 1

## Setup Log
- [13:40:15] Collected ANTHROPIC_AUTH_TOKEN
- [13:40:30] Databricks connection validated
- [13:42:00] Cloned agent-build
- [13:50:45] Built and installed edda_mcp
- [13:51:10] Integration tests: 3/3 passed

## Next Steps
1. Run Claude Code with MCP integration
2. Generate your first data application
3. Deploy to Databricks
```

---

## Usage Examples

### Example 1: First-Time Setup

```bash
$ python3 enterprise_setup.py

================================================================================
                       agent-build Enterprise Setup                           
================================================================================

Welcome to the automated deployment system!

▶ Step 1: Collecting environment variables

Required Variables:

ANTHROPIC_AUTH_TOKEN (secret)
  Z.ai API Key for Claude Code
  > ************************************

ANTHROPIC_BASE_URL [https://api.z.ai/api/anthropic]
  Z.ai API Base URL
  > (press Enter for default)

... (continues for all variables)

✓ Collected 12 environment variables

▶ Step 2: Validating configuration
✓ Databricks: Connected! Found 3 catalogs
✓ Configuration validated successfully

... (continues through all steps)

================================================================================
                           🎉 Deployment Complete!                            
================================================================================

Deployment Summary:
  Configuration: ✓ 12 variables
  Repositories:  ✓ 1 cloned
  Workspace:     ✓ ~/.agent-build
  Report:        ✓ ~/.agent-build/deployment_report.md

Next Steps:
  1. Source environment: source .env
  2. Test edda_mcp: edda_mcp --help
  3. Generate app: See documentation in workspace

Happy building! 🚀
```

### Example 2: With Existing Configuration

If `.env` already exists or you're running again:
- Prompts allow you to update values
- Existing repositories are updated via `git pull`
- Build skipped if binary already exists

### Example 3: Error Handling

```bash
▶ Step 2: Validating configuration
⚠ Databricks connection test failed: 401 Unauthorized
✗ Configuration validation failed:
  - Databricks: 401 Unauthorized

✗ Setup failed: Configuration validation failed
```

Errors are:
- Clearly displayed with context
- Logged to `~/.agent-build/logs/errors.log`
- Cause setup to exit gracefully

---

## Advanced Usage

### Skip Build (If Already Built)

The script automatically detects if `edda_mcp` exists and skips the build if Rust/Cargo is not available.

### Environment Variables Priority

1. Interactive prompts (highest priority)
2. Default values in script
3. Empty (for optional vars)

### Logging

**Standard Output:**
- Colored, formatted progress indicators
- Success/warning/error messages
- Summary at completion

**Error Log:**
```
~/.agent-build/logs/errors.log
```

**Setup Log (in report):**
```
[13:40:15] Collected ANTHROPIC_AUTH_TOKEN
[13:40:30] Databricks connection validated
```

---

## Troubleshooting

### Issue: "Command not found: python3"

**Solution:**
```bash
# Try python instead
python enterprise_setup.py

# Or install Python 3
# macOS: brew install python3
# Ubuntu: sudo apt-get install python3
```

### Issue: "Databricks connection test failed"

**Possible Causes:**
1. Invalid token
2. Wrong workspace URL
3. Network firewall
4. Expired token

**Solution:**
```bash
# Test manually
curl -H "Authorization: Bearer YOUR_TOKEN" \
  https://your-workspace.cloud.databricks.com/api/2.1/unity-catalog/catalogs

# Regenerate token in Databricks UI if needed
```

### Issue: "Rust/Cargo not found"

**Solution:**
```bash
# Install Rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# Reload shell
source ~/.bashrc  # or ~/.zshrc

# Run setup again
python3 enterprise_setup.py
```

### Issue: "Build timed out after 10 minutes"

**Possible Causes:**
1. Slow network (downloading dependencies)
2. Slow CPU
3. Insufficient memory

**Solution:**
```bash
# Build manually with more time
cd ~/.agent-build/repos/agent-build/edda
cargo build --release --package edda_mcp

# Install manually
cp target/release/edda_mcp ~/.local/bin/
chmod +x ~/.local/bin/edda_mcp
```

### Issue: "GitHub token invalid"

**Solution:**
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Generate new token with `repo` scope
3. Run setup again with new token

---

## Security Best Practices

### ✅ DO

- **Keep .env secure** - Never commit to version control
- **Rotate tokens** - Regenerate tokens periodically
- **Limit token scope** - Use minimal required permissions
- **Use .env.example** - Share template, not actual values
- **Review logs** - Check for leaked secrets

### ❌ DON'T

- **Commit .env** - Add to .gitignore
- **Share tokens** - Each user should have their own
- **Use root** - Run as regular user
- **Skip validation** - Let script test connections
- **Store in code** - Always use environment variables

---

## Integration with CI/CD

### GitHub Actions Example

```yaml
name: Deploy agent-build

on: [push]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup environment
        env:
          ANTHROPIC_AUTH_TOKEN: ${{ secrets.ANTHROPIC_AUTH_TOKEN }}
          DATABRICKS_HOST: ${{ secrets.DATABRICKS_HOST }}
          DATABRICKS_TOKEN: ${{ secrets.DATABRICKS_TOKEN }}
          GITHUB_TOKEN: ${{ secrets.GITHUB_TOKEN }}
        run: |
          # Create .env from secrets
          echo "ANTHROPIC_AUTH_TOKEN=$ANTHROPIC_AUTH_TOKEN" >> .env
          echo "DATABRICKS_HOST=$DATABRICKS_HOST" >> .env
          echo "DATABRICKS_TOKEN=$DATABRICKS_TOKEN" >> .env
          echo "GITHUB_TOKEN=$GITHUB_TOKEN" >> .env
      
      - name: Run setup (non-interactive)
        run: |
          # Setup already has .env, skip interactive prompts
          source .env
          # Run build/test steps directly
```

---

## Script Architecture

### Class Structure

```
EnterpriseSetup
├── __init__()           # Initialize workspace paths
├── run()                # Main orchestration
├── collect_environment_variables()
├── validate_configuration()
├── save_env_file()
├── setup_workspace()
├── clone_repositories()
├── analyze_documentation()
├── install_dependencies()
├── build_mcp_server()
├── test_integrations()
│   ├── test_databricks()
│   ├── test_github()
│   └── test_zai_api()
├── generate_report()
├── print_summary()
├── log_step()
└── log_error()

SetupConfig
├── REQUIRED_VARS        # List[EnvVariable]
├── OPTIONAL_VARS        # List[EnvVariable]
└── REPOSITORIES         # List[Dict]

EnvVariable (dataclass)
├── name: str
├── description: str
├── required: bool
├── default: Optional[str]
├── validation: Optional[callable]
└── secret: bool
```

### Execution Flow

```
1. Welcome & Header
2. Collect Variables (interactive)
   ├─ Required (5 variables)
   └─ Optional (7 variables)
3. Validate Configuration
   └─ Test Databricks connection
4. Save .env + .env.example
5. Setup Workspace
   └─ Create directories
6. Clone Repositories
   └─ agent-build (with git)
7. Analyze Documentation
   └─ Index all .md files
8. Install Dependencies
   ├─ Check Rust/Cargo
   └─ Check Docker
9. Build MCP Server
   └─ cargo build --release
10. Test Integrations
    ├─ Databricks API
    ├─ GitHub API
    └─ Z.ai API
11. Generate Report
12. Print Summary
```

---

## Performance Characteristics

### Execution Time

| Step | Time | Notes |
|------|------|-------|
| Variable Collection | 2-5 min | User input speed |
| Validation | 5-10 sec | API calls |
| Repository Cloning | 10-30 sec | Network speed |
| Documentation Analysis | 1-2 sec | Local file operations |
| Dependency Check | 1-2 sec | Command availability |
| MCP Server Build | 5-10 min | First build only |
| Integration Tests | 5-15 sec | 3 API calls |
| Report Generation | <1 sec | File writing |
| **Total** | **8-16 min** | First-time setup |

**Subsequent runs:** 2-3 minutes (skips build)

### Resource Usage

- **Disk:** ~500MB (Rust target directory)
- **Memory:** 2-4GB peak (during Rust build)
- **Network:** ~100MB (dependencies + repo)
- **CPU:** 100% during build (10 minutes)

---

## FAQ

**Q: Can I run this multiple times?**  
A: Yes! The script detects existing setups and updates them.

**Q: What if I don't have Rust installed?**  
A: The script will guide you to install it, or you can skip the build step.

**Q: Can I use this in production?**  
A: Yes! It's designed for enterprise deployment.

**Q: How do I update agent-build?**  
A: Run the script again - it will `git pull` updates.

**Q: Where are secrets stored?**  
A: Only in `.env` file (local, not committed).

**Q: Can I automate this?**  
A: Yes! Pre-create `.env` file to skip interactive prompts.

**Q: What Python version is required?**  
A: Python 3.7+ (uses pathlib, dataclasses)

**Q: Does this work on Windows?**  
A: Partially. Rust/Docker work, but paths may need adjustment.

---

## Support & Contribution

### Getting Help

1. Check troubleshooting section above
2. Review error logs in `~/.agent-build/logs/`
3. Check deployment report for details

### Contributing

Improvements welcome! Key areas:
- Windows compatibility
- Additional integrations (AWS, Azure, GCP)
- More validation checks
- Performance optimizations

---

## License

Part of agent-build project. See main repository for license.

---

**Created by:** Codegen AI  
**Date:** November 14, 2025  
**Version:** 1.0

