# K-Finance: 基于 LLM Agent 的企业级智能财资管控中枢 

K-Finance 是一个将金融科技业务逻辑与大模型推理能力深度结合的 AI Agent 原型。它利用 **LangGraph** 架构，实现了从“实时数据监控”到“智能调配决策”的完整闭环。

---

## 核心亮点 (Key Features)

* **感知层（Perception）**：自动巡检全球子公司账户余额，根据动态预警线实时识别资金缺口。
* **决策层（Brain）**：接入 **DeepSeek-V3** 满血版模型，具备强大的 ReAct（Reasoning and Acting）推理能力。
* **交互层（Interface）**：
    * **CoT (Chain of Thought) 可视化**：实时展示 Agent 的思考链路，解决金融 AI 的“黑盒”信任问题。
    * **动态风控模拟**：支持通过侧边栏滑动条实时调整全局风险阈值。
* **执行工具（Tools）**：集成自定义 Python Tools，实现精准的跨币种汇率折算与调拨方案计算。

---

## 🛠️ 技术栈 (Tech Stack)

* **LLM 框架**: LangChain & LangGraph (Stateful Agentic Workflow)
* **大模型**: DeepSeek-V3 (via SiliconFlow API)
* **前端框架**: Streamlit
* **数据处理**: Pandas
* **环境管理**: Python-dotenv & Git

---

## 业务逻辑与价值 (Business Value)

1.  **降本增效**：将原本复杂的跨国资金核算与调配决策从“小时级”压缩至“秒级”。
2.  **决策严谨**：通过 AI 自动计算成本最低、路径最短的调拨预案，减少汇兑损失。
3.  **合规透明**：每一条建议都附带完整的推理过程与计算依据，符合金融监管对决策可溯源的要求。

---

## 快速启动 (Quick Start)

1.  **克隆仓库**
    ```bash
    git clone [https://github.com/你的用户名/k-finance-agent.git](https://github.com/你的用户名/k-finance-agent.git)
    cd k-finance-agent
    ```

2.  **安装依赖**
    ```bash
    pip install -r requirements.txt
    ```

3.  **配置环境变量**
    在项目根目录创建 `.env` 文件，填入：
    ```text
    OPENAI_API_BASE="[https://api.siliconflow.cn/v1](https://api.siliconflow.cn/v1)"
    OPENAI_API_KEY="你的API_KEY"
    ```

4.  **运行应用**
    ```bash
    streamlit run app.py
    ```

---

## 作者
**Wang Jingya** *The University of Hong Kong (HKU) - MSc in FinTech & AI*