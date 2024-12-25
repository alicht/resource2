import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

def display_historical_logs(log_file_path):
    try:
        # Load data
        df = pd.read_csv(log_file_path)
        df["Time"] = pd.to_datetime(df["Time"])
        
        # Prepare data for prediction
        df["Seconds"] = (df["Time"] - df["Time"].min()).dt.total_seconds()
        X = df["Seconds"].values.reshape(-1, 1)
        y_tokens = df["Total Tokens"].values
        y_cost = df["Cost"].values

        # Train models
        model_tokens = LinearRegression()
        model_cost = LinearRegression()
        model_tokens.fit(X, y_tokens)
        model_cost.fit(X, y_cost)

        # Make predictions for the next 30 days
        future_seconds = np.arange(X.max() + 86400, X.max() + 86400 * 31, 86400).reshape(-1, 1)
        predicted_tokens = model_tokens.predict(future_seconds)
        predicted_cost = model_cost.predict(future_seconds)

        # Plot historical data
        fig, ax = plt.subplots(2, 1, figsize=(10, 8))

        ax[0].plot(df["Time"], df["Total Tokens"], label="Historical Tokens", marker="o")
        ax[0].plot(
            pd.date_range(df["Time"].max() + pd.Timedelta(days=1), periods=30, freq="D"),
            predicted_tokens,
            label="Predicted Tokens",
            linestyle="--",
            color="orange",
        )
        ax[0].set_title("Token Usage Over Time")
        ax[0].set_xlabel("Time")
        ax[0].set_ylabel("Tokens")
        ax[0].legend()

        ax[1].plot(df["Time"], df["Cost"], label="Historical Cost", marker="o")
        ax[1].plot(
            pd.date_range(df["Time"].max() + pd.Timedelta(days=1), periods=30, freq="D"),
            predicted_cost,
            label="Predicted Cost",
            linestyle="--",
            color="red",
        )
        ax[1].set_title("Cost Over Time")
        ax[1].set_xlabel("Time")
        ax[1].set_ylabel("Cost ($)")
        ax[1].legend()

        plt.tight_layout()
        plt.show()

        return fig

    except Exception as e:
        return f"Error during prediction: {str(e)}"
