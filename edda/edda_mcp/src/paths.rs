use eyre::Result;
use std::path::PathBuf;

pub const SESSION_LOG_DIR: &str = "/tmp/edda-mcp";
pub const EDDA_DIR: &str = ".edda";
pub const HISTORY_FILE: &str = "history.jsonl";

/// get the edda directory path (~/.edda)
pub fn edda_dir() -> Result<PathBuf> {
    let home = dirs::home_dir()
        .ok_or_else(|| eyre::eyre!("failed to get home directory"))?;
    Ok(home.join(EDDA_DIR))
}

/// get the trajectory history file path (~/.edda/history.jsonl)
pub fn trajectory_path() -> Result<PathBuf> {
    Ok(edda_dir()?.join(HISTORY_FILE))
}

/// get the session log directory path (/tmp/edda-mcp)
pub fn session_log_dir() -> PathBuf {
    PathBuf::from(SESSION_LOG_DIR)
}
