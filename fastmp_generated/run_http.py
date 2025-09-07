#!/usr/bin/env python3
"""
HTTP Server Runner for FastMCP Demo
Runs the FastMCP server with HTTP transport for web-based access.
"""

from fastmcp_server import mcp

if __name__ == "__main__":
    print("Starting FastMCP server with HTTP transport...")
    print("Server will be available at: http://127.0.0.1:8000")
    print("Press Ctrl+C to stop the server")
    
    # Run with HTTP transport
    mcp.run(
        transport="http",
        host="127.0.0.1", 
        port=8000,
        show_banner=True
    )