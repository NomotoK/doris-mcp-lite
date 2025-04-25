from mcp.server.fastmcp import FastMCP
from config import DB_CONFIG, MCP_SERVER_NAME, DEBUG
from res.resources import DorisSchemaResource
from db import SQLTools


from db.db import DorisConnector

# db = DorisConnector()
# doris_schema_res = DorisSchemaResource()
sql_tools = SQLTools()

# tables = doris_schema_res.all_table_schemas("cdqj_dws")
# print(tables)

query = "SELECT COUNT(*) FROM dws_tbl_preliminary_abnormal"
print(sql_tools.run_select_query(query))

# schema = doris_schema_res.table_schema("dws_tbl_preliminary_abnormal")
# print(schema)

# tables = db.list_tables("cdqj_dws")
# print(tables)

# schema = db.get_table_schema("dws_tbl_preliminary_abnormal")
# print(schema)

# result = db.execute_query("SELECT * FROM dws_tbl_preliminary_abnormal LIMIT 5")
# print(result)

# db.close()

