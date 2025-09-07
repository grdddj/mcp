#!/usr/bin/env python3
"""
Example usage of the reusable get_openai_response function
"""

from openai_client import get_openai_response

def main():
    # Simple usage
    response = get_openai_response("What is Python?")
    print("Simple response:", response)
    
    # With specific model
    response = get_openai_response(
        "Explain quantum computing in one sentence",
        model="gpt-3.5-turbo"
    )
    print("\nWith model:", response)
    
    # Streaming response
    print("\nStreaming response:")
    for chunk in get_openai_response("Tell me a short joke", stream=True):
        print(chunk, end='', flush=True)
    print("\n")

if __name__ == "__main__":
    main()