import pandas as pd
import yfinance as yf

# 1. Fetch Data
print("📥 Fetching data...")
df = yf.download("AAPL", period="5d", interval="1h")  # Apple stock, last 5 days hourly
df.reset_index(inplace=True)
df.to_csv("raw_data.csv", index=False)
print("✅ Data fetched and saved to raw_data.csv")

# 2. Clean Data
print("🧹 Cleaning data...")
df = df.dropna()
if isinstance(df.columns, pd.MultiIndex):
    df.columns = [' '.join(col).strip() for col in df.columns.values]

# Ensure Close column exists
close_col_name = "Close"
if close_col_name not in df.columns:
    # Sometimes yfinance renames to "Close AAPL"
    possible_cols = [col for col in df.columns if "Close" in col]
    if possible_cols:
        close_col_name = possible_cols[0]
    else:
        raise KeyError("No Close column found in dataframe")

# Convert Close column to float
df["Close"] = df[close_col_name].astype(float)
df = df[df["Close"] > 0]   # keep only positive prices
df.to_csv("clean_data.csv", index=False)
print("✅ Data cleaned and saved to clean_data.csv")

# 3. Analyze Data
print("📊 Analyzing data...")
avg_close = df["Close"].mean()
latest_close = df.iloc[-1]["Close"]
results = pd.DataFrame({
    "average_close": [avg_close],
    "latest_close": [latest_close]
})
results.to_csv("results.csv", index=False)
print("✅ Analysis complete, results saved to results.csv")

# 4. Simple Tests (Validation)
print("🧪 Running tests...")

# Check data is not empty
assert not df.empty, "❌ DataFrame is empty after cleaning!"

# Check closing prices are valid
assert (df["Close"] > 0).all(), "❌ Found invalid (non-positive) closing prices!"

# Check timestamps are sorted
assert df["Datetime"].is_monotonic_increasing, "❌ Timestamps are not sorted!"

print("✅ All tests passed: Data looks good 🎉")
