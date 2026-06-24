#!/usr/bin/env python3
"""
Hermes AI 助手 — API 配置引导工具
=================================
帮客户完成 API Key 配置，不用懂技术，跟着提示填就行。
"""
import os
import sys
import yaml
from pathlib import Path

HERMES_HOME = Path.home() / ".hermes"
CONFIG_PATH = HERMES_HOME / "config.yaml"
ENV_PATH = HERMES_HOME / ".env"

# ── 颜色输出 ─────────────────────────────────
def green(s):  return f"\033[0;32m{s}\033[0m"
def yellow(s): return f"\033[1;33m{s}\033[0m"
def cyan(s):   return f"\033[0;36m{s}\033[0m"
def red(s):    return f"\033[0;31m{s}\033[0m"
def bold(s):   return f"\033[1m{s}\033[0m"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ── 配置模板 ─────────────────────────────────
def get_config_template(deepseek_key="", dashscope_key=""):
    return {
        "model": {
            "default": "deepseek-v4-pro",
            "provider": "deepseek",
            "base_url": "https://api.deepseek.com/v1",
        },
        "auxiliary": {
            "vision": {
                "provider": "dashscope",
                "model": "qwen-vl-max",
                "api_key": dashscope_key,
                "timeout": 120,
            },
        },
        "agent": {
            "max_turns": 90,
        },
        "terminal": {
            "backend": "local",
            "timeout": 180,
        },
        "display": {
            "language": "zh",
        },
    }

# ── 步骤说明 ─────────────────────────────────
def print_header():
    clear_screen()
    print()
    print(cyan("  ╔══════════════════════════════════════╗"))
    print(cyan("  ║    Hermes AI 助手 — API 配置向导    ║"))
    print(cyan("  ╚══════════════════════════════════════╝"))
    print()
    print("  接下来会帮你配置 API Key，跟着提示操作就行。")
    print("  如果暂时没有 Key，可以跳过，以后随时重新运行本向导。")
    print()

def step_deepseek():
    """Step 1: DeepSeek API Key"""
    print(bold("━━━ 第 1 步：AI 对话 Key（DeepSeek）━━━"))
    print()
    print("  DeepSeek 是 AI 的大脑，没有它 Hermes 不会思考。")
    print()
    print(yellow("  💰 怎么买："))
    print("    1. 打开 https://platform.deepseek.com")
    print("    2. 注册账号 → 充值（10 块钱能用好久）")
    print("    3. 左侧菜单 → API Keys → 创建新 Key → 复制")
    print()
    print(yellow("  💡 价格参考："))
    print("    问一句大概 1-2 分钱，充 10 块够用几个月")
    print()
    
    key = input("  请粘贴你的 DeepSeek API Key（回车跳过）: ").strip()
    return key

def step_dashscope():
    """Step 2: DashScope API Key (vision)"""
    print()
    print(bold("━━━ 第 2 步：图片识别 Key（阿里云 DashScope）━━━"))
    print()
    print("  这个 Key 让 Hermes 能看懂图片（截图分析、文档识别等）")
    print("  不需要也可以跳过，但推荐配上。")
    print()
    print(yellow("  💰 怎么买："))
    print("    1. 打开 https://dashscope.aliyun.com")
    print("    2. 登录阿里云账号 → 右上角「API-KEY 管理」")
    print("    3. 创建新 Key → 复制")
    print()
    print(yellow("  💡 价格参考："))
    print("    通义千问 VL 模型有免费额度，日常使用基本不花钱")
    print()
    
    key = input("  请粘贴你的 DashScope API Key（回车跳过）: ").strip()
    return key

def step_tavily():
    """Step 3: TAVILY search key (optional)"""
    print()
    print(bold("━━━ 第 3 步（可选）：联网搜索 Key（Tavily）━━━"))
    print()
    print("  让 Hermes 能联网搜索最新信息。")
    print(yellow("  💰 注册地址：https://tavily.com（有免费额度）"))
    print()
    
    key = input("  请粘贴你的 Tavily API Key（回车跳过）: ").strip()
    return key

def write_config(deepseek_key, dashscope_key, tavily_key):
    """Write config.yaml and .env"""
    HERMES_HOME.mkdir(parents=True, exist_ok=True)
    
    # ── config.yaml ──
    config = get_config_template(deepseek_key, dashscope_key)
    
    # Merge with existing if any
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, 'r') as f:
            existing = yaml.safe_load(f) or {}
        existing.update(config)
        config = existing
    
    with open(CONFIG_PATH, 'w') as f:
        yaml.dump(config, f, default_flow_style=False, allow_unicode=True, sort_keys=False)
    
    # ── .env ──
    env_lines = []
    if ENV_PATH.exists():
        with open(ENV_PATH, 'r') as f:
            existing_env = f.read()
    else:
        existing_env = ""
    
    # Update/add keys
    env_vars = {
        "DEEPSEEK_API_KEY": deepseek_key,
        "DASHSCOPE_API_KEY": dashscope_key,
        "TAVILY_API_KEY": tavily_key,
    }
    
    for var, val in env_vars.items():
        if not val:
            continue
        if f"{var}=" in existing_env:
            # Replace existing
            import re
            existing_env = re.sub(f"{var}=.*", f"{var}={val}", existing_env)
        else:
            existing_env += f"\n{var}={val}"
    
    with open(ENV_PATH, 'w') as f:
        f.write(existing_env.strip() + "\n")

def show_summary(deepseek_key, dashscope_key, tavily_key):
    """Show configuration summary"""
    clear_screen()
    print()
    print(green("  ╔══════════════════════════════════════╗"))
    print(green("  ║        ✅ 配置完成！               ║"))
    print(green("  ╚══════════════════════════════════════╝"))
    print()
    print(bold("  已配置的 Key："))
    print(f"    AI 对话（DeepSeek）  : {'✓ 已配置' if deepseek_key else '✗ 未配置'}")
    print(f"    图片识别（DashScope）: {'✓ 已配置' if dashscope_key else '✗ 未配置'}")
    print(f"    联网搜索（Tavily）   : {'✓ 已配置' if tavily_key else '✗ 未配置'}")
    print()
    print(bold("  配置文件位置："))
    print(f"    {CONFIG_PATH}")
    print(f"    {ENV_PATH}")
    print()
    print(bold("  如何启动："))
    print("    终端输入: hermes")
    print("    或双击桌面「Hermes AI 助手」快捷方式")
    print()
    if not deepseek_key:
        print(yellow("  ⚠ 未配置 DeepSeek Key，Hermes 无法使用。"))
        print(yellow("    随时重新运行 setup_wizard.py 补充配置。"))
        print()

# ── 主流程 ─────────────────────────────────
def main():
    print_header()
    
    deepseek_key = step_deepseek()
    dashscope_key = step_dashscope()
    tavily_key = step_tavily()
    
    print()
    print(cyan("  正在写入配置..."))
    
    try:
        write_config(deepseek_key, dashscope_key, tavily_key)
    except Exception as e:
        print(red(f"  写入配置失败: {e}"))
        sys.exit(1)
    
    show_summary(deepseek_key, dashscope_key, tavily_key)
    
    print(green("  配置向导结束，可以开始使用 Hermes 了！"))
    print()

if __name__ == "__main__":
    main()
