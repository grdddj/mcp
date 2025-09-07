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
3. Optionally set default model: `OPENAI_MODEL=gpt-4o-mini`

## Usage Examples

### Basic Usage
```bash
# Simple one-time question
openai-cli "What is Python?"

# Use a different model
openai-cli -m gpt-3.5-turbo "Write a haiku about coding"

# Stream the response in real-time
openai-cli -s "Tell me a long story about a robot"
```

### Interactive Mode
```bash
# Start interactive conversation (remembers context)
openai-cli -i

# Interactive mode with streaming
openai-cli -i -s

# Interactive mode with specific model
openai-cli -i -m gpt-4o-mini
```

### Token Usage Statistics
```bash
# Show token usage and cost estimation
openai-cli "Explain machine learning" --stats

# Interactive mode with stats after each response
openai-cli -i --stats

# Note: Stats not available in streaming mode
openai-cli -s --stats "Tell a story"  # Shows warning
```

### Combined Examples
```bash
# Interactive conversation with custom model and stats
openai-cli -i -m gpt-3.5-turbo --stats

# One-shot with specific model and stats
openai-cli -m gpt-4o-mini --stats "What are the benefits of renewable energy?"
```

## Options

- `prompt`: Your question/prompt (optional in interactive mode)
- `-m, --model`: Choose model (overrides OPENAI_MODEL from .env)
- `-s, --stream`: Stream the response in real-time
- `-i, --interactive`: Start interactive conversation mode with context memory
- `--stats`: Show token usage statistics and cost estimation
- `-h, --help`: Show help

## Interactive Mode Features

When using `-i` or `--interactive`:
- **Context Memory**: Remembers your entire conversation
- **Multiple Exit Options**: Type `exit`, `quit`, or press `Ctrl+C`
- **Works with all flags**: Combine with `-s` for streaming, `--stats` for usage info
- **Model Selection**: Set model once for the entire session

Example interactive session:
```
$ openai-cli -i --stats
Interactive mode started. Type 'exit', 'quit', or press Ctrl+C to exit.
==================================================

You: What is Python?
Assistant: Python is a high-level programming language...

📊 Token Usage Stats:
   Model: gpt-4o
   Input tokens: 12
   Output tokens: 95
   Total tokens: 107
   Estimated cost: $0.000980

You: Can you give me an example?
Assistant: [Remembers we were talking about Python and gives relevant example]

📊 Token Usage Stats:
   Model: gpt-4o
   Input tokens: 112  # Note: Includes conversation history
   Output tokens: 156
   Total tokens: 268
   Estimated cost: $0.001840

You: exit
Goodbye!
```

## Cost Estimation

The `--stats` flag provides accurate cost estimation based on current OpenAI pricing (2024):

- **gpt-4o**: $2.50/$10.00 per 1M input/output tokens
- **gpt-4o-mini**: $0.15/$0.60 per 1M input/output tokens  
- **gpt-3.5-turbo**: $0.50/$1.50 per 1M input/output tokens
- **gpt-4**: $30.00/$60.00 per 1M input/output tokens

**Note**: Token statistics are only available in non-streaming mode. Streaming mode will show a warning if `--stats` is used.