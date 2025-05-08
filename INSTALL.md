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

Do you need to install uv? (y/n): 
Install uv? y
📦 Installing uv...
✅ uv installation complete.

📥 Cloning project from GitHub...
Cloning into '/Users/hailin/doris-mcp-server'...
Enter passphrase for key '/Users/hailin/.ssh/id_ed25519': 
remote: Enumerating objects: 77, done.
remote: Counting objects: 100% (77/77), done.
remote: Compressing objects: 100% (57/57), done.
remote: Total 77 (delta 21), reused 60 (delta 13), pack-reused 0 (from 0)
Receiving objects: 100% (77/77), 40.71 KiB | 173.00 KiB/s, done.
Resolving deltas: 100% (21/21), done.
🔧 Setting up local environment...
Using CPython 3.12.4 interpreter at: /opt/anaconda3/bin/python3.12
Creating virtual environment at: .venv
Activate with: source .venv/bin/activate
Using Python 3.12.4 environment at: /opt/anaconda3
Resolved 34 packages in 1.45s
      Built doris-mcp-server @ file:///Users/hailin/doris-mcp-server
Prepared 1 package in 602ms
Uninstalled 1 package in 1ms
Installed 1 package in 1ms
 ~ doris-mcp-server==0.0.1 (from file:///Users/hailin/doris-mcp-server)
📋 Copied .env.example to .env

Do you want to configure database connection now?
1) Yes, configure now
2) No, I will configure later in MCP client
Enter 1 or 2: 1

🔧 Please input your Doris database connection information.
DB_HOST (default: localhost): 127.0.0.1
DB_PORT (default: 9030): 9030
DB_USER (default: root): datacenter
DB_PASSWORD (default: empty): 1234567890
DB_NAME (e.g., your database name, required): my_db
MCP_SERVER_NAME (default: DorisAnalytics): 
Enable DEBUG mode? (true/false, default: true): true

✅ Successfully updated .env at: /Users/hailin/doris-mcp-server/src/doris_mcp_server/config/.env

🚀 Setup complete!
You can now start the MCP server with:
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
server
```

or:
```bash
python -m doris_mcp_server.server
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
