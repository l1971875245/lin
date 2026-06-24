#!/usr/bin/env bash
# ============================================================
#  Hermes AI 助手 — Linux / macOS 一键安装脚本
#  适配：Ubuntu / Debian / CentOS / macOS 10.15+
# ============================================================
set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

echo -e "${CYAN}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║     Hermes AI 助手 — 一键安装       ║"
echo "  ║     支持 Linux / macOS              ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${NC}"

# ── 1. 检测系统 ──────────────────────────────
OS="$(uname -s)"
case "$OS" in
    Linux)  PLATFORM="linux" ;;
    Darwin) PLATFORM="macos" ;;
    *)
        echo -e "${RED}❌ 不支持的操作系统: $OS${NC}"
        echo "Hermes 支持 Linux 和 macOS，Windows 请使用 install.bat"
        exit 1
        ;;
esac
echo -e "${GREEN}✓ 检测到系统: $OS${NC}"

# ── 2. 检测 Python ───────────────────────────
PYTHON=""
for cmd in python3 python; do
    if command -v "$cmd" &>/dev/null; then
        ver=$("$cmd" --version 2>&1 | grep -oP '\d+\.\d+' | head -1)
        if [ "$(echo "$ver >= 3.10" | bc 2>/dev/null || echo 0)" = "1" ] || [ "${ver%%.*}" -ge 3 ] && [ "${ver#*.}" -ge 10 ] 2>/dev/null; then
            PYTHON="$cmd"
            break
        fi
    fi
done

if [ -z "$PYTHON" ]; then
    echo -e "${YELLOW}⚠ 未检测到 Python 3.10+，正在安装...${NC}"
    case "$PLATFORM" in
        linux)
            if command -v apt-get &>/dev/null; then
                sudo apt-get update && sudo apt-get install -y python3 python3-pip python3-venv python3-dev build-essential
            elif command -v yum &>/dev/null; then
                sudo yum install -y python3 python3-pip python3-devel gcc
            else
                echo -e "${RED}❌ 无法自动安装 Python，请手动安装 Python 3.10+${NC}"
                exit 1
            fi
            PYTHON="python3"
            ;;
        macos)
            if command -v brew &>/dev/null; then
                brew install python@3.12
            else
                echo -e "${RED}❌ 请先安装 Homebrew (https://brew.sh) 或手动安装 Python 3.10+${NC}"
                exit 1
            fi
            PYTHON="python3"
            ;;
    esac
fi
echo -e "${GREEN}✓ Python: $($PYTHON --version)${NC}"

# ── 3. 配置 pip 镜像（国内加速）──────────────
echo -e "\n${CYAN}🚀 检查网络环境...${NC}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$PYTHON" "$SCRIPT_DIR/pip_mirror.py"

# ── 4. 安装 Hermes ───────────────────────────
echo -e "\n${CYAN}📦 正在安装 Hermes AI 助手...${NC}"
if [ -f "hermes_install.sh" ]; then
    # 离线模式：使用本地缓存的安装脚本
    bash hermes_install.sh
else
    curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
fi
echo -e "${GREEN}✓ Hermes 安装完成${NC}"

# 确保 hermes 在 PATH 中
export PATH="$HOME/.local/bin:$PATH"

# ── 5. 运行配置向导 ──────────────────────────
echo -e "\n${CYAN}⚙ 正在启动配置向导...${NC}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
"$PYTHON" "$SCRIPT_DIR/setup_wizard.py"

echo -e "\n${GREEN}"
echo "  ╔══════════════════════════════════════╗"
echo "  ║   ✅ 安装完成！                     ║"
echo "  ║   在终端输入 hermes 启动            ║"
echo "  ╚══════════════════════════════════════╝"
echo -e "${NC}"
