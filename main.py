import base64
from mcp.server.fastmcp import FastMCP
import pyautogui
import os
from datetime import datetime

mcp = FastMCP(name="computer-control-mcp-server", instructions="This is a tool for controlling the computer.")

@mcp.tool()
def click(x: int, y: int):
    """点击鼠标左键"""
    pyautogui.click(x, y)

@mcp.tool()
def right_click(x: int, y: int):
    """点击鼠标右键
    
    参数:
        x: X坐标
        y: Y坐标
    
    示例:
        right_click(100, 200)  # 在坐标(100, 200)点击右键
    """
    pyautogui.rightClick(x, y)
    
    return {
        "message": f"在坐标({x}, {y})点击了鼠标右键",
        "position": (x, y),
        "button": "right"
    }

@mcp.tool()
def double_click(x: int, y: int):
    """双击鼠标左键
    
    参数:
        x: X坐标
        y: Y坐标
    
    示例:
        double_click(100, 200)  # 在坐标(100, 200)双击左键
    """
    pyautogui.doubleClick(x, y)
    
    return {
        "message": f"在坐标({x}, {y})双击了鼠标左键",
        "position": (x, y),
        "button": "left",
        "clicks": 2
    }

@mcp.tool()
def type(text: str):
    """输入一段文本"""
    pyautogui.typewrite(text)

@mcp.tool()
def press(key: str):
    """按下单个按键，支持空格,回车,shift,ctrl,alt,tab等
    
    参数:
        key: 按键，如 'space', 'enter', 'shift', 'ctrl', 'alt', 'tab'
    
    示例:
        press('space')  # 按下空格键
        press('enter')  # 按下回车键
        press('shift')  # 按下shift键
        press('ctrl')  # 按下ctrl键
        press('alt')  # 按下alt键
        press('tab')  # 按下tab键
    """
    pyautogui.press(key)
    
    return {
        "message": f"按下了按键: {key}",
        "key": key
    }

@mcp.tool()
def hotkey(keys: list[str]):
    """组合键，支持多个按键同时按下
    
    参数:
        keys: 按键列表，如 ['ctrl', 'c'] 或 ['command', 's']
    
    示例:
        hotkey(['ctrl', 'c'])      # 复制
        hotkey(['command', 's'])       # 保存 (Mac)
        hotkey(['ctrl', 'shift', 'esc'])  # 任务管理器 (Windows)
    """
    pyautogui.hotkey(*keys)
    
    return {
        "message": f"按下了组合键: {keys}",
        "keys": keys
    }

@mcp.tool()
def key_down(key: str):
    """按下按键但不释放"""
    pyautogui.keyDown(key)
    
    return {
        "message": f"按下了按键: {key}",
        "key": key
    }

@mcp.tool()
def key_up(key: str):
    """释放之前按下的按键"""
    pyautogui.keyUp(key)
    
    return {
        "message": f"释放了按键: {key}",
        "key": key
    }

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
def scroll(clicks: int, x: int = None, y: int = None):
    """滚动鼠标滚轮
    
    参数:
        clicks: 滚动次数，正数向上滚动，负数向下滚动
        x: 可选的X坐标，如果不指定则使用当前鼠标位置
        y: 可选的Y坐标，如果不指定则使用当前鼠标位置
    
    示例:
        scroll(3)           # 在当前鼠标位置向上滚动3次
        scroll(-2)          # 在当前鼠标位置向下滚动2次
        scroll(1, 100, 200) # 在坐标(100, 200)向上滚动1次
    """
    if x is not None and y is not None:
        # 移动到指定坐标再滚动
        pyautogui.moveTo(x, y)
    
    pyautogui.scroll(clicks)
    
    return {
        "message": f"在位置({pyautogui.position()[0]}, {pyautogui.position()[1]})滚动了{clicks}次",
        "clicks": clicks,
        "position": pyautogui.position()
    }

@mcp.tool()
def scroll_horizontal(clicks: int, x: int = None, y: int = None):
    """水平滚动鼠标滚轮（适用于支持水平滚动的设备）
    
    参数:
        clicks: 滚动次数，正数向右滚动，负数向左滚动
        x: 可选的X坐标，如果不指定则使用当前鼠标位置
        y: 可选的Y坐标，如果不指定则使用当前鼠标位置
    
    示例:
        scroll_horizontal(2)        # 在当前鼠标位置向右滚动2次
        scroll_horizontal(-1)       # 在当前鼠标位置向左滚动1次
        scroll_horizontal(3, 150, 250) # 在坐标(150, 250)向右滚动3次
    """
    if x is not None and y is not None:
        # 移动到指定坐标再滚动
        pyautogui.moveTo(x, y)
    
    pyautogui.hscroll(clicks)
    
    return {
        "message": f"在位置({pyautogui.position()[0]}, {pyautogui.position()[1]})水平滚动{clicks}次",
        "clicks": clicks,
        "position": pyautogui.position()
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