import pandas as pd
import streamlit as st
from agent import run_treasury_analysis # 【新增】把我们写的 Agent 大脑引进来

st.set_page_config(
    page_title="K-Finance 智能财资管控中枢",
    page_icon="🏦",
    layout="wide",
)

st.title("K-Finance 智能财资管控中枢")

# 读取数据
df = pd.read_csv("data/global_balance.csv")

# 计算上方卡片的指标
total_accounts = len(df)
alert_accounts = int((df["Current_Balance"] < df["Alert_Threshold"]).sum())
system_status = "监控中"

# 渲染上方卡片
metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
metric_col_1.metric("总账户数", f"{total_accounts}")
metric_col_2.metric("今日预警账户数", f"{alert_accounts}")
metric_col_3.metric("当前系统状态", system_status)

# 渲染中间的数据表格
st.markdown("### 全球资金账户状态总览")
st.dataframe(df, use_container_width=True)

st.markdown("---") # 加一条分割线让界面更好看

# ==========================================
# 下面就是连接大脑的“核心聊天逻辑”
# ==========================================

# 1. 获取用户的输入框指令
prompt = st.chat_input("请输入您对资金调配的指令...")

# 2. 如果用户按下了回车（输入了内容）
if prompt:
    # 步骤 A：把用户的话显示在右侧（用户的头像）
    with st.chat_message("user"):
        st.write(prompt)
    
    # 步骤 B：让网页转圈圈，提示 AI 正在思考
    with st.spinner('数字员工 DeepSeek 正在分析财资数据并思考对策...'):
        # 核心：把用户的话传给跑在后台的 agent.py，等待它返回结果
        response = run_treasury_analysis(prompt)
        
    # 步骤 C：把 AI 返回的结果显示在左侧（机器人的头像）
    with st.chat_message("assistant"):
        st.write(response)