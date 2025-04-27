# mcp_app.py
from mcp.server.fastmcp import FastMCP
from doris_mcp_server.config import MCP_SERVER_NAME


# 实例化唯一的 MCP Server
mcp = FastMCP(MCP_SERVER_NAME)
