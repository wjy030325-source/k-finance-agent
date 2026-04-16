from langchain.tools import tool
import pandas as pd


@tool
def get_account_balances() -> str:
    """
    读取并汇总全球子公司资金账户状态，返回适合对话展示的清晰文本。

    何时调用：
    - 用户询问“当前各账户余额”“哪些分支触发预警”“请给我账户总览”等问题时。
    - Agent 在执行资金调配、风险分析前，需要先获取最新账户基线数据时。

    输入参数：
    - 无参数。

    输出说明：
    - 返回字符串，包含每个账户的实体名、币种、当前余额、预警线和状态（正常/预警）。
    - 在末尾附带汇总统计（总账户数、预警账户数）。
    - 若文件读取失败或字段缺失，返回可直接给用户展示的错误信息字符串。
    """
    try:
        df = pd.read_csv("data/global_balance.csv")
    except Exception as exc:
        return f"读取 data/global_balance.csv 失败：{exc}"

    required_columns = {
        "Account_Entity",
        "Currency",
        "Current_Balance",
        "Alert_Threshold",
    }
    missing_columns = required_columns - set(df.columns)
    if missing_columns:
        missing_str = ", ".join(sorted(missing_columns))
        return f"数据缺少必要字段：{missing_str}"

    lines = ["全球账户资金状态："]
    for _, row in df.iterrows():
        current_balance = float(row["Current_Balance"])
        alert_threshold = float(row["Alert_Threshold"])
        status = "预警" if current_balance < alert_threshold else "正常"
        lines.append(
            f"- {row['Account_Entity']} | {row['Currency']} | "
            f"当前余额: {current_balance:,.2f} | 预警线: {alert_threshold:,.2f} | 状态: {status}"
        )

    alert_count = int((df["Current_Balance"] < df["Alert_Threshold"]).sum())
    lines.append(f"\n汇总：总账户数 {len(df)}，预警账户数 {alert_count}。")
    return "\n".join(lines)


@tool
def calculate_exchange(source_currency: str, target_currency: str, amount: float) -> str:
    """
    基于内置模拟汇率进行货币兑换计算，返回目标金额与所用汇率。

    何时调用：
    - 用户要求“把某金额从 A 币种换算到 B 币种”时。
    - Agent 在生成跨币种调拨建议、估算调拨后余额影响时。

    输入参数：
    - source_currency (str): 源币种代码，例如 USD、HKD、GBP、SGD。
    - target_currency (str): 目标币种代码，例如 USD、HKD、GBP、SGD。
    - amount (float): 待兑换金额，必须为非负数。

    输出说明：
    - 返回字符串，包含输入金额、源币种、目标币种、使用汇率以及计算后的目标金额。
    - 若币对未配置或金额非法，返回友好错误提示字符串，便于 Agent 继续追问或纠正。
    """
    source = source_currency.upper().strip()
    target = target_currency.upper().strip()

    try:
        amount_value = float(amount)
    except (TypeError, ValueError):
        return "amount 必须是可解析的数字。"

    if amount_value < 0:
        return "amount 不能为负数。"

    if source == target:
        return (
            f"兑换结果：{amount_value:,.2f} {source} = {amount_value:,.2f} {target} "
            f"(汇率: 1 {source} = 1.0 {target})"
        )

    exchange_rates = {
        ("USD", "HKD"): 7.8,
        ("HKD", "USD"): 0.128,
        ("GBP", "USD"): 1.2,
        ("USD", "GBP"): 0.8333,
        ("USD", "SGD"): 1.35,
        ("SGD", "USD"): 0.7407,
        ("GBP", "HKD"): 9.36,
        ("HKD", "GBP"): 0.1068,
        ("SGD", "HKD"): 5.77,
        ("HKD", "SGD"): 0.1732,
    }

    rate = exchange_rates.get((source, target))
    if rate is None:
        return f"暂未配置 {source} -> {target} 的模拟汇率。"

    converted_amount = amount_value * rate
    return (
        f"兑换结果：{amount_value:,.2f} {source} = {converted_amount:,.2f} {target} "
        f"(汇率: 1 {source} = {rate} {target})"
    )

