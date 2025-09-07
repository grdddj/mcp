"""
Claude API functionality for interacting with Anthropic's API
"""

import os
import sys
from pathlib import Path
from anthropic import Anthropic
from dotenv import load_dotenv


def load_env_config() -> tuple[str, str]:
    """Load configuration from .env file"""
    # Load from .env file in current directory
    env_path = Path(".env")
    if env_path.exists():
        load_dotenv(env_path)

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print(
            "Error: ANTHROPIC_API_KEY not found in environment variables or .env file"
        )
        print("Please create a .env file with your API key:")
        print("ANTHROPIC_API_KEY=your_api_key_here")
        sys.exit(1)

    # Get default model from .env if set
    default_model = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")

    return api_key, default_model


def get_default_model() -> str:
    """Get default model from .env or fallback"""
    _, default_model = load_env_config()
    return default_model


def chat_with_claude(
    message: str, model: str = "claude-sonnet-4-20250514", max_tokens: int = 1024
) -> str:
    """Send a message to Claude and return the response"""
    api_key, _ = load_env_config()

    try:
        client = Anthropic(api_key=api_key)

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": message}],
        )

        return response.content[0].text

    except Exception as e:
        print(f"Error communicating with Claude API: {e}")
        sys.exit(1)