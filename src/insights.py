import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from gpt4all import GPT4All

model_path = "/Users/lakkshtyagi/Downloads/MintyCraft/models/mistral-7b-v0.1.Q4_K_M.gguf"
model = GPT4All(model_path, allow_download=False)

def generate_gpt_summary(df_stats: str) -> str:
    prompt = f"""
You are an analytics assistant. Given this pandas DataFrame summary and insights, write a paragraph summarizing the findings for a business audience. Be concise, use professional language, and focus on profit, ROI, and state-wise performance.

Here is the data:
{df_stats}
"""
    output = model.generate(prompt, max_tokens=300, temp=0.7)
    return output.strip()

def generate_insights(df):
    df["total_spend"] = df["r&d_spend"] + df["administration"] + df["marketing_spend"]
    df["roi"] = df["profit"] / df["total_spend"]

    top_roi = df.sort_values(by="roi", ascending=False).head(5)
    low_roi = df.sort_values(by="roi").head(5)

    combined = pd.concat([
        top_roi.assign(group="Top ROI"),
        low_roi.assign(group="Low ROI")
    ])

    # Barplot: Top vs Low ROI
    plt.figure(figsize=(12, 7))
    bar = sns.barplot(
        data=combined, x="group", y="total_spend", hue="state", palette="Set2"
    )
    plt.title("Total Spend Comparison: Top vs Low ROI Companies")
    plt.xlabel("ROI Group")
    plt.ylabel("Total Spend (USD)")
    for p in bar.patches:
        height = p.get_height()
        bar.annotate(
            f'{height:,.0f}',
            (p.get_x() + p.get_width() / 2., height),
            ha='center', va='bottom',
            fontsize=9, color='black', xytext=(0, 5), textcoords='offset points'
        )
    plt.tight_layout()
    os.makedirs("../outputs", exist_ok=True)
    plt.savefig("../outputs/spending_comparison.png")
    plt.close()

    # fig = px.bar(
    #     combined,
    #     x="group",
    #     y="total_spend",
    #     color="state",
    #     barmode="group",
    #     text_auto=".2s",  # Auto-format labels
    #     color_discrete_sequence=px.colors.qualitative.Set2,
    #     title="Total Spend Comparison: Top vs Low ROI Companies"
    # )

    # fig.update_layout(
    #     xaxis_title="ROI Group",
    #     yaxis_title="Total Spend (USD)",
    #     title_font=dict(size=18),
    #     legend_title="State",
    #     legend_font=dict(size=12),
    #     xaxis=dict(tickfont=dict(size=11)),
    #     yaxis=dict(tickfont=dict(size=11)),
    #     bargap=0.2,
    #     margin=dict(l=40, r=40, t=80, b=40)
    # )

    # # Save the interactive plot as an HTML file
    # fig.write_html("../outputs/spending_comparison.html")

    # Barplot: Avg Profit by State
    plt.figure(figsize=(10, 6))
    state_avg_profit = df.groupby("state")["profit"].mean().sort_values(ascending=False)
    bars = state_avg_profit.plot(kind="bar", color="steelblue", edgecolor="black")
    plt.title("Average Profit by State")
    plt.xlabel("State")
    plt.ylabel("Average Profit (USD)")
    for i, val in enumerate(state_avg_profit):
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

    # Preparing summary text
    summary_str = f"""
Top 5 ROI Companies:
{top_roi[['state', 'total_spend', 'roi', 'profit']].to_string(index=False)}

Bottom 5 ROI Companies:
{low_roi[['state', 'total_spend', 'roi', 'profit']].to_string(index=False)}

Average Profit by State:
{state_avg_profit.to_string()}
"""

    # Saving it
    summary = generate_gpt_summary(summary_str)
    with open("../outputs/data_insights_summary_gpt.txt", "w", encoding="utf-8") as f:
        f.write("GPT4All-Generated Summary: \n\n")
        f.write(summary)

    print("GPT summary has been generated!")