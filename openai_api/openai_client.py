import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Optional, Iterator

def get_openai_response(
    request: str, 
    model: Optional[str] = None, 
    stream: bool = False,
    api_key: Optional[str] = None
) -> str | Iterator[str]:
    """
    Get response from OpenAI API.
    
    Args:
        request: The prompt/request text
        model: Model to use (defaults to OPENAI_MODEL env var or gpt-4o)
        stream: Whether to return streaming response
        api_key: API key (defaults to OPENAI_API_KEY env var)
    
    Returns:
        String response or Iterator of string chunks if streaming
    
    Raises:
        ValueError: If API key is not provided or found in environment
        Exception: For OpenAI API errors
    """
    load_dotenv()
    
    # Get API key
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables or .env file")
    
    # Get model
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-4o")
    
    client = OpenAI(api_key=api_key)
    
    completion = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": request}],
        stream=stream
    )
    
    if stream:
        def response_generator():
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content
        return response_generator()
    else:
        return completion.choices[0].message.content