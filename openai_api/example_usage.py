#!/usr/bin/env python3
"""
Example usage of the reusable get_openai_response function
"""

from openai_client import get_openai_response


def demonstrate_basic_usage() -> None:
    """Demonstrate basic single-shot query with token usage analysis."""
    print("=== Basic Usage Example ===")

    response = get_openai_response("What is Python programming language?")
    print(f"Response: {response.content}")

    if response.usage:
        print("\nToken Usage:")
        print(f"  Input: {response.usage.prompt_tokens} tokens")
        print(f"  Output: {response.usage.completion_tokens} tokens")
        print(f"  Total: {response.usage.total_tokens} tokens")
        print(f"  Cost: ${response.usage.estimated_cost:.6f}")
    print("\n" + "-" * 50 + "\n")


def demonstrate_model_selection() -> None:
    """Show how to use different OpenAI models for specific tasks."""
    print("=== Model Selection Example ===")

    # Use cheaper model for simple tasks
    response = get_openai_response(
        "Explain quantum computing in one sentence", model="gpt-3.5-turbo"
    )
    print(f"GPT-3.5 Response: {response.content}")

    if response.usage:
        print(f"Cost with GPT-3.5: ${response.usage.estimated_cost:.6f}")
    print("\n" + "-" * 50 + "\n")


def demonstrate_streaming() -> None:
    """Show real-time streaming response functionality."""
    print("=== Streaming Response Example ===")
    print("Streaming output: ", end="", flush=True)

    response = get_openai_response("Tell me a short programming joke", stream=True)

    # Collect full response while streaming
    full_response = ""
    for chunk in response.content:
        print(chunk, end="", flush=True)
        full_response += chunk

    print(f"\n\nFull response collected: {len(full_response)} characters")
    print(f"Token usage available: {response.usage is not None}")
    print("\n" + "-" * 50 + "\n")


def demonstrate_conversation_context() -> None:
    """Show multi-turn conversation with context preservation."""
    print("=== Conversation Context Example ===")

    # Start conversation
    conversation_history: list[dict[str, str]] = []

    # First turn
    user_input = "My name is Alice and I'm learning Python"
    response = get_openai_response(
        user_input, conversation_history=conversation_history
    )

    print(f"User: {user_input}")
    print(f"Assistant: {response.content}")

    # Update conversation history
    conversation_history.extend(
        [
            {"role": "user", "content": user_input},
            {"role": "assistant", "content": response.content},
        ]
    )

    # Follow-up turn with context
    user_input = "What's my name and what am I learning?"
    response = get_openai_response(
        user_input, conversation_history=conversation_history
    )

    print(f"\nUser: {user_input}")
    print(f"Assistant: {response.content}")

    if response.usage:
        print(f"\nTotal conversation cost so far: ${response.usage.estimated_cost:.6f}")
    print("\n" + "-" * 50 + "\n")


def demonstrate_error_handling() -> None:
    """Show proper error handling patterns."""
    print("=== Error Handling Example ===")

    try:
        # This will work if API key is set
        response = get_openai_response("Test query")
        print("✓ API call successful")
        print(f"✓ Response received: {len(response.content)} characters")

    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Make sure OPENAI_API_KEY is set in environment or .env file")

    except Exception as e:
        print(f"❌ API error: {e}")
        print("This could be a rate limit, invalid model, or network issue")

    print("\n" + "-" * 50 + "\n")


def main() -> None:
    """Run all examples demonstrating different usage patterns.

    Executes a comprehensive set of examples showing how to use the
    get_openai_response() function in various scenarios. Each example
    is self-contained and demonstrates specific features.

    Examples include:
    - Basic usage with token tracking
    - Model selection for different tasks
    - Real-time streaming responses
    - Multi-turn conversations with context
    - Proper error handling patterns
    """
    print("OpenAI API Client - Example Usage Demonstrations\n")
    print("=" * 60)

    try:
        demonstrate_basic_usage()
        demonstrate_model_selection()
        demonstrate_streaming()
        demonstrate_conversation_context()

    except Exception as e:
        print(f"Example failed: {e}")
        print("Make sure your OPENAI_API_KEY is properly configured")

    finally:
        demonstrate_error_handling()

    print("All examples completed!")


if __name__ == "__main__":
    main()
