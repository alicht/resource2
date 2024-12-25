import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

def display_historical_logs(log_file_path):
    try:
        df = pd.read_csv(log_file_path)

        if not all(col in df.columns for col in ["Timestamp", "Total Tokens", "Cost"]):
            return {"error": "The required columns 'Timestamp', 'Total Tokens', and 'Cost' are missing."}

        # Attempt to parse timestamps with fallback for different formats
        def parse_timestamps(timestamp):
            try:
                return pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                return pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S")

        df["Timestamp"] = df["Timestamp"].apply(parse_timestamps)
        df = df.sort_values(by="Timestamp")

        # Plot historical data
        fig, ax = plt.subplots(2, 1, figsize=(10, 8))
        ax[0].plot(df["Timestamp"], df["Total Tokens"], label="Total Tokens", color="blue")
        ax[0].set_title("Total Tokens Over Time")
        ax[0].set_xlabel("Time")
        ax[0].set_ylabel("Tokens")
        ax[0].legend()

        ax[1].plot(df["Timestamp"], df["Cost"], label="Cost", color="red")
        ax[1].set_title("Cost Over Time")
        ax[1].set_xlabel("Time")
        ax[1].set_ylabel("Cost ($)")
        ax[1].legend()

        # Prediction
        df["Elapsed Time"] = (df["Timestamp"] - df["Timestamp"].min()).dt.total_seconds()
        X = df[["Elapsed Time"]].values
        y_tokens = df["Total Tokens"].values
        y_cost = df["Cost"].values

        token_model = LinearRegression()
        token_model.fit(X, y_tokens)

        cost_model = LinearRegression()
        cost_model.fit(X, y_cost)

        future_time = [[X[-1][0] + 86400]]  # 1 day into the future
        predicted_tokens = token_model.predict(future_time)[0]
        predicted_cost = cost_model.predict(future_time)[0]

        return {
            "dataframe": df,
            "plot": fig,
            "predictions": {
                "tokens": predicted_tokens,
                "cost": predicted_cost
            }
        }
    except Exception as e:
        return {"error": str(e)}
