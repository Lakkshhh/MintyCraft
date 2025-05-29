import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def perform_analysis(df):
    # Clean column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Derived columns
    df["total_spend"] = df["r&d_spend"] + df["administration"] + df["marketing_spend"]
    df["roi"] = df["profit"] / df["total_spend"]

    # Ensure output directory exists
    os.makedirs("E:/git/MintyCraft/outputs", exist_ok=True)

    # Correlation Matrix
    corr = df.corr(numeric_only=True)
    plt.figure(figsize=(10, 8))
    sns.heatmap(corr, annot=True, cmap="crest")
    plt.title("Correlation Matrix (Spend vs Profit)")
    plt.tight_layout()
    plt.savefig("E:/git/MintyCraft/outputs/correlation_matrix.png")
    plt.close()

    # ROI Distribution with Outliers
    plt.figure(figsize=(10, 6))
    sns.histplot(df["roi"], bins=12, kde=True, color="skyblue", edgecolor="black", alpha=0.7)
    Q1 = df["roi"].quantile(0.25)
    Q3 = df["roi"].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    outliers = df[(df["roi"] < lower_bound) | (df["roi"] > upper_bound)]
    mean_roi = df["roi"].mean()
    median_roi = df["roi"].median()
    plt.axvline(mean_roi, color='red', linestyle='--', linewidth=2, label=f"Mean ROI: {mean_roi:.2f}")
    plt.axvline(median_roi, color='green', linestyle='-.', linewidth=2, label=f"Median ROI: {median_roi:.2f}")
    if not outliers.empty:
        for outlier in outliers["roi"]:
            plt.axvline(outlier, color='purple', linestyle=':', linewidth=1.5, alpha=0.7)
    plt.title("Distribution of ROI with Outliers Highlighted", fontsize=14)
    plt.xlabel("ROI")
    plt.ylabel("Frequency")
    plt.legend()
    plt.grid(True, linestyle='--', alpha=0.5)
    sns.despine()
    plt.tight_layout()
    plt.savefig("E:/git/MintyCraft/outputs/roi_distribution.png")
    plt.close()
    # R&D Spend vs Profit
    plt.figure(figsize=(10, 6))
    sns.scatterplot(data=df, x="r&d_spend", y="profit", hue="state", palette="Set1")
    plt.title("R&D Spend vs Profit")
    plt.xlabel("R&D Spend")
    plt.ylabel("Profit")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend(title="State")
    plt.tight_layout()
    plt.savefig("E:/git/MintyCraft/outputs/rd_vs_profit.png")
    plt.close()

   # Marketing Spend by State (Boxplot)
    plt.figure(figsize=(10, 6))
    sns.boxplot(data=df, x="state", y="marketing_spend", palette="Set3")
    plt.title("Marketing Spend Distribution by State")
    plt.xlabel("State")
    plt.ylabel("Marketing Spend")
    plt.tight_layout()
    plt.savefig("E:/git/MintyCraft/outputs/marketing_by_state.png")
    plt.close()

    #Company-wise Profit
    df["company"] = df.index + 1
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df.sort_values("profit", ascending=False), x="company", y="profit", palette="Blues_d")
    plt.title("Company-wise Profit")
    plt.xlabel("Company")
    plt.ylabel("Profit")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("E:/git/MintyCraft/outputs/company_profit.png")
    plt.close()

    # Profit vs Administration Spend
    plt.figure(figsize=(10, 6))
    sns.regplot(data=df, x="administration", y="profit", scatter_kws={"color": "blue"}, line_kws={"color": "red"})
    plt.title("Profit vs Administration Spend")
    plt.xlabel("Administration Spend")
    plt.ylabel("Profit")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig("E:/git/MintyCraft/outputs/admin_vs_profit.png")
    plt.close()

    # Average ROI by State
    plt.figure(figsize=(10, 6))
    state_roi = df.groupby("state")["roi"].mean().sort_values(ascending=False)
    sns.barplot(x=state_roi.index, y=state_roi.values, palette="coolwarm")
    plt.title("Average ROI by State")
    plt.xlabel("State")
    plt.ylabel("Average ROI")
    plt.tight_layout()
    plt.savefig("E:/git/MintyCraft/outputs/state_avg_roi.png")
    plt.close()

    # Pie Chart for Spend Breakdown
    avg_spend = df[["r&d_spend", "administration", "marketing_spend"]].mean()
    plt.figure(figsize=(7, 7))
    plt.pie(avg_spend, labels=avg_spend.index.str.replace("_", " ").str.title(), autopct='%1.1f%%', colors=sns.color_palette("pastel"))
    plt.title("Average Spending Breakdown")
    plt.tight_layout()
    plt.savefig("E:/git/MintyCraft/outputs/spending_pie_chart.png")
    plt.close()

