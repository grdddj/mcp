"""
CLI interface for the Claude API tool
"""

import argparse
import sys
from claude_api import chat_with_claude, get_default_model


def main():
    """Main CLI entry point"""
    # Get default model from .env file
    default_model = get_default_model()

    parser = argparse.ArgumentParser(description="Chat with Claude via CLI")
    parser.add_argument("message", nargs="?", help="Message to send to Claude")
    parser.add_argument(
        "--model",
        default=default_model,
        help=f"Claude model to use (default: {default_model})",
    )
    parser.add_argument(
        "--max-tokens",
        type=int,
        default=1024,
        help="Maximum tokens in response (default: 1024)",
    )
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Start interactive chat mode"
    )

    args = parser.parse_args()

    if args.interactive:
        # Interactive mode
        print(
            f"Starting interactive chat with Claude ({args.model}). Type 'exit' or 'quit' to end."
        )
        print("-" * 50)

        while True:
            try:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("Goodbye!")
                    break

                if not user_input:
                    continue

                print("Claude: ", end="")
                response = chat_with_claude(user_input, args.model, args.max_tokens)
                print(response)

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

    elif args.message:
        # Single message mode
        response = chat_with_claude(args.message, args.model, args.max_tokens)
        print(response)

    else:
        # No message provided, read from stdin
        if sys.stdin.isatty():
            print(
                "Error: No message provided. Use -i for interactive mode or provide a message."
            )
            parser.print_help()
            sys.exit(1)

        message = sys.stdin.read().strip()
        if message:
            response = chat_with_claude(message, args.model, args.max_tokens)
            print(response)


if __name__ == "__main__":
    main()