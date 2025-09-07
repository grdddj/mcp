# OpenAI CLI Tool

A simple CLI tool for interacting with OpenAI's ChatGPT API.

## Installation and Usage

### Using uv tool (recommended)

Install and run directly with uv:

```bash
# Run once
uv tool run --from . openai-cli "Your prompt here"

# Install as a tool
uv tool install .

# Then use anywhere
openai-cli "Your prompt here"
```

### Development setup

```bash
# Clone and setup
cd openai_api
cp .env.example .env
# Edit .env with your OpenAI API key

# Install dependencies
uv sync

# Run in development
uv run openai_cli.py "Your prompt here"
```

## Configuration

1. Copy `.env.example` to `.env`
2. Add your OpenAI API key: `OPENAI_API_KEY=your_key_here`

## Usage Examples

```bash
# Basic usage
openai-cli "Explain quantum computing"

# Use different model
openai-cli -m gpt-3.5-turbo "Write a haiku"

# Stream response
openai-cli -s "Tell me a story"
```

## Options

- `-m, --model`: Choose model (default: gpt-4o)
- `-s, --stream`: Stream the response
- `-h, --help`: Show help