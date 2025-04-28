#!/bin/bash

set -euo pipefail

# === 基本参数 ===
REPO_URL="git@github.com:NomotoK/doris-mcp-server.git"
DEFAULT_CLONE_DIR="$HOME/doris-mcp-server"
DEFAULT_CONFIG_RELATIVE_PATH="src/doris_mcp_server/config"
PIP_SITE_PACKAGES="$(python3 -c 'import site; print(site.getsitepackages()[0])')"

# === 检查是否已经在 MCP server 项目根目录 ===
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
LOCAL_CONFIG_PATH="$SCRIPT_DIR/src/doris_mcp_server/config"

if [ -d "$LOCAL_CONFIG_PATH" ]; then
    echo "✅ Detected existing MCP server project at: $SCRIPT_DIR"
    CONFIG_PATH="$LOCAL_CONFIG_PATH"
else
    # === 欢迎界面 ===
    echo "-------------------------------------------"
    echo "🚀 Welcome to Doris-MCP-Server Setup Wizard"
    echo "-------------------------------------------"
    echo ""

    echo "Choose installation method:"
    echo "1) Install via this script (clone & setup automatically)"
    echo "2) Already installed manually (pip install or git clone)"
    read -p "Enter 1 or 2: " INSTALL_OPTION

    CONFIG_PATH=""

    # === 安装或寻找路径 ===
    if [ "$INSTALL_OPTION" == "1" ]; then
        echo ""
        echo "📥 Cloning project from GitHub..."
        git clone "$REPO_URL" "$DEFAULT_CLONE_DIR"
        cd "$DEFAULT_CLONE_DIR"
        echo "🔧 Setting up local environment..."
        uv venv
        uv pip install -e .
        CONFIG_PATH="$DEFAULT_CLONE_DIR/$DEFAULT_CONFIG_RELATIVE_PATH"
    elif [ "$INSTALL_OPTION" == "2" ]; then
        echo ""
        echo "🔍 Attempting to locate existing installation..."
        if [ -d "$PIP_SITE_PACKAGES/doris_mcp_server/config" ]; then
            CONFIG_PATH="$PIP_SITE_PACKAGES/doris_mcp_server/config"
            echo "✅ Found installed package config at: $CONFIG_PATH"
        else
            echo "⚠️  Cannot automatically find installed config."
            read -p "Please manually input your config directory path (e.g., /absolute/path/to/doris_mcp_server/config): " CONFIG_PATH
        fi
    else
        echo "❌ Invalid input. Please restart the script and enter 1 or 2."
        exit 1
    fi

    # === 校验路径存在 ===
    if [ ! -d "$CONFIG_PATH" ]; then
        echo "❌ Error: The provided config directory does not exist: $CONFIG_PATH"
        exit 1
    fi
fi

# === 配置.env文件 ===
ENV_FILE="$CONFIG_PATH/.env"
ENV_EXAMPLE_FILE="$CONFIG_PATH/.env.example"

# 如果.env不存在，从.example复制
if [ ! -f "$ENV_FILE" ]; then
    if [ -f "$ENV_EXAMPLE_FILE" ]; then
        cp "$ENV_EXAMPLE_FILE" "$ENV_FILE"
        echo "📋 Copied .env.example to .env"
    else
        echo "❌ Missing both .env and .env.example. Cannot continue."
        exit 1
    fi
else
    echo "✏️ Existing .env found. Will update its contents."
fi

# === 询问数据库配置信息 ===
echo ""
echo "🔧 Please input your Doris database connection information."

read -p "DB_HOST (default: localhost): " DB_HOST
DB_HOST=${DB_HOST:-localhost}

read -p "DB_PORT (default: 9030): " DB_PORT
DB_PORT=${DB_PORT:-9030}

read -p "DB_USER (default: root): " DB_USER
DB_USER=${DB_USER:-root}

read -p "DB_PASSWORD (default: empty): " DB_PASSWORD
DB_PASSWORD=${DB_PASSWORD:-}

read -p "DB_NAME (e.g., your database name, required): " DB_NAME
if [ -z "$DB_NAME" ]; then
    echo "❌ DB_NAME cannot be empty."
    exit 1
fi

read -p "MCP_SERVER_NAME (default: DorisAnalytics): " MCP_SERVER_NAME
MCP_SERVER_NAME=${MCP_SERVER_NAME:-DorisAnalytics}

read -p "Enable DEBUG mode? (true/false, default: true): " DEBUG
DEBUG=${DEBUG:-true}

# === 写入到 .env文件 ===
cat > "$ENV_FILE" <<EOL
# 自动生成于 $(date)
# 数据库连接
DB_HOST=$DB_HOST
DB_PORT=$DB_PORT
DB_USER=$DB_USER
DB_PASSWORD=$DB_PASSWORD
DB_NAME=$DB_NAME

# MCP 服务器名称
MCP_SERVER_NAME=$MCP_SERVER_NAME

# 其他可能的配置项
DEBUG=$DEBUG
EOL

echo ""
echo "✅ Successfully updated .env at: $ENV_FILE"

echo ""
echo "🚀 Setup complete!"
echo "You can now start the MCP server with:"
echo "   server"
echo "or"
echo "   python -m doris_mcp_server.server"
echo ""