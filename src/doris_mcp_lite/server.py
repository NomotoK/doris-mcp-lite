import os
import sys
import asyncio
from doris_mcp_lite import config
from doris_mcp_lite.mcp_app import mcp
from doris_mcp_lite import config
from doris_mcp_lite.db import tools, DorisConnector
from doris_mcp_lite.res import resources
from doris_mcp_lite.prompts import general_prompts, customize_prompts
import traceback

class MCPDorisServer:

    def __init__(self):
        self.server = mcp


    async def _test_db_connection(self):
        """
        测试数据库连接是否成功。
        """
        try:
            async with DorisConnector() as conn:
                result = await conn.execute_query("SELECT 1")
                if result:
                    print("✅ Database connection successful.")
                else:
                    raise Exception("Database connection test failed: please config .env file.")
        except Exception as e:
            print("❌ Database connection test failed.")
            raise e


    async def run_async(self):
        """
        启动 MCP Server
        """
        try:
            print("🚀 Doris MCP Server is starting...")
            await self._test_db_connection()
            await self.server.run_stdio_async()
        except Exception as e:
            print("🚨 Doris MCP Server failed to start.")
            print(f"Error: {e}")
            traceback.print_exc()


async def main():
    if len(sys.argv) > 1:
        os.environ["DORIS_URL"] = sys.argv[1]

    config.init_config()

    server = MCPDorisServer()
    await server.run_async()