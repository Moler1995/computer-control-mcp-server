import base64
from mcp.server.fastmcp import FastMCP
import pyautogui
import os
from datetime import datetime

mcp = FastMCP(name="computer-control-mcp-server", instructions="This is a tool for controlling the computer.")

@mcp.tool()
def screenshot_save() -> dict:
    """截取屏幕截图并保存到指定目录，返回保存路径"""
    # 截取屏幕截图
    screenshot = pyautogui.screenshot()
    
    # 获取当前时间（到小时）
    current_time = datetime.now()
    time_str = current_time.strftime("%Y-%m-%d_%H")
    
    # 构建保存路径：桌面/one piece/当前时间
    desktop_path = os.path.expanduser("~/Desktop")
    save_dir = os.path.join(desktop_path, "one piece", time_str)
    
    # 创建目录（如果不存在）
    os.makedirs(save_dir, exist_ok=True)
    
    # 生成文件名（包含分钟和秒）
    filename = f"screenshot_{current_time.strftime('%Y%m%d_%H%M%S')}.png"
    file_path = os.path.join(save_dir, filename)
    
    # 保存图像到文件
    screenshot.save(file_path, format='PNG')
    
    return {
        "saved_path": file_path,
        "saved_directory": save_dir,
        "filename": filename,
        "size": screenshot.size,
        "message": f"截图已保存到 {file_path}"
    }

@mcp.tool()
def click(x: int, y: int):
    """点击鼠标左键"""
    pyautogui.click(x, y)

@mcp.tool()
def type(text: str):
    """输入一段文本"""
    pyautogui.typewrite(text)

@mcp.tool()
def press(key: str):
    """按下单个按键"""
    pyautogui.press(key)

@mcp.tool()
def hotkey(keys: list[str]):
    """组合键，支持多个按键同时按下
    
    参数:
        keys: 按键列表，如 ['ctrl', 'c'] 或 ['cmd', 's']
    
    示例:
        hotkey(['ctrl', 'c'])      # 复制
        hotkey(['command', 's'])       # 保存 (Mac)
        hotkey(['ctrl', 'shift', 'esc'])  # 任务管理器 (Windows)
    """
    pyautogui.hotkey(*keys)

@mcp.tool()
def key_down(key: str):
    """按下按键但不释放"""
    pyautogui.keyDown(key)

@mcp.tool()
def key_up(key: str):
    """释放之前按下的按键"""
    pyautogui.keyUp(key)

@mcp.tool()
def screenshot_image_data() -> dict:
    """截取屏幕截图并返回base64编码的图像数据"""
    # 截取屏幕截图
    screenshot = pyautogui.screenshot()
    
    # 将PIL Image转换为PNG格式的字节数据
    from io import BytesIO
    buffer = BytesIO()
    screenshot.save(buffer, format='PNG')
    buffer.seek(0)
    
    # 获取PNG图像数据并转换为base64
    image_bytes = buffer.getvalue()
    base64_string = base64.b64encode(image_bytes).decode()
    
    return {
        "mime_type": "image/png",
        "image_data": base64_string
    }

@mcp.tool()
def get_mouse_position() -> dict:
    """只获取当前鼠标位置坐标"""
    x, y = pyautogui.position()
    
    return {
        "message": f"当前鼠标位置: ({x}, {y})"
    }

@mcp.tool()
def get_base_system_info() -> dict:
    """获取基本系统信息，用于大模型判断系统类型和进行相应操作"""
    import platform
    import subprocess
    import json
    
    # 获取操作系统信息
    os_name = platform.system()
    os_version = platform.version()
    os_release = platform.release()

    # 获取系统架构
    machine = platform.machine()
    processor = platform.processor()
    
    
    # 获取屏幕尺寸
    screen_width, screen_height = pyautogui.size()
    
    # 获取系统特定信息
    system_specific = {}
    
    if os_name == "Darwin":  # macOS
        try:
            # 获取Mac系统版本
            result = subprocess.run(['sw_vers', '-productVersion'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                system_specific["macos_version"] = result.stdout.strip()
            
            # 获取Mac显示器信息
            result = subprocess.run(['system_profiler', 'SPDisplaysDataType', '-json'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                display_data = json.loads(result.stdout)
                displays = display_data.get('SPDisplaysDataType', [])
                
                display_info = []
                for display in displays:
                    if 'spdisplays_ndrvs' in display:
                        for driver in display['spdisplays_ndrvs']:
                            if 'spdisplays_vendor' in driver:
                                display_info.append({
                                    "vendor": driver.get('spdisplays_vendor', 'Unknown'),
                                    "model": driver.get('spdisplays_model', 'Unknown'),
                                    "resolution": driver.get('_spdisplays_resolution', 'Unknown')
                                })
                system_specific["displays"] = display_info
        except Exception as e:
            system_specific["error"] = f"获取Mac信息失败: {str(e)}"
            
    elif os_name == "Windows":
        try:
            # 获取Windows版本信息
            result = subprocess.run(['ver'], capture_output=True, text=True, shell=True)
            if result.returncode == 0:
                system_specific["windows_version"] = result.stdout.strip()
        except Exception as e:
            system_specific["error"] = f"获取Windows信息失败: {str(e)}"
            
    elif os_name == "Linux":
        try:
            # 获取Linux发行版信息
            result = subprocess.run(['cat', '/etc/os-release'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                system_specific["linux_distro"] = result.stdout.strip()
        except Exception as e:
            system_specific["error"] = f"获取Linux信息失败: {str(e)}"
    
    return {
        "system": {
            "os_name": os_name,
            "os_version": os_version,
            "os_release": os_release,
            "machine": machine,
            "processor": processor
        },
        "display": {
            "screen_size": {
                "width": screen_width,
                "height": screen_height,
                "total_pixels": screen_width * screen_height
            },
            "resolution": f"{screen_width}x{screen_height}",
        },
        "system_specific": system_specific,
        "message": f"系统信息: {os_name} {os_release} ({machine}), 屏幕: {screen_width}x{screen_height}"
    }

if __name__ == "__main__":
    mcp.run(transport="streamable-http")