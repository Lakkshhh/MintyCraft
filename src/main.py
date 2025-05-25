from load_data import load_and_clean_data
from spending_analysis import analyze_spending
from customer_analysis import analyze_performance
from visualizer import generate_graphs

def main():
    df = load_and_clean_data("data/50_Startups.csv")
    spending_insights = analyze_spending(df)
    performance_insights = analyze_performance(df)
    generate_graphs(spending_insights, performance_insights)

if __name__ == "__main__":
    main()