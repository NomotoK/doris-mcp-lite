from mcp.server.fastmcp import FastMCP
from db import SQLTools
from res.resources import DorisSchemaResource
from prompts.general_prompts import GeneralPrompts
from prompts.customize_prompts import CustomizePrompts



# 实例化唯一的 MCP Server
mcp = FastMCP("DorisServer")

class MCPDorisServer:

    def __init__(self):
        self.server = mcp

        # 初始化工具类与资源类并注册
        self.sql_tools = SQLTools()
        self.schema_resource = DorisSchemaResource()
        self.general_prompts = GeneralPrompts()
        self.cutomize_prompts = CustomizePrompts()

        self._register_components()

    def _register_components(self):
        """
        注册工具类与资源类至 MCP 服务器实例
        """
        self.server.include(self.sql_tools)
        self.server.include(self.schema_resource)
        self.server.include(self.general_prompts)
        self.server.include(self.cutomize_prompts)

    def run(self):
        """
        启动 MCP Server
        """
        self.server.run()


if __name__ == "__main__":
    app = MCPDorisServer()
    app.run()
