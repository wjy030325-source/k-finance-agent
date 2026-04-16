import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import SystemMessage, HumanMessage
from tools import get_account_balances, calculate_exchange

# 1. 加载 .env 里的硅基流动 API Key
load_dotenv()

# 2. 初始化大模型 (使用硅基流动的 DeepSeek-V3)
llm = ChatOpenAI(
    model="deepseek-ai/DeepSeek-V3", 
    temperature=0.1
)

# 3. 准备工具箱
tools = [get_account_balances, calculate_exchange]

# 4. 构建 Agent (这次我们不传容易报错的参数，保持最干净的初始化)
app = create_react_agent(model=llm, tools=tools)

# 5. 对外暴露的接口函数
def run_treasury_analysis(user_query: str) -> str:
    # 把“人设”写在这里
    system_prompt = """你是一名高级财资数字员工 K-Finance。
你的任务是调用工具分析各分公司的账户余额。
如果发现某账户余额低于预警线，你必须寻找另一个余额充足的账户，调用汇率工具计算，制定出调拨方案以填补缺口。
请给出明确的调拨金额、路径、计算过程和理由。"""
    
    # 巧妙的解法：强行把人设作为对话的第一句 (SystemMessage)，用户的提问作为第二句 (HumanMessage)
    result = app.invoke({
        "messages": [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_query)
        ]
    })
    
    # 返回大模型的最后一句回答
    return result["messages"][-1].content