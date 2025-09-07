import argparse
from openai_client import get_openai_response


def interactive_mode(model=None, stream=False):
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

                response = get_openai_response(
                    request=user_input,
                    model=model,
                    stream=stream,
                    conversation_history=conversation_history,
                )

                # Handle response and update conversation history
                if stream:
                    full_response = ""
                    for chunk in response:
                        print(chunk, end="", flush=True)
                        full_response += chunk
                    print()
                    assistant_response = full_response
                else:
                    print(response)
                    assistant_response = response

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

    args = parser.parse_args()

    # Interactive mode
    if args.interactive:
        return interactive_mode(model=args.model, stream=args.stream)

    # Single prompt mode
    if not args.prompt:
        parser.error("prompt is required unless using --interactive mode")

    try:
        response = get_openai_response(
            request=args.prompt, model=args.model, stream=args.stream
        )

        if args.stream:
            for chunk in response:
                print(chunk, end="", flush=True)
            print()
        else:
            print(response)

    except Exception as e:
        print(f"Error: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
