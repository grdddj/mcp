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
    """Send a single message to Claude (no conversation memory)"""
    return chat_with_conversation(
        [{"role": "user", "content": message}], model, max_tokens
    )


def chat_with_conversation(
    messages: list[dict[str, str]],
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
) -> str:
    """Send a conversation history to Claude and return the response"""
    api_key, _ = load_env_config()

    try:
        client = Anthropic(api_key=api_key)

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,  # type: ignore
        )

        return response.content[0].text

    except Exception as e:
        print(f"Error communicating with Claude API: {e}")
        sys.exit(1)


class ConversationManager:
    """Manages conversation history and context window limits"""

    def __init__(self, max_context_messages: int = 20):
        self.messages: list[dict[str, str]] = []
        self.max_context_messages = max_context_messages

    def add_user_message(self, content: str):
        """Add a user message to the conversation"""
        self.messages.append({"role": "user", "content": content})
        self._trim_context()

    def add_assistant_message(self, content: str):
        """Add an assistant message to the conversation"""
        self.messages.append({"role": "assistant", "content": content})
        self._trim_context()

    def get_messages(self) -> list[dict[str, str]]:
        """Get the current conversation history"""
        return self.messages.copy()

    def _trim_context(self):
        """Keep only the most recent messages to stay within context limits"""
        if len(self.messages) > self.max_context_messages:
            # Keep the most recent messages, ensuring we don't break user/assistant pairs
            excess = len(self.messages) - self.max_context_messages
            # Remove pairs from the beginning
            pairs_to_remove = (excess + 1) // 2
            self.messages = self.messages[pairs_to_remove * 2 :]

    def clear(self):
        """Clear the conversation history"""
        self.messages.clear()

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.messages:
            return "No conversation history"
        return f"Conversation with {len(self.messages)} messages ({len([m for m in self.messages if m['role'] == 'user'])} from user)"
