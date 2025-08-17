# PyAutoGUI MCP Server

一个基于Model Context Protocol (MCP)的自动化控制服务器，使用PyAutoGUI实现屏幕截图、鼠标控制、键盘输入等功能。

## 🚀 功能特性

### 基础控制功能
- **鼠标控制**: 点击指定坐标、获取鼠标位置
- **键盘输入**: 输入文本、按键、组合键支持
- **屏幕截图**: 截图保存到指定目录、返回图像数据

### 系统信息
- **系统检测**: 自动识别操作系统类型（macOS/Windows/Linux）
- **环境信息**: 获取系统架构、Python环境、显示信息等
- **跨平台支持**: 针对不同系统提供相应的操作适配

### 高级功能
- **组合键支持**: 支持复杂的键盘组合操作
- **智能路径**: 自动创建截图保存目录，按时间组织
- **错误处理**: 完善的异常处理和错误提示

## 📋 系统要求

- Python 3.8+
- macOS / Windows / Linux
- 支持MCP协议的客户端

## 🛠️ 安装方法

### 1. 克隆项目
```bash
git clone <your-repo-url>
cd pyautogui-mcp-server
```

### 2. 创建虚拟环境
```bash
python -m venv venv
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate     # Windows
```

### 3. 安装依赖
```bash
pip install -r requirements.txt
```

## 🚀 使用方法

### 启动服务器
```bash
python main.py
```

### 连接MCP客户端
使用支持MCP协议的客户端连接，如Cursor、Claude Desktop等。

## 🛠️ 可用工具

### 屏幕截图
```python
# 截图并保存到文件
screenshot_save() -> dict

# 截图并返回图像数据
screenshot_image_data() -> dict
```

### 鼠标控制
```python
# 点击指定坐标
click(x: int, y: int)

# 获取鼠标位置
get_mouse_position() -> dict
```

### 键盘控制
```python
# 输入文本
type(text: str)

# 按键
press(key: str)

# 组合键
hotkey(keys: list[str])

# 按键按下（不释放）
key_down(key: str)

# 按键释放
key_up(key: str)
```

### 系统信息
```python
# 获取基本系统信息
get_base_system_info() -> dict

# 获取截图目录
screenshot_dir() -> str
```

## 📁 项目结构

```
pyautogui-mcp-server/
├── main.py              # 主服务器文件
├── requirements.txt     # Python依赖
├── README.md           # 项目说明
├── .python-version     # Python版本
└── venv/               # 虚拟环境
```

## 🔧 配置说明

### 截图保存路径
截图默认保存到：`~/Desktop/one piece/当前时间/`
- 按小时自动创建目录
- 文件名包含时间戳，避免重复

### 系统适配
- **macOS**: 使用`system_profiler`获取详细系统信息
- **Windows**: 使用`ver`命令获取系统版本
- **Linux**: 读取`/etc/os-release`获取发行版信息

## 📝 使用示例

### 基础操作
```python
# 截图并保存
result = screenshot_save()
print(f"截图已保存到: {result['saved_path']}")

# 获取鼠标位置
pos = get_mouse_position()
print(f"鼠标位置: {pos['message']}")

# 点击坐标
click(100, 200)

# 输入文本
type("Hello, World!")

# 组合键
hotkey(['cmd', 's'])  # 保存文件
```

### 系统检测
```python
# 获取系统信息
info = get_base_system_info()
print(f"操作系统: {info['system']['os_name']}")
print(f"屏幕分辨率: {info['display']['resolution']}")
```

## ⚠️ 注意事项

1. **权限要求**: 某些操作可能需要系统权限
2. **安全考虑**: 自动化操作可能影响系统安全，请谨慎使用
3. **跨平台**: 不同系统的快捷键可能不同
4. **性能**: 截图操作可能消耗较多资源

## 🐛 故障排除

### 常见问题

1. **导入错误**: 确保已安装所有依赖包
2. **权限错误**: 检查系统权限设置
3. **路径错误**: 确认截图保存路径存在且有写入权限

### 调试方法
```python
# 获取详细系统信息
info = get_base_system_info()
print(json.dumps(info, indent=2, ensure_ascii=False))
```

## 🤝 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 📄 许可证

[添加您的许可证信息]

## 📞 联系方式

[添加您的联系方式]
