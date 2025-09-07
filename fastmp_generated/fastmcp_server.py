#!/usr/bin/env python3
"""
FastMCP Server Demo
A comprehensive MCP server built with FastMCP featuring multiple tools and resources.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP(
    name="Demo FastMCP Server",
    instructions="""
    This is a demonstration FastMCP server showcasing various capabilities:
    - Mathematical calculations and utilities
    - Text processing tools  
    - File operations
    - System information
    - Data generation tools
    
    Use the available tools to perform calculations, process text, work with files, and more.
    """,
)

# Mathematical Tools
@mcp.tool
def add_numbers(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b

@mcp.tool
def multiply_numbers(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b

@mcp.tool
def calculate_factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n == 0 or n == 1:
        return 1
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result

@mcp.tool
def is_prime(n: int) -> bool:
    """Check if a number is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(n**0.5) + 1, 2):
        if n % i == 0:
            return False
    return True

# Text Processing Tools
@mcp.tool
def reverse_text(text: str) -> str:
    """Reverse the given text."""
    return text[::-1]

@mcp.tool
def count_words(text: str) -> int:
    """Count the number of words in the given text."""
    return len(text.split())

@mcp.tool
def text_statistics(text: str) -> Dict[str, int]:
    """Get comprehensive statistics about the text."""
    words = text.split()
    return {
        "characters": len(text),
        "characters_no_spaces": len(text.replace(" ", "")),
        "words": len(words),
        "sentences": len([s for s in text.split('.') if s.strip()]),
        "paragraphs": len([p for p in text.split('\n\n') if p.strip()]),
    }

@mcp.tool
def capitalize_words(text: str) -> str:
    """Capitalize the first letter of each word."""
    return text.title()

# System Information Tools
@mcp.tool
def get_current_time() -> str:
    """Get the current date and time."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@mcp.tool
def get_system_info() -> Dict[str, str]:
    """Get basic system information."""
    import platform
    import os
    
    return {
        "platform": platform.platform(),
        "system": platform.system(),
        "processor": platform.processor(),
        "python_version": platform.python_version(),
        "current_directory": os.getcwd(),
        "user": os.getenv("USER", "unknown"),
    }

# Data Generation Tools
@mcp.tool
def generate_fibonacci(n: int) -> List[int]:
    """Generate the first n numbers in the Fibonacci sequence."""
    if n <= 0:
        return []
    if n == 1:
        return [0]
    if n == 2:
        return [0, 1]
    
    fib = [0, 1]
    for i in range(2, n):
        fib.append(fib[i-1] + fib[i-2])
    return fib

@mcp.tool
def generate_primes(limit: int) -> List[int]:
    """Generate all prime numbers up to the given limit."""
    if limit < 2:
        return []
    
    primes = []
    for num in range(2, limit + 1):
        if num < 2:
            continue
        if num == 2:
            primes.append(num)
            continue
        if num % 2 == 0:
            continue
        
        is_num_prime = True
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                is_num_prime = False
                break
        if is_num_prime:
            primes.append(num)
    return primes

@mcp.tool
def create_sample_data(count: int = 5) -> List[Dict[str, Any]]:
    """Generate sample data records."""
    import random
    
    names = ["Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Henry"]
    departments = ["Engineering", "Marketing", "Sales", "HR", "Finance"]
    
    data = []
    for i in range(count):
        data.append({
            "id": i + 1,
            "name": random.choice(names),
            "department": random.choice(departments),
            "age": random.randint(22, 65),
            "salary": random.randint(40000, 120000),
            "active": random.choice([True, False])
        })
    
    return data

# File Operation Tools
@mcp.tool
def write_json_file(filename: str, data: Dict[str, Any]) -> str:
    """Write data to a JSON file."""
    try:
        filepath = Path(filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return f"Successfully wrote data to {filepath.absolute()}"
    except Exception as e:
        return f"Error writing file: {str(e)}"

@mcp.tool
def read_json_file(filename: str) -> Dict[str, Any]:
    """Read data from a JSON file."""
    try:
        filepath = Path(filename)
        with open(filepath, 'r') as f:
            return json.load(f)
    except Exception as e:
        raise ValueError(f"Error reading file: {str(e)}")

@mcp.tool
def list_files(directory: str = ".") -> List[str]:
    """List files in the specified directory."""
    try:
        path = Path(directory)
        if not path.exists():
            return [f"Directory {directory} does not exist"]
        
        files = []
        for item in path.iterdir():
            if item.is_file():
                files.append(item.name)
        return sorted(files)
    except Exception as e:
        return [f"Error listing files: {str(e)}"]

# Utility Tools
@mcp.tool
def encode_base64(text: str) -> str:
    """Encode text to base64."""
    import base64
    return base64.b64encode(text.encode()).decode()

@mcp.tool
def decode_base64(encoded_text: str) -> str:
    """Decode base64 text."""
    import base64
    try:
        return base64.b64decode(encoded_text).decode()
    except Exception as e:
        raise ValueError(f"Invalid base64 string: {str(e)}")

@mcp.tool
def generate_uuid() -> str:
    """Generate a random UUID."""
    import uuid
    return str(uuid.uuid4())

@mcp.tool
def hash_text(text: str, algorithm: str = "sha256") -> str:
    """Hash text using the specified algorithm (md5, sha1, sha256, sha512)."""
    import hashlib
    
    algorithms = {
        "md5": hashlib.md5,
        "sha1": hashlib.sha1,
        "sha256": hashlib.sha256,
        "sha512": hashlib.sha512,
    }
    
    if algorithm not in algorithms:
        raise ValueError(f"Unsupported algorithm. Use one of: {', '.join(algorithms.keys())}")
    
    hash_obj = algorithms[algorithm]()
    hash_obj.update(text.encode())
    return hash_obj.hexdigest()

# Resources
@mcp.resource("resource://server-info")
def get_server_info() -> str:
    """Get information about this FastMCP server."""
    return json.dumps({
        "name": "Demo FastMCP Server",
        "version": "1.0.0",
        "description": "A comprehensive demonstration server built with FastMCP",
        "features": [
            "Mathematical calculations",
            "Text processing",
            "File operations", 
            "System information",
            "Data generation",
            "Utility functions"
        ],
        "total_tools": 20,
        "created": "2025-01-01",
        "author": "FastMCP Demo"
    }, indent=2)

@mcp.resource("resource://sample-config")  
def get_sample_config() -> str:
    """Get a sample configuration file."""
    config = {
        "server": {
            "name": "MyApp",
            "port": 8000,
            "debug": False
        },
        "database": {
            "host": "localhost",
            "port": 5432,
            "name": "myapp_db"
        },
        "features": {
            "auth": True,
            "logging": True,
            "metrics": False
        }
    }
    return json.dumps(config, indent=2)

@mcp.resource("resource://math-constants")
def get_math_constants() -> str:
    """Get common mathematical constants."""
    import math
    constants = {
        "pi": math.pi,
        "e": math.e,
        "tau": math.tau,
        "golden_ratio": (1 + math.sqrt(5)) / 2,
        "sqrt_2": math.sqrt(2),
        "sqrt_3": math.sqrt(3),
        "euler_mascheroni": 0.5772156649015329
    }
    return json.dumps(constants, indent=4)

@mcp.resource("data://sample-employees")
def get_sample_employees() -> str:
    """Get sample employee data."""
    employees = [
        {"id": 1, "name": "Alice Johnson", "department": "Engineering", "salary": 75000},
        {"id": 2, "name": "Bob Smith", "department": "Marketing", "salary": 65000},
        {"id": 3, "name": "Carol Davis", "department": "Sales", "salary": 70000},
        {"id": 4, "name": "David Wilson", "department": "HR", "salary": 60000},
        {"id": 5, "name": "Eve Brown", "department": "Finance", "salary": 72000}
    ]
    return json.dumps({"employees": employees, "total": len(employees)}, indent=2)

@mcp.resource("resource://help")
def get_help() -> str:
    """Get help information for using this server."""
    help_text = """
# FastMCP Server Help

## Available Tool Categories:

### Mathematical Tools
- add_numbers(a, b) - Add two numbers
- multiply_numbers(a, b) - Multiply two numbers  
- calculate_factorial(n) - Calculate factorial
- is_prime(n) - Check if number is prime
- generate_fibonacci(n) - Generate Fibonacci sequence
- generate_primes(limit) - Generate primes up to limit

### Text Processing
- reverse_text(text) - Reverse text
- count_words(text) - Count words
- text_statistics(text) - Get text stats
- capitalize_words(text) - Capitalize words

### System & Utilities
- get_current_time() - Get current timestamp
- get_system_info() - Get system information
- generate_uuid() - Generate UUID
- hash_text(text, algorithm) - Hash text

### File Operations
- write_json_file(filename, data) - Write JSON file
- read_json_file(filename) - Read JSON file
- list_files(directory) - List files in directory

### Encoding
- encode_base64(text) - Encode to base64
- decode_base64(encoded_text) - Decode from base64

### Data Generation
- create_sample_data(count) - Generate sample records

## Available Resources:
- resource://server-info - Server information
- resource://sample-config - Sample configuration
- resource://math-constants - Mathematical constants
- data://sample-employees - Sample employee data
- resource://help - This help text

## Usage Examples:
1. Call add_numbers with parameters: {"a": 5, "b": 3}
2. Get server info by reading resource://server-info
3. Generate 10 Fibonacci numbers: {"n": 10}
"""
    return help_text.strip()

if __name__ == "__main__":
    # Run the server with stdio transport (default)
    print("Starting FastMCP server...")
    print("Use 'fastmcp run fastmcp_server.py' to start via CLI")
    print("Or run this script directly for stdio transport")
    
    mcp.run()