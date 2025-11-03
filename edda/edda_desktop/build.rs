use anyhow::{Context, Result};
use std::path::PathBuf;

fn main() -> Result<()> {
    println!("cargo:rerun-if-changed=../edda_mcp");

    // copy edda_mcp binary to resources for bundling
    let target_dir = PathBuf::from(std::env::var("CARGO_MANIFEST_DIR")?).join("target");
    let profile = std::env::var("PROFILE")?;

    let src_binary = target_dir
        .parent()
        .context("Failed to get workspace root")?
        .join("target")
        .join(&profile)
        .join("edda_mcp");

    if !src_binary.exists() {
        println!("cargo:warning=edda_mcp binary not found at {:?}, will skip bundling", src_binary);
        return Ok(());
    }

    // for development, we'll just use the binary from target/release
    // for production builds, we'd embed it in the app bundle
    println!("cargo:warning=Using edda_mcp from: {:?}", src_binary);

    Ok(())
}
