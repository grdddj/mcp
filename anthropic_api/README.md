# Claude CLI

A simple CLI tool for interacting with Anthropic's Claude API.

## Installation

1. Clone this repository
2. Install dependencies with uv:
   ```bash
   uv sync
   ```
3. Copy the environment file and add your API key:
   ```bash
   cp .env.example .env
   # Edit .env and add your ANTHROPIC_API_KEY
   # Optionally set ANTHROPIC_MODEL for default model
   ```

## Usage

### Install the CLI tool
```bash
uv sync
```

### Run with uv
```bash
# Single message
uv run claude-cli "What's the weather like?"

# Interactive mode with conversation memory
uv run claude-cli -i

# Interactive mode without memory (each message independent)
uv run claude-cli -i --no-memory

# With custom model and token limit
uv run claude-cli "Hello" --model claude-sonnet-4-20250514 --max-tokens 512

# Show token usage and costs
uv run claude-cli "Hello" --show-tokens

# From stdin
echo "Hello Claude" | uv run claude-cli
```

### Install globally (optional)
```bash
uv tool install .
claude-cli "Hello Claude"
```

## Options

- `--model`: Choose Claude model (overrides ANTHROPIC_MODEL from .env)
- `--max-tokens`: Maximum tokens in response (default: 1024)
- `--interactive` / `-i`: Start interactive chat mode with conversation memory
- `--no-memory`: Disable conversation memory in interactive mode
- `--show-tokens`: Display token usage and cost information for each request
- `--help`: Show help message

## Interactive Mode Features

**Conversation Memory (default)**:
- Claude remembers the entire conversation context
- Each response builds on previous messages
- Automatic context window management (keeps last 20 messages)

**Special Commands in Interactive Mode**:
- `/clear` - Clear conversation history
- `/status` - Show conversation status
- `/usage` - Show token usage and cost summary
- `/reset` - Reset usage tracking counters
- `exit`, `quit`, `bye` - Exit the program

**Memory Management**:
- Automatically trims old messages to stay within context limits
- Preserves user/assistant message pairs when trimming
- Use `--no-memory` flag for independent messages (like the old behavior)

## Token Usage Tracking

**Cost Monitoring**:
- Track input/output tokens for each API call
- Model-specific cost calculation (Haiku, Sonnet, Opus pricing)
- Cumulative session cost tracking in interactive mode

**Usage Examples**:
```bash
# Single message with token display
uv run claude-cli "Explain quantum computing" --show-tokens
# Output: [Tokens: 15 in, 245 out, $0.0003]

# Interactive mode with usage tracking
uv run claude-cli -i --show-tokens
# Shows per-message and session totals

# Check usage in interactive mode
/usage  # Shows: Session usage: 5 exchanges, 1,234 tokens (890 in, 344 out), $0.0045
```

**Supported Models & Pricing**:
https://www.anthropic.com/pricing#api
https://token-calculator.net/
- **Claude 3.5 Haiku**: $0.80/$4.00 per 1M tokens (in/out)
- **Claude 4 Sonnet**: $3.00/$15.00 per 1M tokens (in/out)
- **Claude 4.1 Opus**: $15.00/$75.00 per 1M tokens (in/out)

## Environment Variables

- `ANTHROPIC_API_KEY`: Your Anthropic API key (required)
- `ANTHROPIC_MODEL`: Default Claude model (optional, can be overridden by --model)

## Model Selection Priority

1. `--model` CLI argument (highest priority)
2. `ANTHROPIC_MODEL` environment variable
3. Default: `claude-sonnet-4-20250514`

## Example .env file

```
ANTHROPIC_API_KEY=sk-ant-api03-...
ANTHROPIC_MODEL=claude-opus-4-20250514
```
