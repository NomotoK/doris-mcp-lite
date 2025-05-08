# **📖 INSTALL.md**

This guide will walk you through how to install **Doris-MCP-Server** using the provided **setup.sh** script, and configure the database connection needed for it to function properly.

## **🚀 Prerequisites**

Before you start, make sure you have:

- **Python 3.10+** installed (recommend 3.12)
- **git** installed
- **uv** installed
	- If not installed, run:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```
> [!NOTE]
> In version 0.0.2, we have added automatic installation of uv in the setup.sh script. You can choose to install uv during installation process. If you have installed uv before, please make sure it is updated to the latest version.

## **📦 Installation Steps**

### Option 1: automatic install:

1. **Download `setup.sh` on your machine.**

2. **Make the script executable:**

```bash
chmod +x setup.sh
```

3. Run the script:

```bash
./setup.sh
```

The script will automatically install the server and help you walk through database configuration.

### Option 2: install with source code and configure connection with `setup.sh`

1. **Download or clone this repository**
  
If you have not already cloned the repository, you can clone it via:

```bash
git clone git@github.com:NomotoK/doris-mcp-server.git
cd doris-mcp-server
```

2. **Run the installation and setup script**

Inside the project root directory, run:

```bash
bash setup.sh
```

and then follow the commands.

preview of installation process:

```bash
./setup.sh
-------------------------------------------
🚀 Welcome to Doris-MCP-Server Setup Wizard
-------------------------------------------

Choose installation method:
1) Install via this script (clone & setup automatically)
2) Already installed manually (pip install or git clone)
Enter 1 or 2: 1

🐍 Checking Python version...
✅ Python version is 3.12
🔎 Python executable: /opt/anaconda3/bin/python3

🔍 Checking if 'uv' is installed...
✅ uv is already installed.

📥 Cloning project from GitHub...
Cloning into '/Users/hailin/doris-mcp-server'...
Enter passphrase for key '/Users/hailin/.ssh/id_ed25519': 
remote: Enumerating objects: 218, done.
remote: Counting objects: 100% (218/218), done.
remote: Compressing objects: 100% (138/138), done.
remote: Total 218 (delta 102), reused 160 (delta 63), pack-reused 0 (from 0)
Receiving objects: 100% (218/218), 91.55 KiB | 189.00 KiB/s, done.
Resolving deltas: 100% (102/102), done.
🔧 Setting up local environment...
Using CPython 3.12.4 interpreter at: /opt/anaconda3/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
Using Python 3.12.4 environment at: /opt/anaconda3
Resolved 49 packages in 1.10s
      Built doris-mcp-server @ file:///Users/hailin/doris-mcp-server
Prepared 1 package in 627ms
Uninstalled 1 package in 1ms
Installed 1 package in 1ms
 - doris-mcp-server==0.0.2a2 (from file:///Users/hailin/dev/doris-mcp-server)
 + doris-mcp-server==0.0.2a3 (from file:///Users/hailin/doris-mcp-server)
📦 Installing dependencies via uv sync...
Resolved 59 packages in 853ms
Prepared 32 packages in 1.83s
Installed 52 packages in 147ms
 + annotated-types==0.7.0
 + anyio==4.9.0
 + certifi==2025.1.31
 + charset-normalizer==3.4.1
 + click==8.1.8
 + dbutils==3.1.0
 + docutils==0.21.2
 + doris-mcp-server==0.0.2a3 (from file:///Users/hailin/doris-mcp-server)
 + h11==0.16.0
 + httpcore==1.0.9
 + httpx==0.28.1
 + httpx-sse==0.4.0
 + id==1.5.0
 + idna==3.10
 + jaraco-classes==3.4.0
 + jaraco-context==6.0.1
 + jaraco-functools==4.1.0
 + keyring==25.6.0
 + markdown-it-py==3.0.0
 + mcp==1.6.0
 + mdurl==0.1.2
 + more-itertools==10.7.0
 + nh3==0.2.21
 + numpy==2.2.5
 + packaging==25.0
 + pandas==2.2.3
 + pyarrow==19.0.1
 + pydantic==2.11.3
 + pydantic-core==2.33.1
 + pydantic-settings==2.9.1
 + pygments==2.19.1
 + pymysql==1.1.1
 + python-dateutil==2.9.0.post0
 + python-dotenv==1.1.0
 + pytz==2025.2
 + readme-renderer==44.0
 + requests==2.32.3
 + requests-toolbelt==1.0.0
 + rfc3986==2.0.0
 + rich==14.0.0
 + shellingham==1.5.4
 + six==1.17.0
 + sniffio==1.3.1
 + sse-starlette==2.3.3
 + starlette==0.46.2
 + twine==6.1.0
 + typer==0.15.2
 + typing-extensions==4.13.2
 + typing-inspection==0.4.0
 + tzdata==2025.2
 + urllib3==2.4.0
 + uvicorn==0.34.2
📋 Copied .env.example to .env

Do you want to configure database connection now?
1) Yes, configure now
2) No, I will configure later in MCP client
Enter 1 or 2: 1

🔧 Please input your Doris database connection information.
DB_HOST (default: localhost): localhost
DB_PORT (default: 9030): 9030
DB_USER (default: root): root
DB_PASSWORD (default: empty): 123456
DB_NAME (e.g., your database name, required): mydb
MCP_SERVER_NAME (default: DorisAnalytics): doris_mcp
Enable DEBUG mode? (true/false, default: true): 

✅ Successfully updated .env at: /Users/hailin/doris-mcp-server/src/doris_mcp_server/config/.env

🚀 Setup complete!
You can now start the MCP server and test database connection with:
   server doris://user:pass@localhost:9030/mydb
or
   python -m doris_mcp_server.server doris://user:pass@localhost:9030/mydb
```

## **🛠️ What the Script Will Do**

  

When you run the script:

- It **automatically detects** if you are already inside a Doris-MCP-Server project.
- If not detected, it will prompt you:
    - **Option 1**: Automatically clone and install the server project via GitHub
    - **Option 2**: Use an existing installation (pip-installed or manually cloned)
- It will **set up a local virtual environment** and **install dependencies** if needed.
- It will **locate** or **prompt for** the correct config folder path containing .env.
- It will **ask you to enter** your **Doris database connection parameters** via command-line prompts. You can also choose to skip any optional parameters.
- It will **generate or update** the .env file based on your inputs.

✅ If you want to reconfigure your database connection later, simply run `bash setup.sh` again — it will safely update your .env file.

## **🔧 Database Connection Inputs**

During setup, you will be asked to provide:

|**Field**|**Description**|**Example**|
|---|---|---|
|DB_HOST|Your Doris database host address|127.0.0.1|
|DB_PORT|Doris database port|9030|
|DB_USER|Database username|root|
|DB_PASSWORD|Database password|mypassword|
|DB_NAME|Target database name|analytics_db|
|MCP_SERVER_NAME|Name of your MCP Server|DorisAnalytics|
|DEBUG|Enable debug mode (true/false)|true|


- All values are entered interactively, with sensible defaults provided where possible.

## **⚙️ After Setup**

Once setup is complete, you can start your MCP server:

```bash
server doris://user:pass@localhost:9030/mydb
```

or:
```bash
python -m doris_mcp_server.server doris://user:pass@localhost:9030/mydb
```

✅ Your MCP Server will then be available for any MCP-compatible client (e.g., Claude Desktop, Continue, Cline) to connect!

## **💬 Common Questions**

### **What if I made a mistake in the database settings?**

Simply re-run:
```bash
bash setup.sh
```

and input the correct connection details. It will **safely overwrite** the old .env file.

### **What if the script can’t find my existing installation?**

If automatic detection fails, the script will prompt you to **manually input** the full path to your `doris_mcp_server/config `folder.

Example:
```bash
/Users/yourname/.local/lib/python3.11/site-packages/doris_mcp_server/config
```

or
```bash
/your/path/to/doris-mcp-server/src/doris_mcp_server/config
```

## **📢 Important Notes**

- The .env file contains **sensitive information** (like database passwords).
    **Do not upload it** to public GitHub repositories.
- Always ensure your environment variables are correctly set before starting the server.
