# FastMCP Demo Server

A comprehensive MCP (Model Context Protocol) server built with FastMCP, showcasing various tools and resources for mathematical calculations, text processing, file operations, and more.

## Features

### 🧮 Mathematical Tools
- **add_numbers**, **multiply_numbers** - Basic arithmetic operations
- **calculate_factorial** - Calculate factorial of numbers
- **is_prime** - Check if a number is prime
- **generate_fibonacci** - Generate Fibonacci sequences
- **generate_primes** - Generate prime numbers up to a limit

### 📝 Text Processing Tools
- **reverse_text** - Reverse any text string
- **count_words** - Count words in text
- **text_statistics** - Comprehensive text analysis
- **capitalize_words** - Capitalize each word

### 🔧 System & Utilities
- **get_current_time** - Get current timestamp
- **get_system_info** - System information
- **generate_uuid** - Generate UUIDs
- **hash_text** - Hash text with various algorithms (MD5, SHA1, SHA256, SHA512)
- **encode_base64** / **decode_base64** - Base64 encoding/decoding

### 📁 File Operations
- **write_json_file** - Write JSON data to files
- **read_json_file** - Read JSON data from files
- **list_files** - List files in directories

### 📊 Data Generation
- **create_sample_data** - Generate sample employee records

### 📖 Resources
- **resource://server-info** - Server metadata and information
- **resource://sample-config** - Sample application configuration
- **resource://math-constants** - Mathematical constants (π, e, etc.)
- **data://sample-employees** - Sample employee dataset
- **resource://help** - Comprehensive help documentation

## Installation

1. Install FastMCP:
```bash
pip install fastmcp
```

## Running the Server

### Option 1: STDIO Transport (Default)
```bash
python fastmcp_server.py
```

### Option 2: HTTP Transport
```bash
python run_http.py
```

### Option 3: Using FastMCP CLI
```bash
# With configuration file
fastmcp run fastmcp.json

# Direct file execution
fastmcp run fastmcp_server.py

# HTTP transport with CLI
fastmcp run fastmcp_server.py --transport http --port 8000
```

## Testing

Run the test client to verify all functionality:
```bash
python test_client.py
```

## Usage Examples

### Mathematical Operations
```json
{
  "tool": "add_numbers",
  "arguments": {"a": 15, "b": 27}
}
```

### Text Processing
```json
{
  "tool": "text_statistics", 
  "arguments": {"text": "Hello, FastMCP world!"}
}
```

### Data Generation
```json
{
  "tool": "create_sample_data",
  "arguments": {"count": 5}
}
```

### Resource Access
- Read `resource://server-info` for server metadata
- Read `resource://help` for detailed usage instructions
- Read `data://sample-employees` for sample data

## Configuration

The server can be configured using `fastmcp.json`:

```json
{
  "$schema": "https://gofastmcp.com/schemas/fastmcp_config/v1.json",
  "entrypoint": {
    "file": "fastmcp_server.py",
    "object": "mcp"
  },
  "deployment": {
    "transport": "http",
    "host": "127.0.0.1",
    "port": 8000
  }
}
```

## Files Structure

- `fastmcp_server.py` - Main server implementation
- `run_http.py` - HTTP server runner
- `test_client.py` - Test client for functionality verification
- `fastmcp.json` - Configuration file
- `README.md` - This documentation

## Requirements

- Python 3.8+
- FastMCP 2.12.0+

## License

MIT License - Feel free to use and modify for your projects!