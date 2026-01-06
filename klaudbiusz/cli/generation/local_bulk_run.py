"""Local bulk app generation (no Dagger containers)."""

import json
import os
from datetime import datetime
from pathlib import Path

import fire
from dotenv import load_dotenv

load_dotenv()


def run_single(
    app_name: str,
    prompt: str,
    mcp_binary: str,
    mcp_args: list[str],
    output_dir: Path,
    backend: str = "claude",
    model: str | None = None,
) -> tuple[str, Path | None, dict | None, str | None]:
    """Run single app generation locally.

    Returns:
        Tuple of (app_name, app_dir, metrics, error)
    """
    from cli.generation.codegen import ClaudeAppBuilder

    try:
        builder = ClaudeAppBuilder(
            app_name=app_name,
            wipe_db=False,
            suppress_logs=False,
            mcp_binary=mcp_binary,
            mcp_args=mcp_args,
            output_dir=str(output_dir),
        )
        metrics = builder.run(prompt, wipe_db=False)
        app_dir = output_dir / app_name
        return (app_name, app_dir if app_dir.exists() else None, metrics, None)
    except Exception as e:
        return (app_name, None, None, str(e))


def main(
    prompts: str = "databricks",
    backend: str = "claude",
    model: str | None = None,
    mcp_binary: str | None = None,
    mcp_args: list[str] | None = None,
    output_dir: str | None = None,
) -> None:
    """Local bulk app generation (no Dagger).

    Args:
        prompts: Prompt set to use ("databricks", "databricks_v2", or "test")
        backend: Backend to use ("claude" or "litellm")
        model: LLM model (required if backend=litellm)
        mcp_binary: Path to MCP binary (required)
        mcp_args: Optional list of args passed to the MCP server
        output_dir: Custom output directory for generated apps
    """
    if not mcp_binary:
        raise ValueError("--mcp_binary is required")

    if backend == "litellm" and not model:
        raise ValueError("--model is required when using --backend=litellm")

    # validate required environment variables
    if not os.environ.get("DATABRICKS_HOST") or not os.environ.get("DATABRICKS_TOKEN"):
        raise ValueError("DATABRICKS_HOST and DATABRICKS_TOKEN environment variables must be set")

    # load prompt set
    match prompts:
        case "databricks":
            from cli.generation.prompts.databricks import PROMPTS as selected_prompts
        case "databricks_v2":
            from cli.generation.prompts.databricks_v2 import PROMPTS as selected_prompts
        case "test":
            from cli.generation.prompts.web import PROMPTS as selected_prompts
        case _:
            raise ValueError(f"Unknown prompt set: {prompts}. Use 'databricks', 'databricks_v2', or 'test'")

    print(f"Starting LOCAL bulk generation for {len(selected_prompts)} prompts...")
    print(f"Backend: {backend}")
    if backend == "litellm":
        print(f"Model: {model}")
    print(f"Prompt set: {prompts}")
    print(f"MCP binary: {mcp_binary}")
    out_path = Path(output_dir) if output_dir else Path("./app")
    print(f"Output dir: {out_path}\n")
    out_path.mkdir(parents=True, exist_ok=True)

    mcp_args_list = mcp_args or []
    results = []
    success_count = 0
    fail_count = 0

    for i, (app_name, prompt) in enumerate(selected_prompts.items(), 1):
        print(f"\n{'=' * 80}")
        print(f"[{i}/{len(selected_prompts)}] Generating: {app_name}")
        print(f"{'=' * 80}")

        app_name_result, app_dir, metrics, error = run_single(
            app_name=app_name,
            prompt=prompt,
            mcp_binary=mcp_binary,
            mcp_args=mcp_args_list,
            output_dir=out_path,
            backend=backend,
            model=model,
        )

        if error:
            fail_count += 1
            print(f"FAILED: {error}")
        else:
            success_count += 1
            print(f"SUCCESS: {app_dir}")

        results.append({
            "app_name": app_name_result,
            "success": error is None,
            "prompt": prompt,
            "app_dir": str(app_dir) if app_dir else None,
            "error": error,
            "backend": backend,
            "model": model,
            "metrics": metrics,
        })

    # summary
    print(f"\n{'=' * 80}")
    print("Bulk Generation Summary")
    print(f"{'=' * 80}")
    print(f"Total prompts: {len(selected_prompts)}")
    print(f"Successful: {success_count}")
    print(f"Failed: {fail_count}")

    # save results json
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = out_path / f"local_bulk_results_{timestamp}.json"
    output_file.write_text(json.dumps(results, indent=2))
    print(f"\nResults saved to {output_file}")


if __name__ == "__main__":
    fire.Fire(main)
