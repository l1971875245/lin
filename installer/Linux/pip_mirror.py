#!/usr/bin/env python3
"""
下载加速器 — 国内用户配置 pip 清华镜像
在 install 前自动检测是否需要配置代理
"""
import os
import subprocess
import sys
from pathlib import Path

PIP_CONF_DIR = Path.home() / ".pip"
PIP_CONF = PIP_CONF_DIR / "pip.conf" if os.name != 'nt' else Path.home() / "pip" / "pip.ini"

def is_china():
    """简单判断是否在中国境内（通过时区/语言环境）"""
    try:
        import locale
        lang = locale.getdefaultlocale()[0] or ""
        if "zh_CN" in lang:
            return True
    except:
        pass
    # 检查时区
    try:
        result = subprocess.run(["date", "+%Z"], capture_output=True, text=True, timeout=3)
        if "CST" in result.stdout:
            return True
    except:
        pass
    return False

def configure_pip_mirror():
    """配置 pip 清华镜像源"""
    if os.name == 'nt':
        pip_conf_dir = Path.home() / "pip"
        pip_conf_dir.mkdir(parents=True, exist_ok=True)
        conf_path = pip_conf_dir / "pip.ini"
    else:
        pip_conf_dir = Path.home() / ".pip"
        pip_conf_dir.mkdir(parents=True, exist_ok=True)
        conf_path = pip_conf_dir / "pip.conf"
    
    if conf_path.exists():
        print("  pip 镜像已配置，跳过")
        return
    
    mirror_url = "https://pypi.tuna.tsinghua.edu.cn/simple"
    conf_content = f"""[global]
index-url = {mirror_url}
trusted-host = pypi.tuna.tsinghua.edu.cn
"""
    
    conf_path.write_text(conf_content)
    print(f"  ✓ pip 镜像已切换到清华源（下载速度快 10 倍）")

if __name__ == "__main__":
    if is_china():
        print("  检测到国内网络，配置 pip 镜像加速...")
        configure_pip_mirror()
    else:
        print("  跳过镜像配置（非国内环境）")
