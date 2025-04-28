from doris_mcp_server.mcp_app import mcp
from doris_mcp_server.db import tools, DorisConnector
from doris_mcp_server.res import resources
from doris_mcp_server.prompts import general_prompts, customize_prompts
import traceback


class MCPDorisServer:

    def __init__(self):
        self.server = mcp


    def _test_db_connection(self):
        """
        测试数据库连接是否成功。
        """
        try:
            conn = DorisConnector()
            result = conn.execute_query("SELECT 1")
            if result:
                print("✅ Database connection successful.")
            else:
                raise Exception("Database connection test failed: please config .env file.")
            conn.close()
        except Exception as e:
            print("❌ Database connection test failed.")
            raise e


    def run(self):
        """
        启动 MCP Server
        """
        try:
            print("🚀 Doris MCP Server is starting...")
            self._test_db_connection()
            self.server.run()
        except Exception as e:
            print("🚨 Doris MCP Server failed to start.")
            print(f"Error: {e}")
            traceback.print_exc()


def main():
    app = MCPDorisServer()
    app.run()

if __name__ == "__main__":
    main()
