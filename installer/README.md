# Hermes AI 助手 — 一键安装包

不用懂代码，跟着走三步，5 分钟装好你自己的 AI 助手。

---

## 第一步：打开你电脑对应的文件夹

| 你的电脑 | 打开这个文件夹 | 双击这个文件 |
|----------|---------------|-------------|
| Windows 10 / 11 | `Windows` | `install.bat` |
| Mac（苹果电脑） | `Mac` | `install.sh` |
| Linux（Ubuntu 等） | `Linux` | `install.sh` |

> Mac / Linux 如果双击不行：右键 → 在终端中打开

---

## 第二步：跟着提示填 Key

安装完之后会自动弹出一个配置工具，让你填 API Key。

**必须有的：DeepSeek API Key（AI 大脑）**

> 去哪买：https://platform.deepseek.com  
> 注册 → 充值 10 块钱 → 左边菜单「API Keys」→ 创建 → 复制  
> 价格：问一句话大概 1-2 分钱，10 块能用好几个月

**建议有：阿里云 DashScope Key（图片识别）**

> 去哪搞：https://dashscope.aliyun.com  
> 登录阿里云 → 右上角「API-KEY 管理」→ 创建 → 复制  
> 有免费额度，日常用基本不花钱

如果暂时不想配，直接回车跳过，以后随时重新运行 `setup_wizard.py`。

---

## 第三步：开始用

- **Windows**：双击桌面「Hermes AI 助手」
- **Mac / Linux**：打开终端，输入 `hermes`

---

## 常见问题

**Q：Python 没装怎么办？**  
A：Windows 版会自动引导你去 Microsoft Store 安装。Mac/Linux 版会自动装。

**Q：为什么我的 DeepSeek Key 用不了？**  
A：检查两件事：① 账户里有没有余额（至少充 1 块）；② Key 有没有复制完整（sk- 开头）。

**Q：能换别的 AI 吗？**  
A：能。终端输入 `hermes model` 可以切换模型和供应商。

**Q：怎么卸载？**  
A：终端输入 `hermes uninstall`

---

## 需要帮助？

把报错信息截图发给我，我帮你看。
