"""
配置模块 - 统一管理项目所有配置
位置: 项目根目录/config.py
使用: from config import Config
"""
import os
from pathlib import Path
from dotenv import load_dotenv
from typing import Optional, Dict, Any
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载环境变量
def load_environment():
    """加载环境变量，支持多种方式"""
    env_path = Path(__file__).parent / '.env'
    
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        logger.info(f"从 {env_path} 加载环境变量")
    else:
        logger.warning(f".env 文件不存在: {env_path}")
        
        # 尝试从系统环境变量加载
        api_key = os.getenv("OPENAI_API_KEY")
        if api_key:
            logger.info("从系统环境变量加载API密钥")
        else:
            logger.error("未找到API密钥配置")

load_environment()

class Config:
    """配置类 - 所有项目配置的集中管理"""
    
    # ========== API 配置 ==========
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")
    OPENAI_BASE_URL: Optional[str] = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
    
    # ========== 应用配置 ==========
    APP_NAME: str = "AI学习助手"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "秋招冲刺 - AI学习助手"
    
    # ========== AI 模型默认配置 ==========
    DEFAULT_MODEL: str = "gpt-3.5-turbo"
    DEFAULT_TEMPERATURE: float = 0.7
    DEFAULT_MAX_TOKENS: int = 300
    
    # ========== 文件路径配置 ==========
    BASE_DIR: Path = Path(__file__).parent
    DATA_DIR: Path = BASE_DIR / "data"
    LOGS_DIR: Path = BASE_DIR / "logs"
    EXPORTS_DIR: Path = BASE_DIR / "exports"
    
    # ========== Streamlit 配置 ==========
    STREAMLIT_THEME: Dict[str, Any] = {
        "primaryColor": "#FF4B4B",
        "backgroundColor": "#FFFFFF",
        "secondaryBackgroundColor": "#F0F2F6",
        "textColor": "#262730",
        "font": "sans serif"
    }
    
    # ========== 功能开关 ==========
    ENABLE_EXPORT: bool = True
    ENABLE_HISTORY: bool = True
    ENABLE_CONFIG_UI: bool = True
    
    @classmethod
    def validate_config(cls) -> Dict[str, bool]:
        """
        验证配置完整性
        
        Returns:
            配置验证结果字典
        """
        results = {
            "api_key": bool(cls.OPENAI_API_KEY),
            "base_url": bool(cls.OPENAI_BASE_URL),
            "data_dir": cls.DATA_DIR.exists(),
            "logs_dir": cls.LOGS_DIR.exists(),
        }
        
        # 自动创建必要的目录
        for dir_path in [cls.DATA_DIR, cls.LOGS_DIR, cls.EXPORTS_DIR]:
            dir_path.mkdir(exist_ok=True)
            
        return results
    
    @classmethod
    def get_api_info(cls, mask: bool = True) -> Dict[str, Optional[str]]:
        """
        获取API信息（可选脱敏）
        
        Args:
            mask: 是否脱敏显示密钥
            
        Returns:
            API信息字典
        """
        api_key = cls.OPENAI_API_KEY
        
        if mask and api_key and len(api_key) > 12:
            masked_key = f"{api_key[:8]}...{api_key[-4:]}"
        else:
            masked_key = api_key
            
        return {
            "api_key": masked_key,
            "base_url": cls.OPENAI_BASE_URL,
            "model": cls.DEFAULT_MODEL,
            "temperature": cls.DEFAULT_TEMPERATURE,
            "max_tokens": cls.DEFAULT_MAX_TOKENS
        }
    
    @classmethod
    def get_app_info(cls) -> Dict[str, Any]:
        """获取应用信息"""
        return {
            "name": cls.APP_NAME,
            "version": cls.VERSION,
            "description": cls.DESCRIPTION,
            "base_dir": str(cls.BASE_DIR),
            "features": {
                "export": cls.ENABLE_EXPORT,
                "history": cls.ENABLE_HISTORY,
                "config_ui": cls.ENABLE_CONFIG_UI
            }
        }
    
    @classmethod
    def print_summary(cls):
        """打印配置摘要"""
        print("=" * 50)
        print(f"{cls.APP_NAME} v{cls.VERSION} - 配置摘要")
        print("=" * 50)
        
        # API信息
        api_info = cls.get_api_info()
        print(f"🔑 API密钥: {api_info['api_key']}")
        print(f"🌐 接口地址: {api_info['base_url']}")
        print(f"🤖 默认模型: {api_info['model']}")
        
        # 验证配置
        validation = cls.validate_config()
        print("\n✅ 配置验证:")
        for key, value in validation.items():
            status = "通过" if value else "失败"
            print(f"  {key}: {status}")
        
        print("=" * 50)

# 自动验证配置
if __name__ == "__main__":
    Config.print_summary()