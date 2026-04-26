"""
AI学习助手 - 第一天：基础对话功能
运行命令: python main.py
"""
import openai
import os
from dotenv import load_dotenv

# 1. 加载环境变量
load_dotenv()  # 从 .env 文件加载

# 2. 配置OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

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
            response = openai.chat.completions.create(
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
            
        except Exception as e:
            print(f"\n❌ 出错: {e}")
            print("💡 检查: 1. API密钥 2. 网络连接 3. API余额")

def test_api():
    """快速API测试"""
    print("🧪 运行API连接测试...")
    
    try:
        # 使用最小请求测试
        test_response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "只说'连接成功'"}],
            max_tokens=5
        )
        
        if test_response.choices[0].message.content:
            print("✅ API连接成功！")
            return True
        else:
            print("❌ API无响应")
            return False
            
    except openai.AuthenticationError:
        print("❌ API密钥错误")
        return False
    except openai.APIConnectionError:
        print("❌ 网络连接失败")
        return False
    except Exception as e:
        print(f"❌ 未知错误: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("🎯 AI学习助手 - Day 1 启动")
    print("=" * 50)
    
    # 运行API测试
    if test_api():
        print("\n🚀 开始对话！")
        simple_chat()
    else:
        print("\n⚠️ 请检查配置后重试")