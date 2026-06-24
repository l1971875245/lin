@echo off
chcp 65001 >nul
title Hermes AI 助手 — 一键安装 (Windows)

echo.
echo   ╔══════════════════════════════════════╗
echo   ║     Hermes AI 助手 — 一键安装       ║
echo   ║     Windows 10 / 11                ║
echo   ╚══════════════════════════════════════╝
echo.

:: ── 1. 检测 Python ──────────────────────────
where python >nul 2>nul
if %errorlevel% neq 0 (
    where python3 >nul 2>nul
    if %errorlevel% neq 0 (
        echo [警告] 未检测到 Python
        echo.
        echo Hermes 需要 Python 3.10 或更高版本。
        echo.
        echo 请选择安装方式：
        echo   [1] 从 Microsoft Store 安装（推荐，自动完成）
        echo   [2] 从 python.org 下载安装
        echo   [3] 我已安装 Python，手动指定路径
        echo.
        set /p choice="请输入选项 (1/2/3): "
        
        if "!choice!"=="1" (
            echo 正在打开 Microsoft Store...
            start ms-windows-store://pdp/?productid=9NRWMJP3717K
            echo.
            echo 请在 Store 中点击"安装"，完成后按任意键继续...
            pause >nul
        ) else if "!choice!"=="2" (
            echo 正在打开下载页面...
            start https://www.python.org/downloads/
            echo.
            echo 请下载 Python 3.10+，安装时务必勾选 "Add Python to PATH"
            echo 安装完成后按任意键继续...
            pause >nul
        ) else if "!choice!"=="3" (
            set /p python_path="请输入 python.exe 的完整路径: "
            set PYTHON=!python_path!
            goto :check_python_version
        )
    )
)

:: 找到 Python
set PYTHON=python
where python >nul 2>nul || set PYTHON=python3

:check_python_version
%PYTHON% --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 无法运行 Python，请检查安装
    pause
    exit /b 1
)

echo [✓] Python: 
%PYTHON% --version

:: ── 2. 检查 pip ─────────────────────────────
%PYTHON% -m pip --version >nul 2>nul
if %errorlevel% neq 0 (
    echo [警告] pip 未安装，正在安装...
    %PYTHON% -m ensurepip --upgrade
)

:: ── 3. 配置 pip 镜像（国内加速）─────────────
echo [加速] 检查网络环境...
%PYTHON% "%~dp0pip_mirror.py"

:: ── 4. 安装 Hermes ──────────────────────────
echo.
echo [安装] 正在安装 Hermes AI 助手...
if exist "hermes_install.ps1" (
    powershell -ExecutionPolicy Bypass -File hermes_install.ps1
) else (
    %PYTHON% -m pip install hermes-agent --upgrade
)

if %errorlevel% neq 0 (
    echo [错误] Hermes 安装失败，请检查网络连接
    pause
    exit /b 1
)
echo [✓] Hermes 安装完成

:: ── 5. 配置向导 ─────────────────────────────
echo.
echo [配置] 正在启动配置向导...
%PYTHON% "%~dp0setup_wizard.py"
if %errorlevel% neq 0 (
    echo [警告] 配置向导未完成，你可以稍后手动运行 setup_wizard.py
)

:: ── 6. 创建桌面快捷方式 ──────────────────────
echo.
echo [快捷方式] 正在创建桌面快捷方式...

set "desktop=%USERPROFILE%\Desktop"
set "shortcut=%desktop%\Hermes AI 助手.lnk"

:: 创建启动批处理
set "launcher=%USERPROFILE%\.hermes\hermes_launcher.bat"
(
echo @echo off
echo cd /d "%USERPROFILE%"
echo hermes
echo pause
) > "%launcher%"

powershell -Command ^
"$WshShell = New-Object -ComObject WScript.Shell; ^
$Shortcut = $WshShell.CreateShortcut('%shortcut%'); ^
$Shortcut.TargetPath = '%launcher%'; ^
$Shortcut.WorkingDirectory = '%USERPROFILE%'; ^
$Shortcut.Description = 'Hermes AI 助手'; ^
$Shortcut.Save()"

echo [✓] 桌面快捷方式已创建

:: ── 完成 ────────────────────────────────────
echo.
echo   ╔══════════════════════════════════════╗
echo   ║   ✅ 安装完成！                     ║
echo   ║   双击桌面"Hermes AI 助手"启动      ║
echo   ║   或在终端输入 hermes 启动          ║
echo   ╚══════════════════════════════════════╝
echo.

pause
