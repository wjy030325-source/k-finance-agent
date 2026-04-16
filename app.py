import pandas as pd
import streamlit as st
import time
from agent import run_treasury_analysis

# ==========================================
# 页面基础配置
# ==========================================
st.set_page_config(
    page_title="K-Finance 智能财资中枢",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded" # 默认展开侧边栏
)

# ==========================================
# 侧边栏：全局参数控制区 (体现产品灵活性)
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/bank-building.png", width=60)
    st.markdown("## 系统设置")
    st.markdown("---")
    
    # 允许用户动态调整全局预警系数，体现系统不是写死的
    risk_multiplier = st.slider(
        "全局风险预警系数 (倍率)", 
        min_value=0.5, 
        max_value=2.0, 
        value=1.0, 
        step=0.1,
        help="调整此系数将成倍放大或缩小所有账户的预警红线。"
    )
    st.markdown("---")
    st.info("💡 **PM 说明**：真实的财资系统应允许财务总监根据市场波动率，动态调整各子公司的资金留存红线。")

# ==========================================
# 主页面：数据感知层
# ==========================================
st.title("K-Finance 智能财资管控中枢")
st.markdown("基于 LangGraph 架构的跨国资金协同调度 Agent")

# 读取基础数据
df = pd.read_csv("data/global_balance.csv")

# 根据侧边栏的系数，动态计算“实际预警线”
df["动态预警线"] = df["Alert_Threshold"] * risk_multiplier

# 计算风险指标
total_accounts = len(df)
# 判断哪些账户余额低于了动态预警线
risk_mask = df["Current_Balance"] < df["动态预警线"]
alert_accounts = int(risk_mask.sum())
system_status = "⚠️ 警报响应" if alert_accounts > 0 else "✅ 监控中"

# 渲染顶部 KPI 卡片
metric_col_1, metric_col_2, metric_col_3 = st.columns(3)
metric_col_1.metric("全球活跃账户", f"{total_accounts} 个")

# 如果有预警，用红色强调 (Streamlit 原生特性：负面 delta 为红)
if alert_accounts > 0:
    metric_col_2.metric("资金风险账户", f"{alert_accounts} 个", delta="-需立即调拨", delta_color="inverse")
else:
    metric_col_2.metric("资金风险账户", f"{alert_accounts} 个", delta="资金健康", delta_color="normal")
    
metric_col_3.metric("Agent 调度引擎", system_status)

# 渲染中间的数据表格 (高亮显示有风险的行)
st.markdown("### 全球账户实时账本")

# 这是一个 Pandas 样式函数，把风险账户标黄
def highlight_risk(row):
    if row["Current_Balance"] < row["动态预警线"]:
        return ['background-color: rgba(255, 99, 71, 0.2)'] * len(row)
    return [''] * len(row)

st.dataframe(
    df.style.apply(highlight_risk, axis=1).format({
        "Current_Balance": "${:,.0f}",
        "Alert_Threshold": "${:,.0f}",
        "动态预警线": "${:,.0f}"
    }), 
    use_container_width=True
)

st.markdown("---")

# ==========================================
# 主页面：智能决策层 (Agent 交互区)
# ==========================================
st.markdown("### 🧠 财资调度指令中心")

prompt = st.chat_input("示例指令：帮我分析目前的资金数据，并给出跨国调拨方案...")

if prompt:
    with st.chat_message("user"):
        st.write(prompt)
    
    # 核心优化：可视化 Agent 思考链路
    with st.status("K-Finance 数字员工正在推理...", expanded=True) as status:
        st.write("🔍 连接核心账本，扫描全球实时余额...")
        time.sleep(1) # 增加延迟感，显得更逼真
        st.write("⚖️ 执行风险探针，识别违约缺口...")
        time.sleep(1)
        st.write("🌐 接入外汇数据中心，预估跨币种调拨损耗...")
        
        # 真正调用后台大模型
        response = run_treasury_analysis(prompt)
        
        # 完成后收起状态框
        status.update(label="✅ 资金调配最优策略已生成", state="complete", expanded=False)
        
    with st.chat_message("assistant"):
        st.write(response)