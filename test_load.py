import os
from dotenv import load_dotenv

load_dotenv()
key = os.getenv("OPENAI_API_KEY")

if key:
    print(f"✅ 成功从环境变量加载密钥。")
    print(f"   密钥前8位: {key[:8]}...")
    print(f"   密钥长度: {len(key)} 字符")
else:
    print("❌ 失败：未找到 OPENAI_API_KEY 环境变量。")
