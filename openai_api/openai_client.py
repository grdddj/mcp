import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import Iterator, NamedTuple


class TokenUsage(NamedTuple):
    """Token usage information from OpenAI API response.

    This NamedTuple contains comprehensive token usage statistics and cost estimation
    for OpenAI API requests. All token counts are provided by the OpenAI API response.

    Attributes:
        prompt_tokens: Number of tokens in the input/prompt
        completion_tokens: Number of tokens in the generated response
        total_tokens: Sum of prompt_tokens and completion_tokens
        estimated_cost: Calculated cost in USD based on current pricing
    """

    prompt_tokens: int
    completion_tokens: int
    total_tokens: int
    estimated_cost: float


class OpenAIResponse(NamedTuple):
    """Complete OpenAI API response containing content and usage statistics.

    This is the primary return type for the get_openai_response() function.
    The content can be either a string (for non-streaming responses) or an
    Iterator[str] (for streaming responses). Token usage is only available
    for non-streaming responses due to OpenAI API limitations.

    Attributes:
        content: The response content (string) or streaming iterator
        usage: Token usage statistics, None for streaming responses

    Example:
        # Non-streaming response
        response = get_openai_response("Hello")
        print(response.content)  # "Hello! How can I help you?"
        print(response.usage.total_tokens)  # 25

        # Streaming response
        response = get_openai_response("Hello", stream=True)
        for chunk in response.content:
            print(chunk, end="")  # Stream chunks as they arrive
        print(response.usage)  # None
    """

    content: str | Iterator[str]
    usage: TokenUsage | None


def estimate_cost(model: str, prompt_tokens: int, completion_tokens: int) -> float:
    """Calculate estimated cost for OpenAI API usage based on token consumption.

    Uses current OpenAI pricing (as of 2024) to estimate the cost of an API request.
    Pricing is based on per-million-token rates with separate input and output pricing.
    Falls back to gpt-4o pricing for unknown models.

    Args:
        model: The OpenAI model name (e.g., 'gpt-4o', 'gpt-3.5-turbo')
        prompt_tokens: Number of tokens in the input prompt
        completion_tokens: Number of tokens in the generated completion

    Returns:
        Estimated cost in USD as a float

    Example:
        >>> estimate_cost('gpt-4o', 1000, 500)
        0.0075  # $0.0075 for 1000 input + 500 output tokens

    Note:
        Pricing is subject to change by OpenAI. Update the pricing dictionary
        when new rates are announced.
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
    """Core function to get responses from OpenAI's ChatGPT API with full feature support.

    This is the primary reusable function for interacting with OpenAI's chat completion API.
    It supports both single-shot queries and multi-turn conversations with context preservation,
    streaming responses, token usage tracking, and cost estimation.

    The function handles environment configuration, conversation context management, and
    provides comprehensive response information including token usage statistics.

    Args:
        request: The user's prompt or question text
        model: OpenAI model to use. If None, uses OPENAI_MODEL env var or defaults to 'gpt-4o'
        stream: If True, returns streaming response iterator. If False, returns complete response
        api_key: OpenAI API key. If None, uses OPENAI_API_KEY env var
        conversation_history: List of previous message dicts for context.
                            Each dict should have 'role' ('user'/'assistant') and 'content' keys

    Returns:
        OpenAIResponse containing:
        - content: Response text (str) or streaming iterator (Iterator[str])
        - usage: TokenUsage with stats and cost (None for streaming responses)

    Raises:
        ValueError: If API key is not provided or found in environment variables
        Exception: For OpenAI API errors (rate limits, invalid model, etc.)

    Example:
        # Simple usage
        response = get_openai_response("What is Python?")
        print(response.content)
        print(f"Cost: ${response.usage.estimated_cost:.4f}")

        # With conversation context
        history = [
            {"role": "user", "content": "My name is Alice"},
            {"role": "assistant", "content": "Nice to meet you, Alice!"}
        ]
        response = get_openai_response("What's my name?", conversation_history=history)

        # Streaming response
        response = get_openai_response("Tell me a story", stream=True)
        for chunk in response.content:
            print(chunk, end="", flush=True)

    Note:
        - Streaming responses cannot provide token usage statistics due to API limitations
        - Conversation history is automatically extended with the current request
        - Cost estimation uses current OpenAI pricing and may become outdated
        - The function loads .env file automatically for environment variables
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
        # For streaming responses, usage statistics are not available from the API
        def response_generator() -> Iterator[str]:
            """Generator that yields content chunks from streaming response.

            Yields:
                str: Content chunks as they arrive from the API
            """
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
