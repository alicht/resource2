import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from prediction import train_prediction_model, predict_future_value
import streamlit as st

def display_historical_logs(log_file_path):
    try:
        # Load the historical log data
        df = pd.read_csv(log_file_path)

        # Ensure required columns exist
        if not all(col in df.columns for col in ["Timestamp", "Total Tokens", "Cost"]):
            st.error("The required columns 'Timestamp', 'Total Tokens', and 'Cost' are missing from the log file.")
            return

        # Parse timestamps and handle formats
        def parse_timestamps(timestamp):
            try:
                return pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                return pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S")

        try:
            df["Timestamp"] = df["Timestamp"].apply(parse_timestamps)
            df = df.sort_values(by="Timestamp")
        except Exception as e:
            st.error(f"Error parsing timestamps: {e}")
            return

        # Calculate elapsed time
        df["Elapsed Time"] = (df["Timestamp"] - df["Timestamp"].min()).dt.total_seconds()

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

        st.pyplot(fig)

        # Prediction
        token_model = train_prediction_model(df, "Total Tokens")
        cost_model = train_prediction_model(df, "Cost")

        current_elapsed_time = df["Elapsed Time"].max()
        predicted_tokens = predict_future_value(token_model, current_elapsed_time, days_into_future=1)
        predicted_cost = predict_future_value(cost_model, current_elapsed_time, days_into_future=1)

        st.write("## Predictions")
        st.write(f"Predicted Total Tokens for Tomorrow: {predicted_tokens:.2f}")
        st.write(f"Predicted Cost for Tomorrow: ${predicted_cost:.4f}")

    except Exception as e:
        st.error(f"Error loading historical data: {e}")
