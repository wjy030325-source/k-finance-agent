import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from tools import get_account_balances, calculate_exchange

# 1. 加载环境变量
load_dotenv()

# 2. 初始化大模型 (满血版 DeepSeek-V3)
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3", 
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    openai_api_base=os.getenv("OPENAI_API_BASE"),
    temperature=0.1
)

# 3. 准备工具箱
tools = [get_account_balances, calculate_exchange]

# 4. 构建 Agent
app = create_react_agent(model=llm, tools=tools)

# 5. 对外暴露的接口函数
def run_treasury_analysis(user_query: str) -> str:
    system_prompt = """你是一名高级财资数字员工 K-Finance。
你的任务是调用工具分析各分公司的账户余额。
如果发现某账户余额低于预警线，你必须寻找另一个余额充足的账户，调用汇率工具计算，制定出调拨方案。
请给出明确的调拨金额、路径、计算过程和理由。回答要专业、干练。"""
    
    result = app.invoke({
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]
    })
    
    return result["messages"][-1].content