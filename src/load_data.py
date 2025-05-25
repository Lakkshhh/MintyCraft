import pandas as pd
def load_data(file_path):
    try:
        df = pd.read_csv(file_path)
        print("✅ Data loaded successfully.")
        return df
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return None

def clean_data(df):
    df.columns = df.columns.str.strip()
    print("Missing values:\n", df.isnull().sum())
    df_cleaned = df.dropna()
    print("✅ Data cleaned. Shape:", df_cleaned.shape)
    return df_cleaned

if __name__ == "__main__":
    data = load_data("data/50_Startups.csv")
    if data is not None:
        clean_data(data)
