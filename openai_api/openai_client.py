import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Iterator, NamedTuple


class TokenUsage(NamedTuple):
    """Token usage information"""

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float


class OpenAIResponse(NamedTuple):
    """OpenAI response with token usage"""

    content: str | Iterator[str]
    usage: TokenUsage | None


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """
    Estimate cost based on model and token usage.
    Prices as of 2024 (per 1M tokens).
    """
    # Pricing per 1M tokens (input, output)
    pricing = {
        "gpt-4o": (2.50, 10.00),
        "gpt-4o-2024-08-06": (2.50, 10.00),
        "gpt-4o-2024-05-13": (5.00, 15.00),
        "gpt-4o-mini": (0.15, 0.60),
        "gpt-4o-mini-2024-07-18": (0.15, 0.60),
        "gpt-4-turbo": (10.00, 30.00),
        "gpt-4": (30.00, 60.00),
        "gpt-3.5-turbo": (0.50, 1.50),
        "gpt-3.5-turbo-0125": (0.50, 1.50),
    }

    if model not in pricing:
        # Default to gpt-4o pricing if unknown
        input_price, output_price = pricing["gpt-4o"]
    else:
        input_price, output_price = pricing[model]

    # Calculate cost (prices are per 1M tokens)
    input_cost = (prompt_tokens / 1_000_000) * input_price
    output_cost = (completion_tokens / 1_000_000) * output_price

    return input_cost + output_cost


def get_openai_response(
    request: str,
    model: str | None = None,
    stream: bool = False,
    api_key: str | None = None,
    conversation_history: list[dict[str, str]] | None = None,
) -> OpenAIResponse:
    """
    Get response from OpenAI API.

    Args:
        request: The prompt/request text
        model: Model to use (defaults to OPENAI_MODEL env var or gpt-4o)
        stream: Whether to return streaming response
        api_key: API key (defaults to OPENAI_API_KEY env var)
        conversation_history: List of previous messages in conversation

    Returns:
        OpenAIResponse with content and token usage information

    Raises:
        ValueError: If API key is not provided or found in environment
        Exception: For OpenAI API errors
    """
    load_dotenv()

    # Get API key
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY not found in environment variables or .env file"
        )

    # Get model
    if model is None:
        model = os.getenv("OPENAI_MODEL", "gpt-4o")

    client = OpenAI(api_key=api_key)

    # Build messages list with conversation history
    messages = []
    if conversation_history:
        messages.extend(conversation_history)
    messages.append({"role": "user", "content": request})

    completion = client.chat.completions.create(
        model=model,
        messages=messages,
        stream=stream,
    )

    if stream:
        # For streaming, we can't get usage info, so return None
        def response_generator():
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    yield chunk.choices[0].delta.content

        return OpenAIResponse(content=response_generator(), usage=None)
    else:
        usage = completion.usage
        cost = estimate_cost(model, usage.prompt_tokens, usage.completion_tokens)

        token_usage = TokenUsage(
            prompt_tokens=usage.prompt_tokens,
            completion_tokens=usage.completion_tokens,
            total_tokens=usage.total_tokens,
            estimated_cost=cost,
        )

        return OpenAIResponse(
            content=completion.choices[0].message.content, usage=token_usage
        )
