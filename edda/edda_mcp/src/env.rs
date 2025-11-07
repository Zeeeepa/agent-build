//! Environment variable management for edda_mcp
//!
//! Loads environment variables from:
//! 1. ~/.edda/.env (takes priority)
//! 2. System environment variables
//!
//! Provides grouped validation for provider-specific credentials.

use crate::paths;
use std::collections::HashMap;
use std::path::PathBuf;

/// Environment variable groups for different providers
#[derive(Debug, Clone)]
pub struct EnvVars {
    vars: HashMap<String, String>,
}

impl EnvVars {
    /// Load environment variables from ~/.edda/.env and system environment
    /// Priority: local .env > system env
    pub fn load() -> eyre::Result<Self> {
        let mut vars = HashMap::new();

        // first, load system environment variables
        for (key, value) in std::env::vars() {
            vars.insert(key, value);
        }

        // then, load from ~/.edda/.env (overrides system env)
        let env_path = paths::edda_dir()?.join(".env");
        if env_path.exists() {
            tracing::debug!("Loading environment from {}", env_path.display());
            dotenvy::from_path(&env_path)?;

            // re-read all env vars to get the loaded ones
            for (key, value) in std::env::vars() {
                vars.insert(key, value);
            }
        } else {
            tracing::debug!("No .env file found at {}", env_path.display());
        }

        Ok(Self { vars })
    }

    /// Get an environment variable value
    pub fn get(&self, key: &str) -> Option<&str> {
        self.vars.get(key).map(|s| s.as_str())
    }

    /// Validate Databricks credentials (HOST, TOKEN, WAREHOUSE_ID)
    pub fn validate_databricks(&self, require_warehouse: bool) -> eyre::Result<()> {
        let host = self.get("DATABRICKS_HOST")
            .ok_or_else(|| eyre::eyre!(
                "DATABRICKS_HOST not set. Please add it to ~/.edda/.env or system environment.\n\
                 See ~/.edda/.env.example for template."
            ))?;

        let _token = self.get("DATABRICKS_TOKEN")
            .ok_or_else(|| eyre::eyre!(
                "DATABRICKS_TOKEN not set. Please add it to ~/.edda/.env or system environment.\n\
                 See ~/.edda/.env.example for template."
            ))?;

        if require_warehouse {
            self.get("DATABRICKS_WAREHOUSE_ID")
                .ok_or_else(|| eyre::eyre!(
                    "DATABRICKS_WAREHOUSE_ID not set (required for deployment). \
                     Please add it to ~/.edda/.env or system environment.\n\
                     See ~/.edda/.env.example for template."
                ))?;
        }

        tracing::debug!("Databricks credentials validated (host: {})", host);
        Ok(())
    }

    /// Validate Google Sheets credentials path
    pub fn validate_google_sheets(&self) -> eyre::Result<()> {
        let path = self.get("GOOGLE_CREDENTIALS_PATH")
            .ok_or_else(|| eyre::eyre!(
                "GOOGLE_CREDENTIALS_PATH not set. Please add it to ~/.edda/.env or system environment.\n\
                 See ~/.edda/.env.example for template."
            ))?;

        let path = PathBuf::from(path);
        if !path.exists() {
            return Err(eyre::eyre!(
                "Google credentials file not found at: {}\n\
                 Please ensure the file exists or update GOOGLE_CREDENTIALS_PATH.",
                path.display()
            ));
        }

        tracing::debug!("Google Sheets credentials validated (path: {})", path.display());
        Ok(())
    }

    /// Get Databricks host (normalizes URL format)
    pub fn databricks_host(&self) -> Option<String> {
        self.get("DATABRICKS_HOST").map(|host| {
            // normalize: remove trailing slash, ensure https://
            let host = host.trim_end_matches('/');
            if host.starts_with("http://") || host.starts_with("https://") {
                host.to_string()
            } else {
                format!("https://{}", host)
            }
        })
    }

    /// Get Databricks token
    pub fn databricks_token(&self) -> Option<&str> {
        self.get("DATABRICKS_TOKEN")
    }

    /// Get Databricks warehouse ID
    pub fn databricks_warehouse_id(&self) -> Option<&str> {
        self.get("DATABRICKS_WAREHOUSE_ID")
    }

    /// Get Google credentials path
    pub fn google_credentials_path(&self) -> Option<&str> {
        self.get("GOOGLE_CREDENTIALS_PATH")
    }
}

/// Create .env.example file in ~/.edda/ if it doesn't exist
pub fn create_env_example() -> eyre::Result<()> {
    let edda_dir = paths::edda_dir()?;
    std::fs::create_dir_all(&edda_dir)?;

    let example_path = edda_dir.join(".env.example");

    // only create if it doesn't exist
    if example_path.exists() {
        tracing::debug!(".env.example already exists at {}", example_path.display());
        return Ok(());
    }

    let example_content = r#"# Edda MCP Environment Configuration
# Copy this file to .env and fill in your credentials

# ============================================
# Databricks Configuration
# ============================================
# Required for Databricks tools (list catalogs, schemas, tables, execute SQL)
# DATABRICKS_HOST=your-workspace.cloud.databricks.com
# DATABRICKS_TOKEN=dapi...
# DATABRICKS_WAREHOUSE_ID=your-warehouse-id

"#;

    std::fs::write(&example_path, example_content)?;
    tracing::info!("Created .env.example at {}", example_path.display());

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_databricks_host_normalization() {
        let mut vars = HashMap::new();

        // test with https://
        vars.insert("DATABRICKS_HOST".to_string(), "https://example.databricks.com".to_string());
        let env = EnvVars { vars: vars.clone() };
        assert_eq!(env.databricks_host(), Some("https://example.databricks.com".to_string()));

        // test without protocol
        vars.insert("DATABRICKS_HOST".to_string(), "example.databricks.com".to_string());
        let env = EnvVars { vars: vars.clone() };
        assert_eq!(env.databricks_host(), Some("https://example.databricks.com".to_string()));

        // test with trailing slash
        vars.insert("DATABRICKS_HOST".to_string(), "https://example.databricks.com/".to_string());
        let env = EnvVars { vars };
        assert_eq!(env.databricks_host(), Some("https://example.databricks.com".to_string()));
    }
}
