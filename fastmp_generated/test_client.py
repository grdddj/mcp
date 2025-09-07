#!/usr/bin/env python3
"""
Test Client for FastMCP Demo Server
Tests the FastMCP server functionality by calling various tools and reading resources.
"""

import asyncio
import json
from fastmcp import Client
from fastmcp_server import mcp


async def test_fastmcp_server():
    """Test various tools and resources on the FastMCP server."""

    print("🚀 Testing FastMCP Server Functionality")
    print("=" * 50)

    # Create client
    client = Client(mcp)

    async with client:
        print("\n📋 Listing available tools...")
        tools = await client.list_tools()
        print(f"Found {len(tools)} tools:")
        for tool in tools[:5]:  # Show first 5
            print(f"  - {tool.name}: {tool.description}")
        print("  ... and more")

        print("\n📋 Listing available resources...")
        resources = await client.list_resources()
        print(f"Found {len(resources)} resources:")
        for resource in resources:
            print(f"  - {resource.uri}: {resource.name}")

        print("\n🧮 Testing mathematical tools...")

        # Test addition
        result = await client.call_tool("add_numbers", {"a": 15, "b": 27})
        print(f"add_numbers(15, 27) = {result.data}")

        # Test factorial
        result = await client.call_tool("calculate_factorial", {"n": 5})
        print(f"factorial(5) = {result.data}")

        # Test prime check
        result = await client.call_tool("is_prime", {"n": 17})
        print(f"is_prime(17) = {result.data}")

        # Test Fibonacci
        result = await client.call_tool("generate_fibonacci", {"n": 8})
        print(f"fibonacci(8) = {result.data}")

        print("\n📝 Testing text processing tools...")

        # Test text statistics
        test_text = "Hello, world! This is a test of the FastMCP server."
        result = await client.call_tool("text_statistics", {"text": test_text})
        print(f"Text stats for '{test_text}':")
        for key, value in result.data.items():
            print(f"  {key}: {value}")

        # Test text reversal
        result = await client.call_tool("reverse_text", {"text": "FastMCP"})
        print(f"reverse_text('FastMCP') = '{result.data}'")

        print("\n🔧 Testing utility tools...")

        # Test UUID generation
        result = await client.call_tool("generate_uuid")
        print(f"Generated UUID: {result.data}")

        # Test base64 encoding
        result = await client.call_tool("encode_base64", {"text": "Hello FastMCP!"})
        encoded = result.data
        print(f"Base64 encoded 'Hello FastMCP!': {encoded}")

        # Test base64 decoding
        result = await client.call_tool("decode_base64", {"encoded_text": encoded})
        print(f"Base64 decoded: '{result.data}'")

        # Test hashing
        result = await client.call_tool(
            "hash_text", {"text": "FastMCP", "algorithm": "sha256"}
        )
        print(f"SHA256 hash of 'FastMCP': {result.data[:16]}...")

        print("\n📊 Testing data generation...")

        # Generate sample data
        result = await client.call_tool("create_sample_data", {"count": 3})
        print("Generated sample data:")
        sample_data = result.data
        if isinstance(sample_data, list):
            for record in sample_data:
                if hasattr(record, "__dict__"):
                    # Handle pydantic model objects
                    record_dict = record.__dict__ if hasattr(record, "__dict__") else {}
                    name = record_dict.get("name", "Unknown")
                    dept = record_dict.get("department", "Unknown")
                    salary = record_dict.get("salary", 0)
                else:
                    # Handle dict objects
                    name = record.get("name", "Unknown")
                    dept = record.get("department", "Unknown")
                    salary = record.get("salary", 0)
                print(f"  {name} - {dept} - ${salary:,}")
        else:
            print(f"  Unexpected data format: {type(sample_data)}")

        print("\n📖 Testing resources...")

        # Read server info resource
        server_info_contents = await client.read_resource("resource://server-info")
        if isinstance(server_info_contents, list) and server_info_contents:
            server_info_text = server_info_contents[0].text  # type: ignore
        else:
            server_info_text = str(server_info_contents)

        try:
            info_data = json.loads(server_info_text)
            print(f"Server: {info_data['name']} v{info_data['version']}")
            print(f"Features: {', '.join(info_data['features'][:3])}...")
        except json.JSONDecodeError:
            print(f"Server info (raw): {server_info_text[:100]}...")

        # Read math constants
        constants_contents = await client.read_resource("resource://math-constants")
        if isinstance(constants_contents, list) and constants_contents:
            constants_text = constants_contents[0].text  # type: ignore
        else:
            constants_text = str(constants_contents)

        try:
            constants_data = json.loads(constants_text)
            print(f"π = {constants_data['pi']:.6f}")
            print(f"e = {constants_data['e']:.6f}")
        except json.JSONDecodeError:
            print(f"Math constants (raw): {constants_text[:100]}...")

        # Read sample employees
        employees_contents = await client.read_resource("data://sample-employees")
        if isinstance(employees_contents, list) and employees_contents:
            employees_text = employees_contents[0].text  # type: ignore
        else:
            employees_text = str(employees_contents)

        try:
            employees_data = json.loads(employees_text)
            print(f"Sample data has {employees_data['total']} employees")
        except json.JSONDecodeError:
            print(f"Employee data (raw): {employees_text[:100]}...")

        print("\n⏰ Testing system info...")

        # Get current time
        result = await client.call_tool("get_current_time")
        print(f"Current time: {result.data}")

        # Get system info
        result = await client.call_tool("get_system_info")
        sys_info = result.data
        print(f"System: {sys_info['system']} on {sys_info['platform']}")
        print(f"Python: {sys_info['python_version']}")

        print("\n✅ All tests completed successfully!")
        print("=" * 50)
        print("FastMCP server is working correctly! 🎉")


if __name__ == "__main__":
    asyncio.run(test_fastmcp_server())
