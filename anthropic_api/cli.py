"""
CLI interface for the Claude API tool
"""

import argparse
import sys
from claude_api import chat_with_claude, chat_with_conversation, get_default_model, ConversationManager


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
        "--interactive", "-i", action="store_true", help="Start interactive chat mode with conversation memory"
    )
    parser.add_argument(
        "--no-memory", action="store_true", help="Disable conversation memory in interactive mode"
    )

    args = parser.parse_args()

    if args.interactive:
        # Interactive mode with conversation memory
        memory_status = "disabled" if args.no_memory else "enabled"
        print(
            f"Starting interactive chat with Claude ({args.model}). Conversation memory: {memory_status}."
        )
        print("Type 'exit', 'quit', or 'bye' to end. Type '/clear' to clear conversation history.")
        print("-" * 70)

        # Initialize conversation manager if memory is enabled
        conversation = None if args.no_memory else ConversationManager()

        while True:
            try:
                user_input = input("\nYou: ").strip()
                
                # Handle special commands
                if user_input.lower() in ["exit", "quit", "bye"]:
                    print("Goodbye!")
                    break
                
                if user_input.lower() == "/clear":
                    if conversation:
                        conversation.clear()
                        print("Conversation history cleared.")
                    else:
                        print("No conversation memory to clear.")
                    continue
                
                if user_input.lower() == "/status":
                    if conversation:
                        print(f"Status: {conversation.get_conversation_summary()}")
                    else:
                        print("Status: Conversation memory disabled")
                    continue

                if not user_input:
                    continue

                print("Claude: ", end="")
                
                if conversation:
                    # Add user message to conversation history
                    conversation.add_user_message(user_input)
                    # Get response with full conversation context
                    response = chat_with_conversation(
                        conversation.get_messages(), args.model, args.max_tokens
                    )
                    # Add assistant response to conversation history
                    conversation.add_assistant_message(response)
                else:
                    # No memory mode - single message
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