"""
导出工具模块
"""
from datetime import datetime
from typing import List, Dict
import os

def export_to_markdown(messages: List[Dict[str, str]], filename: str = None) -> str:
    """
    将对话导出为Markdown格式
    
    Args:
        messages: 对话历史
        filename: 文件名，None则自动生成
        
    Returns:
        文件路径
    """
    if filename is None:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"对话记录_{timestamp}.md"
    
    # 确保exports目录存在
    exports_dir = "exports"
    os.makedirs(exports_dir, exist_ok=True)
    
    filepath = os.path.join(exports_dir, filename)
    
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("# AI学习助手对话记录\n\n")
        f.write(f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write("---\n\n")
        
        for msg in messages:
            role_icon = "👤" if msg["role"] == "user" else "🤖"
            role_text = "用户" if msg["role"] == "user" else "AI助手"
            
            f.write(f"## {role_icon} {role_text}\n\n")
            f.write(f"{msg['content']}\n\n")
            f.write("---\n\n")
    
    return filepath