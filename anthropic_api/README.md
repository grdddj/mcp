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

# Interactive mode  
uv run claude-cli -i

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
- `--interactive` / `-i`: Start interactive chat mode
- `--help`: Show help message

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