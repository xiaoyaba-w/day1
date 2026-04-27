"""
AI学习助手 - 第一天：基础对话功能
支持OpenAI官方接口和国内兼容接口（如智增增）
运行命令: python main.py
"""
import openai
import os
from pathlib import Path
from dotenv import load_dotenv

# 1. 加载环境变量
env_path = Path(__file__).parent.parent / '.env'  # 从src目录向上两级
load_dotenv(dotenv_path=env_path)

# 2. 配置OpenAI客户端
api_key = os.getenv("OPENAI_API_KEY")
base_url = os.getenv("OPENAI_BASE_URL")  # 可选，用于国内兼容接口

# 配置OpenAI客户端
client = openai.OpenAI(
    api_key=api_key,
    base_url=base_url if base_url else None  # 如果base_url存在则使用，否则用默认
)

def simple_chat():
    """简单的命令行对话"""
    print("🤖 AI学习助手已启动！(输入 'quit' 退出)")
    print("-" * 40)
    
    messages = [
        {"role": "system", "content": "你是一个编程学习助手，专门帮助大学生准备秋招面试。回答要简洁实用。"}
    ]
    
    while True:
        # 获取用户输入
        user_input = input("\n💬 你的问题: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'q']:
            print("👋 再见！")
            break
            
        if not user_input:
            print("⚠️  请输入问题...")
            continue
        
        # 添加到消息历史
        messages.append({"role": "user", "content": user_input})
        
        try:
            print("⏳ AI思考中...", end="", flush=True)
            
            # 调用OpenAI API
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",  # 使用便宜的模型测试
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )
            
            # 获取AI回复
            ai_reply = response.choices[0].message.content
            
            print("\r" + " " * 20 + "\r", end="")  # 清除"思考中"
            print(f"🤖 助手: {ai_reply}")
            
            # 保存AI回复到历史
            messages.append({"role": "assistant", "content": ai_reply})
            
        except openai.AuthenticationError as e:
            print(f"\n❌ 认证失败: {e}")
            print("💡 检查: 1. API密钥是否正确 2. API密钥是否已启用")
        except openai.APIConnectionError as e:
            print(f"\n❌ 网络连接失败: {e}")
            print("💡 检查: 1. 网络连接 2. 代理设置")
        except openai.RateLimitError as e:
            print(f"\n❌ 请求频率超限: {e}")
            print("💡 检查: 1. API余额 2. 请求频率")
        except openai.APIError as e:
            print(f"\n❌ API错误: {e}")
        except Exception as e:
            print(f"\n❌ 未知错误: {e}")

def test_api():
    """快速API测试"""
    print("🧪 运行API连接测试...")
    
    try:
        # 使用最小请求测试
        test_response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "只说'连接成功'"}],
            max_tokens=5
        )
        
        if test_response.choices[0].message.content:
            print("✅ API连接成功！")
            print(f"   使用接口: {base_url if base_url else 'OpenAI官方接口'}")
            return True
        else:
            print("❌ API无响应")
            return False
            
    except openai.AuthenticationError as e:
        print(f"❌ API密钥错误: {e}")
        return False
    except openai.APIConnectionError as e:
        print(f"❌ 网络连接失败: {e}")
        return False
    except openai.RateLimitError as e:
        print(f"❌ 请求频率超限: {e}")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

def check_config():
    """检查配置信息"""
    print("🔧 检查当前配置...")
    
    if api_key:
        masked_key = f"{api_key[:8]}...{api_key[-4:]}" if len(api_key) > 12 else api_key
        print(f"   ✅ API密钥已设置 ({masked_key})")
    else:
        print("   ❌ API密钥未设置")
        return False
        
    if base_url:
        print(f"   ✅ 使用自定义接口: {base_url}")
    else:
        print("   ✅ 使用OpenAI官方接口")
        
    return True

if __name__ == "__main__":
    print("=" * 50)
    print("🎯 AI学习助手 - Day 1 启动")
    print("=" * 50)
    
    # 检查配置
    if not check_config():
        print("\n⚠️ 请检查.env配置文件")
        exit(1)
    
    # 运行API测试
    if test_api():
        print("\n🚀 开始对话！")
        simple_chat()
    else:
        print("\n⚠️ 请检查配置后重试")