import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def generate_insights(df):
    df["total_spend"] = df["r&d_spend"] + df["administration"] + df["marketing_spend"]
    df["roi"] = df["profit"] / df["total_spend"]

    top_roi = df.sort_values(by="roi", ascending=False).head(5)
    low_roi = df.sort_values(by="roi").head(5)

    combined = pd.concat([
        top_roi.assign(group="Top ROI"),
        low_roi.assign(group="Low ROI")
    ])

    # Improved Spending Comparison Barplot
    plt.figure(figsize=(12, 7))
    bar = sns.barplot(
        data=combined, x="group", y="total_spend", hue="state", palette="Set2"
    )
    plt.title("Total Spend Comparison: Top vs Low ROI Companies", fontsize=14)
    plt.xlabel("ROI Group", fontsize=12)
    plt.ylabel("Total Spend (USD)", fontsize=12)
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.legend(title="State", title_fontsize=11, fontsize=10, loc="upper right")
    for p in bar.patches:
        height = p.get_height()
        bar.annotate(
            f'{height:,.0f}',
            (p.get_x() + p.get_width() / 2., height),
            ha='center', va='bottom',
            fontsize=9, color='black', rotation=0, xytext=(0, 5),
            textcoords='offset points'
        )
    plt.tight_layout()
    plt.savefig("../outputs/spending_comparison.png")
    plt.close()

    # Improved Average Profit by State
    plt.figure(figsize=(10, 6))
    state_avg = df.groupby("state")["profit"].mean().sort_values(ascending=False)
    bars = state_avg.plot(kind="bar", color="steelblue", edgecolor="black")
    plt.title("Average Profit by State", fontsize=14)
    plt.xlabel("State", fontsize=12)
    plt.ylabel("Average Profit (USD)", fontsize=12)
    plt.xticks(rotation=0, fontsize=11)
    plt.yticks(fontsize=11)

    for i, val in enumerate(state_avg):
        bars.annotate(
            f'{val:,.0f}', 
            xy=(i, val), 
            xytext=(0, 5), 
            textcoords="offset points",
            ha='center', va='bottom', fontsize=9, color='black'
        )
    plt.tight_layout()
    plt.savefig("../outputs/profit_by_state.png")
    plt.close()