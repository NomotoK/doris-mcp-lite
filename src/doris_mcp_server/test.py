import asyncio
import argparse
import json
from mcp import ClientSession
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters

async def test_resources(session: ClientSession):
    print("== 列出所有资源 ==")
    resources = await session.list_resources()
    for res in resources.resources:
        print(f"- {res.uri} ({res.name})")

    if resources.resources:
        print("\n== 读取第一个资源 ==")
        uri = resources.resources[0].uri
        content, mime_type = await session.read_resource(uri)
        print(f"内容类型: {mime_type}\n内容预览:\n{content[:500]}...")

async def test_tools(session: ClientSession):
    print("== 列出所有工具 ==")
    tools = await session.list_tools()
    for tool in tools.tools:
        print(f"- {tool.name}: {tool.description}")

    if tools.tools:
        tool = tools.tools[0]
        print(f"\n== 调用第一个工具：{tool.name} ==")

        # 构造默认的空参数，如果需要可以在这里根据schema生成
        args = {}
        for key, schema in tool.inputSchema.get("properties", {}).items():
            if schema.get("type") == "string":
                args[key] = "test"
            elif schema.get("type") == "integer":
                args[key] = 1
            elif schema.get("type") == "number":
                args[key] = 1.0
            elif schema.get("type") == "boolean":
                args[key] = True
            else:
                args[key] = None

        print(f"调用参数: {json.dumps(args)}")
        result = await session.call_tool(tool.name, arguments=args)
        print(f"返回结果: {result}")

async def test_prompts(session: ClientSession):
    print("== 列出所有提示词 (prompts) ==")
    prompts = await session.list_prompts()
    for prompt in prompts.prompts:
        print(f"- {prompt.name}: {prompt.description}")

    if prompts.prompts:
        prompt = prompts.prompts[0]
        print(f"\n== 获取第一个提示词：{prompt.name} ==")
        response = await session.get_prompt(prompt.name, arguments={})
        print("提示词返回内容:")
        print(response)

async def main():
    parser = argparse.ArgumentParser(description="MCP Server 测试工具")
    parser.add_argument("--server", type=str, required=True, help="Server 启动脚本路径，例如 server.py")
    parser.add_argument("--test", type=str, required=True, choices=["resources", "tools", "prompts", "all"], help="要测试的功能")
    args = parser.parse_args()

    # 连接到 MCP Server
    server_params = StdioServerParameters(command="python", args=[args.server])
    async with stdio_client(server_params) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()

            if args.test in ["resources", "all"]:
                await test_resources(session)
            if args.test in ["tools", "all"]:
                await test_tools(session)
            if args.test in ["prompts", "all"]:
                await test_prompts(session)

if __name__ == "__main__":
    asyncio.run(main())