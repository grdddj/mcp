"""
CLI interface for the Claude API tool
"""

import argparse
import sys
from claude_api import (
    chat_with_claude,
    chat_with_claude_detailed,
    chat_with_conversation,
    chat_with_conversation_detailed,
    get_default_model,
    ConversationManager,
)


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
        "--interactive",
        "-i",
        action="store_true",
        help="Start interactive chat mode with conversation memory",
    )
    parser.add_argument(
        "--no-memory",
        action="store_true",
        help="Disable conversation memory in interactive mode",
    )
    parser.add_argument(
        "--show-tokens",
        action="store_true",
        help="Display token usage and cost information",
    )

    args = parser.parse_args()

    if args.interactive:
        # Interactive mode with conversation memory
        memory_status = "disabled" if args.no_memory else "enabled"
        print(
            f"Starting interactive chat with Claude ({args.model}). Conversation memory: {memory_status}."
        )
        show_tokens_help = " Token usage will be displayed." if args.show_tokens else ""
        print(
            f"Type 'exit', 'quit', or 'bye' to end. Type '/clear' to clear conversation history.{show_tokens_help}"
        )
        print(
            "Additional commands: '/status' (conversation info), '/usage' (token usage), '/reset' (reset usage tracking)"
        )
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

                if user_input.lower() == "/usage":
                    if conversation:
                        print(f"Usage: {conversation.get_usage_summary()}")
                    else:
                        print(
                            "Usage tracking not available without conversation memory"
                        )
                    continue

                if user_input.lower() == "/reset":
                    if conversation:
                        conversation.reset_usage()
                        print("Usage tracking reset.")
                    else:
                        print("No usage tracking to reset")
                    continue

                if not user_input:
                    continue

                print("Claude: ", end="")

                if conversation:
                    # Add user message to conversation history
                    conversation.add_user_message(user_input)
                    # Get response with full conversation context
                    if args.show_tokens:
                        claude_response = chat_with_conversation_detailed(
                            conversation.get_messages(), args.model, args.max_tokens
                        )
                        response = claude_response.content
                        conversation.record_usage(claude_response.usage)
                    else:
                        response = chat_with_conversation(
                            conversation.get_messages(), args.model, args.max_tokens
                        )
                    # Add assistant response to conversation history
                    conversation.add_assistant_message(response)
                else:
                    # No memory mode - single message
                    if args.show_tokens:
                        claude_response = chat_with_claude_detailed(
                            user_input, args.model, args.max_tokens
                        )
                        response = claude_response.content
                    else:
                        response = chat_with_claude(
                            user_input, args.model, args.max_tokens
                        )

                print(response)

                # Show token usage if requested
                if args.show_tokens:
                    if conversation:
                        # Show current exchange usage
                        if "claude_response" in locals():
                            usage = claude_response.usage
                            print(
                                f"\n[Tokens: {usage.input_tokens:,} in, {usage.output_tokens:,} out, ${usage.cost_estimate:.4f}]"
                            )
                        # Show session total
                        print(f"[{conversation.get_usage_summary()}]")
                    else:
                        if "claude_response" in locals():
                            usage = claude_response.usage
                            print(
                                f"\n[Tokens: {usage.input_tokens:,} in, {usage.output_tokens:,} out, ${usage.cost_estimate:.4f}]"
                            )

            except KeyboardInterrupt:
                print("\nGoodbye!")
                break
            except EOFError:
                print("\nGoodbye!")
                break

    elif args.message:
        # Single message mode
        if args.show_tokens:
            claude_response = chat_with_claude_detailed(
                args.message, args.model, args.max_tokens
            )
            print(claude_response.content)
            usage = claude_response.usage
            print(
                f"\n[Tokens: {usage.input_tokens:,} in, {usage.output_tokens:,} out, ${usage.cost_estimate:.4f}]"
            )
        else:
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
            if args.show_tokens:
                claude_response = chat_with_claude_detailed(
                    message, args.model, args.max_tokens
                )
                print(claude_response.content)
                usage = claude_response.usage
                print(
                    f"\n[Tokens: {usage.input_tokens:,} in, {usage.output_tokens:,} out, ${usage.cost_estimate:.4f}]"
                )
            else:
                response = chat_with_claude(message, args.model, args.max_tokens)
                print(response)


if __name__ == "__main__":
    main()
