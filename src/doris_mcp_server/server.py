from doris_mcp_server.mcp_app import mcp
from doris_mcp_server.db import tools
from doris_mcp_server.res import resources
from doris_mcp_server.prompts import general_prompts, customize_prompts
import traceback


class MCPDorisServer:

    def __init__(self):
        self.server = mcp


    def run(self):
        """
        启动 MCP Server
        """
        try:
            print("🚀 MCP Doris Server is starting...")
            self.server.run()
        except Exception as e:
            print("🚨 MCP Doris Server failed to start.")
            print(f"Error: {e}")
            traceback.print_exc()


def main():
    app = MCPDorisServer()
    app.run()

if __name__ == "__main__":
    main()
