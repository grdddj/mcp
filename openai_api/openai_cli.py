import argparse
from openai_client import get_openai_response


def display_stats(usage, model_name):
    """Display token usage statistics"""
    if usage:
        print("\n📊 Token Usage Stats:")
        print(f"   Model: {model_name}")
        print(f"   Input tokens: {usage.prompt_tokens:,}")
        print(f"   Output tokens: {usage.completion_tokens:,}")
        print(f"   Total tokens: {usage.total_tokens:,}")
        print(f"   Estimated cost: ${usage.estimated_cost:.6f}")


def interactive_mode(model=None, stream=False, show_stats=False):
    """Run interactive conversation mode"""
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


def main():
    parser = argparse.ArgumentParser(description="Simple CLI for OpenAI ChatGPT API")
    parser.add_argument(
        "prompt",
        nargs="?",
        help="Your prompt for ChatGPT (optional in interactive mode)",
    )
    parser.add_argument(
        "-m", "--model", help="Model to use (overrides OPENAI_MODEL from .env)"
    )
    parser.add_argument(
        "-s", "--stream", action="store_true", help="Stream the response"
    )
    parser.add_argument(
        "-i",
        "--interactive",
        action="store_true",
        help="Start interactive conversation mode",
    )
    parser.add_argument(
        "--stats",
        action="store_true",
        help="Show token usage statistics and cost estimation",
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
