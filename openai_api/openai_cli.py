"""CLI interface for OpenAI ChatGPT API with interactive and single-shot modes.

This module provides a command-line interface for the OpenAI API client,
supporting both one-time queries and interactive conversation sessions.
Includes streaming responses, token usage tracking, and cost estimation.
"""

import argparse
from openai_client import get_openai_response, TokenUsage


def display_stats(usage: TokenUsage | None, model_name: str) -> None:
    """Display formatted token usage statistics and cost information.

    Prints a nicely formatted summary of token usage including input/output tokens,
    total usage, and estimated cost. Only displays if usage data is available
    (not available for streaming responses).

    Args:
        usage: TokenUsage object with statistics, or None if not available
        model_name: Name of the OpenAI model used for the request

    Example output:
        📊 Token Usage Stats:
           Model: gpt-4o
           Input tokens: 1,234
           Output tokens: 567
           Total tokens: 1,801
           Estimated cost: $0.012345
    """
    if usage:
        print("\n📊 Token Usage Stats:")
        print(f"   Model: {model_name}")
        print(f"   Input tokens: {usage.prompt_tokens:,}")
        print(f"   Output tokens: {usage.completion_tokens:,}")
        print(f"   Total tokens: {usage.total_tokens:,}")
        print(f"   Estimated cost: ${usage.estimated_cost:.6f}")


def interactive_mode(
    model: str | None = None, stream: bool = False, show_stats: bool = False
) -> int:
    """Start an interactive conversation session with context preservation.

    Runs a continuous conversation loop where users can chat with the AI
    while maintaining conversation context across multiple turns. Supports
    all the same features as single-shot mode including streaming and stats.

    The conversation history is preserved throughout the session, allowing
    for follow-up questions and contextual responses. Users can exit with
    'exit', 'quit', Ctrl+C, or EOF.

    Args:
        model: OpenAI model to use (defaults to env var or gpt-4o)
        stream: Whether to stream responses in real-time
        show_stats: Whether to display token usage stats after each response

    Returns:
        Exit code (0 for success, non-zero for errors)

    Features:
        - Persistent conversation context across turns
        - Graceful exit handling (multiple methods)
        - Real-time streaming support
        - Token usage tracking and cost estimation
        - Empty input handling

    Example session:
        You: What is Python?
        Assistant: Python is a programming language...

        📊 Token Usage Stats:
           Model: gpt-4o
           Input tokens: 15
           Output tokens: 120
           Total tokens: 135
           Estimated cost: $0.001350

        You: What can I build with it?
        Assistant: With Python, you can build many things...
    """
    conversation_history = []

    print("Interactive mode started. Type 'exit', 'quit', or press Ctrl+C to exit.")
    print("=" * 50)

    try:
        while True:
            try:
                user_input = input("\nYou: ").strip()

                if not user_input:
                    continue

                if user_input.lower() in ["exit", "quit"]:
                    print("Goodbye!")
                    break

                print("Assistant: ", end="", flush=True)

                response_obj = get_openai_response(
                    request=user_input,
                    model=model,
                    stream=stream,
                    conversation_history=conversation_history,
                )

                # Handle response and update conversation history
                if stream:
                    full_response = ""
                    for chunk in response_obj.content:
                        print(chunk, end="", flush=True)
                        full_response += chunk
                    print()
                    assistant_response = full_response

                    # Note: Token usage stats not available in streaming mode
                    if show_stats:
                        print("\n⚠️  Token usage stats not available in streaming mode")
                else:
                    print(response_obj.content)
                    assistant_response = response_obj.content

                    # Display stats for non-streaming
                    if show_stats:
                        display_stats(response_obj.usage, model or "gpt-4o")

                # Add to conversation history
                conversation_history.append({"role": "user", "content": user_input})
                conversation_history.append(
                    {"role": "assistant", "content": assistant_response}
                )

            except EOFError:
                print("\nGoodbye!")
                break

    except KeyboardInterrupt:
        print("\n\nGoodbye!")
        return 0

    return 0


def main() -> int:
    """Main CLI entry point with argument parsing and mode routing.

    Parses command-line arguments and routes to either interactive mode
    or single-shot query mode. Handles all CLI flags and options including
    model selection, streaming, statistics display, and interactive mode.

    Command-line interface supports:
    - Single-shot queries: openai-cli "Your prompt here"
    - Interactive mode: openai-cli -i
    - Model selection: openai-cli -m gpt-3.5-turbo "prompt"
    - Streaming: openai-cli -s "prompt"
    - Statistics: openai-cli --stats "prompt"
    - Combined flags: openai-cli -i -s --stats

    Returns:
        Exit code (0 for success, 1 for errors)

    Raises:
        SystemExit: Via argparse for invalid arguments
    """
    parser = argparse.ArgumentParser(
        description="CLI tool for OpenAI ChatGPT API with interactive and single-shot modes",
        epilog="Examples:\n"
        "  %(prog)s 'What is Python?'                    # Single query\n"
        "  %(prog)s -i                                    # Interactive mode\n"
        "  %(prog)s -s 'Tell me a story'                 # Streaming response\n"
        "  %(prog)s --stats 'Explain AI'                 # Show token usage\n"
        "  %(prog)s -i -m gpt-3.5-turbo --stats          # Interactive with custom model\n",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Your prompt/question for ChatGPT (required unless using -i/--interactive)",
    )
    parser.add_argument(
        "-m",
        "--model",
        help="OpenAI model to use (e.g., gpt-4o, gpt-3.5-turbo). Overrides OPENAI_MODEL from .env",
        metavar="MODEL",
    )
    parser.add_argument(
        "-s",
        "--stream",
        action="store_true",
        help="Stream the response in real-time (disables token usage stats)",
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Start interactive conversation mode with context preservation",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show detailed token usage statistics and cost estimation (not available with --stream)",
    )

    args = parser.parse_args()

    # Interactive mode
    if args.interactive:
        return interactive_mode(
            model=args.model, stream=args.stream, show_stats=args.stats
        )

    # Single prompt mode
    if not args.prompt:
        parser.error("prompt is required unless using --interactive mode")

    try:
        response_obj = get_openai_response(
            request=args.prompt, model=args.model, stream=args.stream
        )

        if args.stream:
            for chunk in response_obj.content:
                print(chunk, end="", flush=True)
            print()

            # Note: Token usage stats not available in streaming mode
            if args.stats:
                print("\n⚠️  Token usage stats not available in streaming mode")
        else:
            print(response_obj.content)

            # Show stats for non-streaming
            if args.stats:
                display_stats(response_obj.usage, args.model or "gpt-4o")

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
