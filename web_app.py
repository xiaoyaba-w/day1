"""
AI学习助手 - Web界面版本
运行命令: streamlit run web_app.py
"""
import streamlit as st
import sys
from pathlib import Path
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.append(str(project_root))

# 导入项目模块
try:
    from src.ai_service import AIService
    from config import Config
    from utils.export_utils import export_to_markdown
    IMPORT_SUCCESS = True
except ImportError as e:
    logger.warning(f"模块导入失败: {e}")
    IMPORT_SUCCESS = False

# 页面配置
st.set_page_config(
    page_title="AI学习助手",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded"
)

# ========== 初始化会话状态 ==========
# 这是修复的关键：在访问前初始化所有需要的状态变量
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "你好！我是你的AI学习助手，专门帮助你准备秋招面试。有什么问题都可以问我！"}
    ]

# 修复：初始化所有会话状态变量
if "api_key" not in st.session_state:
    st.session_state.api_key = ""
if "api_configured" not in st.session_state:
    st.session_state.api_configured = False
if "base_url" not in st.session_state:
    st.session_state.base_url = "https://api.zhizengzeng.com/v1"
if "model" not in st.session_state:
    st.session_state.model = "gpt-3.5-turbo"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 300
if "theme" not in st.session_state:
    st.session_state.theme = "默认"

# 页面标题
st.title("🤖 AI学习助手 - 秋招冲刺伴侣")
st.markdown("---")

# 侧边栏配置
with st.sidebar:
    st.header("⚙️ 配置")
    
    # API配置
    st.subheader("API设置")
    
    # 从config中获取默认值（如果可用）
    default_api_key = ""
    default_base_url = "https://api.zhizengzeng.com/v1"
    
    if IMPORT_SUCCESS and hasattr(Config, 'OPENAI_API_KEY') and Config.OPENAI_API_KEY:
        default_api_key = Config.OPENAI_API_KEY
    if IMPORT_SUCCESS and hasattr(Config, 'OPENAI_BASE_URL') and Config.OPENAI_BASE_URL:
        default_base_url = Config.OPENAI_BASE_URL
    
    # API密钥输入
    api_key = st.text_input(
        "API密钥", 
        value=st.session_state.api_key or default_api_key,
        type="password", 
        help="输入您的智增增平台API密钥"
    )
    
    # API地址输入
    base_url = st.text_input(
        "API地址", 
        value=st.session_state.base_url or default_base_url,
        help="API服务地址，默认使用智增增平台"
    )
    
    # 保存配置按钮
    if st.button("🔧 保存配置", type="primary", use_container_width=True):
        if api_key.strip():
            st.session_state.api_key = api_key.strip()
            st.session_state.base_url = base_url.strip()
            st.session_state.api_configured = True
            st.success("✅ 配置已保存！")
            st.rerun()
        else:
            st.error("❌ API密钥不能为空")
    
    st.markdown("---")
    
    # 模型选择
    st.subheader("模型设置")
    model = st.selectbox(
        "选择AI模型",
        ["gpt-3.5-turbo", "gpt-4", "gpt-4-turbo"],
        index=0,
        help="选择要使用的AI模型"
    )
    st.session_state.model = model
    
    # 参数调节
    st.subheader("参数调节")
    
    temperature = st.slider(
        "随机性 (Temperature)", 
        0.0, 2.0, 0.7, 0.1,
        help="值越高回答越随机有创意，值越低回答越确定保守"
    )
    st.session_state.temperature = temperature
    
    max_tokens = st.slider(
        "最大生成长度 (Max Tokens)", 
        50, 2000, 300, 50,
        help="控制AI回复的最大长度，token是文本单位"
    )
    st.session_state.max_tokens = max_tokens
    
    st.markdown("---")
    
    # 主题切换
    st.subheader("🎨 界面设置")
    theme = st.selectbox(
        "选择主题",
        ["默认", "简洁", "专业"],
        index=0
    )
    st.session_state.theme = theme
    
    st.markdown("---")
    
    # 工具按钮
    st.subheader("🛠️ 工具")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗑️ 清空对话", use_container_width=True):
            st.session_state.messages = [
                {"role": "assistant", "content": "对话已清空，有什么可以帮助你的？"}
            ]
            st.rerun()
    
    with col2:
        if st.button("💾 导出对话", use_container_width=True):
            if st.session_state.messages and len(st.session_state.messages) > 1:
                try:
                    if IMPORT_SUCCESS:
                        filename = export_to_markdown(st.session_state.messages)
                        st.success(f"✅ 对话已导出到: {filename}")
                        
                        # 提供下载
                        with open(filename, "rb") as f:
                            st.download_button(
                                label="📥 下载文件",
                                data=f,
                                file_name=filename,
                                mime="text/markdown"
                            )
                    else:
                        st.error("导出模块加载失败")
                except Exception as e:
                    st.error(f"导出失败: {str(e)}")
            else:
                st.warning("没有对话内容可导出")
    
    st.markdown("---")
    
    # 使用说明
    with st.expander("📖 使用说明", expanded=False):
        st.markdown("""
        ### 使用指南
        
        1. **配置API**（首次使用必须）
           - 在侧边栏输入您的API密钥
           - 点击"保存配置"按钮
        
        2. **开始对话**
           - 在下方输入框提问
           - AI助手会即时回复
        
        3. **功能说明**
           - 🗑️ 清空对话：重置聊天记录
           - 💾 导出对话：保存为Markdown文件
           - ⚙️ 参数调节：调整AI回复风格
        
        4. **温馨提示**
           - API密钥仅保存在浏览器会话中
           - 刷新页面会清空对话记录
           - 建议定期导出重要对话
        """)
    
    # 状态显示
    st.markdown("---")
    st.subheader("📊 状态")
    
    if st.session_state.api_configured:
        st.success("✅ API已配置")
    else:
        st.warning("⚠️ 请配置API密钥")
    
    st.caption(f"对话数: {len(st.session_state.messages)}")
    st.caption(f"模型: {st.session_state.model}")
    st.caption(f"当前主题: {st.session_state.theme}")

# 主界面 - 聊天区域
st.header("💬 与AI助手对话")

# 显示聊天历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 用户输入区域
st.markdown("---")
if prompt := st.chat_input("请输入您的问题...", key="user_input"):
    # 检查API配置
    if not st.session_state.get("api_configured", False):
        st.error("""
        ⚠️ **请先配置API密钥**
        
        1. 点击左侧边栏展开配置面板
        2. 在"API设置"中输入您的API密钥
        3. 点击"保存配置"按钮
        4. 然后就可以开始对话了
        """)
        st.stop()
    
    # 添加用户消息
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # 准备AI回复
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("⏳ AI思考中...")
        
        try:
            # 初始化AI服务
            ai_service = AIService(
                api_key=st.session_state.api_key,
                base_url=st.session_state.base_url
            )
            
            # 调用AI
            ai_response = ai_service.chat_completion(
                messages=st.session_state.messages[:-1],  # 不包含刚刚添加的用户消息
                model=st.session_state.model,
                temperature=st.session_state.temperature,
                max_tokens=st.session_state.max_tokens
            )
            
            # 显示AI回复
            message_placeholder.markdown(ai_response)
            
            # 添加助手消息到历史
            st.session_state.messages.append(
                {"role": "assistant", "content": ai_response}
            )
            
        except Exception as e:
            error_msg = f"""
            ❌ **出错了**
            
            **错误详情**: {str(e)}
            
            **可能的原因**:
            1. API密钥错误或已失效
            2. 网络连接问题
            3. API服务暂时不可用
            4. 账户余额不足
            
            **解决方法**:
            1. 检查侧边栏的API配置是否正确
            2. 确认网络连接正常
            3. 稍后重试
            """
            message_placeholder.markdown(error_msg)
            
            # 添加错误消息到历史
            st.session_state.messages.append(
                {"role": "assistant", "content": f"错误: {str(e)}"}
            )

# 页面底部信息
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])

with col1:
    st.caption(f"🚀 AI学习助手 v1.0 | 秋招冲刺项目")
    
with col2:
    if st.session_state.api_configured:
        st.caption("🔐 API: 已配置")
    else:
        st.caption("🔐 API: 未配置")
        
with col3:
    st.caption(f"🤖 模型: {st.session_state.model}")

# 页脚
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: gray; font-size: 0.8em;'>
    提示：本工具旨在帮助学习，AI生成内容仅供参考，请结合实际情况判断
    </div>
    """,
    unsafe_allow_html=True
)