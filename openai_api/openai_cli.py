import argparse
from openai_client import get_openai_response

def main():
    parser = argparse.ArgumentParser(description="Simple CLI for OpenAI ChatGPT API")
    parser.add_argument("prompt", help="Your prompt for ChatGPT")
    parser.add_argument("-m", "--model", help="Model to use (overrides OPENAI_MODEL from .env)")
    parser.add_argument("-s", "--stream", action="store_true", help="Stream the response")
    
    args = parser.parse_args()
    
    try:
        response = get_openai_response(
            request=args.prompt,
            model=args.model,
            stream=args.stream
        )
        
        if args.stream:
            for chunk in response:
                print(chunk, end='', flush=True)
            print()
        else:
            print(response)
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())