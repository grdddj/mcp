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
- `--help`: Show help message

## Interactive Mode Features

**Conversation Memory (default)**:
- Claude remembers the entire conversation context
- Each response builds on previous messages
- Automatic context window management (keeps last 20 messages)

**Special Commands in Interactive Mode**:
- `/clear` - Clear conversation history
- `/status` - Show conversation status
- `exit`, `quit`, `bye` - Exit the program

**Memory Management**:
- Automatically trims old messages to stay within context limits
- Preserves user/assistant message pairs when trimming
- Use `--no-memory` flag for independent messages (like the old behavior)

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