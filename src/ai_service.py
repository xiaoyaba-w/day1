"""
AI服务模块 - 封装OpenAI API调用
"""
import openai
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class AIService:
    """AI服务类"""
    
    def __init__(self, api_key: str, base_url: Optional[str] = None):
        """
        初始化AI服务
        
        Args:
            api_key: API密钥
            base_url: API地址，None表示使用OpenAI官方
        """
        self.client = openai.OpenAI(
            api_key=api_key,
            base_url=base_url
        )
        logger.info(f"AI服务初始化完成，使用地址: {base_url or 'OpenAI官方'}")
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "gpt-3.5-turbo",
        temperature: float = 0.7,
        max_tokens: int = 300
    ) -> str:
        """
        调用AI对话接口
        
        Args:
            messages: 对话历史
            model: 模型名称
            temperature: 随机性
            max_tokens: 最大token数
            
        Returns:
            AI回复内容
        """
        try:
            response = self.client.chat.completions.create(
                model=model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            
            return response.choices[0].message.content
            
        except openai.AuthenticationError as e:
            logger.error(f"认证失败: {e}")
            raise Exception(f"API认证失败: {str(e)}")
            
        except openai.APIConnectionError as e:
            logger.error(f"连接失败: {e}")
            raise Exception(f"网络连接失败: {str(e)}")
            
        except openai.RateLimitError as e:
            logger.error(f"频率限制: {e}")
            raise Exception(f"请求频率超限: {str(e)}")
            
        except Exception as e:
            logger.error(f"API调用失败: {e}")
            raise Exception(f"AI服务错误: {str(e)}")
    
    def quick_test(self) -> bool:
        """快速连接测试"""
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": "说'连接成功'"}],
                max_tokens=5
            )
            return bool(response.choices[0].message.content)
        except Exception as e:
            logger.error(f"连接测试失败: {e}")
            return False