"""
Claude API functionality for interacting with Anthropic's API
"""

import os
import sys
from pathlib import Path
from dataclasses import dataclass
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


@dataclass
class TokenUsage:
    """Token usage information"""

    input_tokens: int
    output_tokens: int
    total_tokens: int
    model: str = ""

    def get_cost_estimate(self, model: str = "") -> float:
        """Estimate cost in USD based on model-specific pricing"""
        model_name = model or self.model

        # Anthropic pricing (as of 2024) - per 1M tokens
        pricing = {
            # Claude 3.5 models
            "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
            "claude-3-5-sonnet-20241022": {"input": 3.00, "output": 15.00},
            "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
            "claude-opus-4-20250514": {"input": 15.00, "output": 75.00},
            "claude-opus-4-1-20250805": {"input": 15.00, "output": 75.00},
            "claude-3-7-sonnet-20250219": {"input": 4.00, "output": 20.00},
        }

        # Default to Haiku pricing if model not found
        model_pricing = pricing.get(model_name, pricing["claude-3-5-haiku-20241022"])

        input_cost = self.input_tokens * model_pricing["input"] / 1_000_000
        output_cost = self.output_tokens * model_pricing["output"] / 1_000_000
        return input_cost + output_cost

    @property
    def cost_estimate(self) -> float:
        """Backward compatibility - estimate cost"""
        return self.get_cost_estimate()


@dataclass
class ClaudeResponse:
    """Claude API response with token usage"""

    content: str
    usage: TokenUsage


def get_default_model() -> str:
    """Get default model from .env or fallback"""
    _, default_model = load_env_config()
    return default_model


def chat_with_claude(
    message: str, model: str = "claude-sonnet-4-20250514", max_tokens: int = 1024
) -> str:
    """Send a single message to Claude (no conversation memory)"""
    response = chat_with_conversation_detailed(
        [{"role": "user", "content": message}], model, max_tokens
    )
    return response.content


def chat_with_claude_detailed(
    message: str, model: str = "claude-sonnet-4-20250514", max_tokens: int = 1024
) -> ClaudeResponse:
    """Send a single message to Claude and return detailed response with token usage"""
    return chat_with_conversation_detailed(
        [{"role": "user", "content": message}], model, max_tokens
    )


def chat_with_conversation(
    messages: list[dict[str, str]],
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
) -> str:
    """Send a conversation history to Claude and return the response"""
    response = chat_with_conversation_detailed(messages, model, max_tokens)
    return response.content


def chat_with_conversation_detailed(
    messages: list[dict[str, str]],
    model: str = "claude-sonnet-4-20250514",
    max_tokens: int = 1024,
) -> ClaudeResponse:
    """Send a conversation history to Claude and return detailed response with token usage"""
    api_key, _ = load_env_config()

    try:
        client = Anthropic(api_key=api_key)

        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=messages,  # type: ignore
        )

        usage = TokenUsage(
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            total_tokens=response.usage.input_tokens + response.usage.output_tokens,
            model=model,
        )

        return ClaudeResponse(content=response.content[0].text, usage=usage)  # type: ignore

    except Exception as e:
        print(f"Error communicating with Claude API: {e}")
        sys.exit(1)


class ConversationManager:
    """Manages conversation history and context window limits"""

    def __init__(self, max_context_messages: int = 20):
        self.messages: list[dict[str, str]] = []
        self.max_context_messages = max_context_messages
        # Token usage tracking
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.exchange_count = 0

    def add_user_message(self, content: str):
        """Add a user message to the conversation"""
        self.messages.append({"role": "user", "content": content})
        self._trim_context()

    def add_assistant_message(self, content: str):
        """Add an assistant message to the conversation"""
        self.messages.append({"role": "assistant", "content": content})
        self._trim_context()

    def record_usage(self, usage: TokenUsage):
        """Record token usage for this conversation session"""
        self.total_input_tokens += usage.input_tokens
        self.total_output_tokens += usage.output_tokens
        self.total_cost += usage.cost_estimate
        self.exchange_count += 1

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

    def reset_usage(self):
        """Reset token usage tracking"""
        self.total_input_tokens = 0
        self.total_output_tokens = 0
        self.total_cost = 0.0
        self.exchange_count = 0

    def get_conversation_summary(self) -> str:
        """Get a summary of the current conversation"""
        if not self.messages:
            return "No conversation history"
        return f"Conversation with {len(self.messages)} messages ({len([m for m in self.messages if m['role'] == 'user'])} from user)"

    def get_usage_summary(self) -> str:
        """Get a summary of token usage and costs"""
        if self.exchange_count == 0:
            return "No API calls made"

        total_tokens = self.total_input_tokens + self.total_output_tokens
        return (
            f"Session usage: {self.exchange_count} exchanges, "
            f"{total_tokens:,} tokens ({self.total_input_tokens:,} in, {self.total_output_tokens:,} out), "
            f"${self.total_cost:.4f}"
        )
