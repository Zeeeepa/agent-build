"""Agentic evaluation using Claude SDK.

Replaces template-specific shell scripts with direct Claude SDK agent calls.
Instead of `bash install.sh`, ask the agent "install dependencies for this app"
and let it figure out the commands.
"""

import logging
from pathlib import Path
from typing import Literal

from claude_agent_sdk import (
    AssistantMessage,
    ClaudeAgentOptions,
    ResultMessage,
    TextBlock,
    ToolResultBlock,
    UserMessage,
    query,
)

logger = logging.getLogger(__name__)

# Evaluation step prompts - agent figures out specific commands
EVAL_PROMPTS: dict[str, str] = {
    "install": """Install dependencies for this Node.js app.
- If root package.json has an "install:all" script, run `npm run install:all`
- Otherwise, run `npm install` in each directory that has a package.json (server/, client/, etc.)
- Do not modify any files, only install dependencies""",
    "build": """Build this app for production.
- Find the build command in package.json (usually `npm run build`)
- Run it in the appropriate directory (root or client/ for tRPC apps)
- Report success/failure based on exit code""",
    "typecheck": """Run TypeScript type checking on this codebase.
- Find directories with tsconfig.json
- Run `npx tsc --noEmit --skipLibCheck` in each directory
- Report success if no type errors found""",
    "test": """Run the test suite for this app.
- Find the test command in package.json (usually `npm test`)
- Run tests in the server/ directory if it exists
- Report test results and coverage percentage if available""",
    "start": """Start this app and verify it responds on port {port}.

Steps:
1. First, kill any existing processes on port {port}: lsof -ti:{port} | xargs kill -9 2>/dev/null || true
2. Start the app in background: npm start > /tmp/app.log 2>&1 &
3. Wait briefly for startup: sleep 3
4. Health check with retries - try these endpoints:
   - curl -sf --max-time 2 http://localhost:{port}/healthcheck
   - curl -sf --max-time 2 http://localhost:{port}/
5. If either returns success, the app is running correctly
6. Clean up: kill any process on port {port} after testing

The test succeeds if the health check passes.""",
    "stop": """Stop any running processes for this app on port {port}.
- Kill any processes listening on port {port}
- Use: lsof -ti:{port} | xargs kill -9 2>/dev/null || true
- Ensure the port is free for the next test""",
}

EvalStep = Literal["install", "build", "typecheck", "test", "start", "stop"]


class EvalAgent:
    """Agent-based evaluation runner using Claude SDK."""

    def __init__(
        self,
        app_dir: Path,
        model: str = "haiku",
        suppress_logs: bool = True,
        env: dict[str, str] | None = None,
    ):
        """Initialize evaluation agent.

        Args:
            app_dir: Path to the app directory to evaluate
            model: Model to use (default: haiku for cost efficiency)
            suppress_logs: Whether to suppress logging output
            env: Environment variables to pass to the agent
        """
        self.app_dir = app_dir
        self.model = model
        self.suppress_logs = suppress_logs
        self.env = env or {}

    async def run_step(
        self,
        step: EvalStep,
        timeout_sec: int = 120,
        **kwargs,
    ) -> tuple[bool, str]:
        """Run an evaluation step using the agent.

        Args:
            step: Evaluation step to run (install, build, typecheck, test, start, stop)
            timeout_sec: Maximum time for the step (not currently enforced)
            **kwargs: Format arguments for the prompt (e.g., port=8000)

        Returns:
            Tuple of (success: bool, output: str)
        """
        if step not in EVAL_PROMPTS:
            return False, f"Unknown evaluation step: {step}"

        prompt_template = EVAL_PROMPTS[step]
        prompt = prompt_template.format(**kwargs)

        # Build the full prompt with app context
        # Use absolute path for the working directory
        abs_app_dir = self.app_dir.resolve()
        full_prompt = f"""Task: {prompt}

Important:
- Work only within the current directory ({abs_app_dir})
- Do not create or modify source code files
- Report success (exit 0) or failure (exit 1) clearly
- Be concise - this is an automated evaluation step"""

        # Configure agent options
        # Use more turns for start/stop which are more complex
        max_turns = 15 if step in ("start", "stop") else 10
        options = ClaudeAgentOptions(
            system_prompt={
                "type": "preset",
                "preset": "claude_code",
            },
            permission_mode="bypassPermissions",
            allowed_tools=["Bash", "Read", "Glob", "Grep"],
            max_turns=max_turns,
            model=self.model,
            cwd=abs_app_dir,  # Set working directory to app directory
            env=self.env,  # Pass environment variables
        )

        output_lines: list[str] = []
        success = False

        try:
            async for message in query(prompt=full_prompt, options=options):
                if isinstance(message, AssistantMessage):
                    # Capture assistant text output
                    for block in message.content:
                        if isinstance(block, TextBlock) and block.text:
                            output_lines.append(block.text)
                elif isinstance(message, UserMessage):
                    # Capture tool results (which come in UserMessage)
                    for block in message.content:
                        if isinstance(block, ToolResultBlock):
                            content = str(block.content) if block.content else ""
                            if content:
                                # Truncate long output
                                if len(content) > 1000:
                                    content = content[:1000] + "..."
                                output_lines.append(content)
                elif isinstance(message, ResultMessage):
                    # subtype indicates success/failure, result is the text response
                    success = message.subtype == "success" and not message.is_error
                    # Capture the final result text
                    if message.result:
                        output_lines.append(message.result)
                    if not self.suppress_logs:
                        logger.info(f"Eval step {step} subtype: {message.subtype}")

        except Exception as e:
            logger.error(f"Eval step {step} failed with exception: {e}")
            return False, f"Exception: {str(e)}"

        return success, "\n".join(output_lines)

    async def install_dependencies(self) -> tuple[bool, str]:
        """Install npm dependencies."""
        return await self.run_step("install")

    async def build(self) -> tuple[bool, str]:
        """Build the app for production."""
        return await self.run_step("build")

    async def typecheck(self) -> tuple[bool, str]:
        """Run TypeScript type checking."""
        return await self.run_step("typecheck")

    async def test(self) -> tuple[bool, str]:
        """Run the test suite."""
        return await self.run_step("test")

    async def start(self, port: int = 8000) -> tuple[bool, str]:
        """Start the app and verify it responds."""
        return await self.run_step("start", port=port)

    async def stop(self, port: int = 8000) -> tuple[bool, str]:
        """Stop any running processes for this app."""
        return await self.run_step("stop", port=port)
