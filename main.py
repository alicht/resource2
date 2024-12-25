import os  # Add this at the beginning of your file
import streamlit as st
from llm_insights import track_openai_usage
from aws_metrics import fetch_aws_metrics
from gcp_metrics import fetch_gcp_metrics
from azure_metrics import fetch_azure_metrics
from historical_logs import display_historical_logs
from utils import load_environment_variables
import openai
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np

# Load environment variables
load_environment_variables()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Check your .env file or environment variables.")


# Streamlit App
st.title("Unified Resource Monitor")

# Sidebar: LLM Insights
st.sidebar.header("LLM Insights")
prompt = st.sidebar.text_area("Enter your LLM prompt:")
if st.sidebar.button("Track Usage"):
    result = track_openai_usage(prompt)
    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader("OpenAI API Response")
        st.write(result["response"])

        st.subheader("Usage Details")
        st.write(f"Total Tokens: {result['total_tokens']}")
        st.write(f"Prompt Tokens: {result['prompt_tokens']}")
        st.write(f"Completion Tokens: {result['completion_tokens']}")
        st.write(f"Cost: ${result['cost']:.4f}")

# AWS Metrics Section
st.sidebar.header("AWS Metrics")
if st.sidebar.button("Fetch AWS Metrics"):
    metrics = fetch_aws_metrics()
    if "error" in metrics:
        st.error(metrics["error"])
    else:
        st.subheader("AWS Metrics")
        st.write(metrics)


# Historical Logs Section
st.sidebar.header("Historical Logs")
log_file_path = "llm_usage_logs.csv"
if st.sidebar.button("View Historical Logs"):
    try:
        df = pd.read_csv(log_file_path)
        st.subheader("Historical LLM Usage Logs and Predictions")

        # Check for required columns
        if not all(col in df.columns for col in ["Timestamp", "Total Tokens", "Cost"]):
            st.error("The required columns 'Timestamp', 'Total Tokens', and 'Cost' are missing from the log file.")
        else:
            # Handle mixed timestamp formats
            def parse_mixed_timestamps(timestamp):
                try:
                    return pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S.%f")
                except ValueError:
                    return pd.to_datetime(timestamp, format="%Y-%m-%d %H:%M:%S")

            df["Parsed Timestamp"] = df["Timestamp"].apply(parse_mixed_timestamps)

            # Log invalid rows
            invalid_rows = df[df["Parsed Timestamp"].isnull()]
            if not invalid_rows.empty:
                st.error("Some timestamps could not be parsed. Invalid rows are listed below:")
                st.write(invalid_rows)
            else:
                df["Timestamp"] = df["Parsed Timestamp"]
                df = df.drop(columns=["Parsed Timestamp"])
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

                st.pyplot(fig)

                # Prediction
                df["Elapsed Time"] = (df["Timestamp"] - df["Timestamp"].min()).dt.total_seconds()
                X = df[["Elapsed Time"]].values
                y_tokens = df["Total Tokens"].values
                y_cost = df["Cost"].values

                token_model = LinearRegression()
                token_model.fit(X, y_tokens)

                cost_model = LinearRegression()
                cost_model.fit(X, y_cost)

                future_time = np.array([[X[-1][0] + 86400]])  # 1 day into the future
                predicted_tokens = token_model.predict(future_time)[0]
                predicted_cost = cost_model.predict(future_time)[0]

                st.write("## Predictions")
                st.write(f"Predicted Total Tokens for Tomorrow: {predicted_tokens:.2f}")
                st.write(f"Predicted Cost for Tomorrow: ${predicted_cost:.4f}")

    except Exception as e:
        st.error(f"Error loading historical data: {e}")


# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed by Spaire Team")
