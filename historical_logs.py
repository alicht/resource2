import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def display_historical_logs(log_file_path):
    """
    Displays historical logs and visualizes trends.
    :param log_file_path: Path to the CSV file containing the historical logs.
    """
    try:
        # Load the log file into a DataFrame
        df = pd.read_csv(log_file_path)

        # Display the logs in a table
        st.subheader("Historical LLM Usage Logs")
        st.dataframe(df)

        # Visualize token and cost trends
        st.subheader("LLM Usage Trends")
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        ax[0].plot(df["Total Tokens"], label="Total Tokens", marker="o")
        ax[0].set_title("Token Usage Over Time")
        ax[0].set_xlabel("Requests")
        ax[0].set_ylabel("Tokens")
        ax[0].legend()

        ax[1].plot(df["Cost"], label="Cost", color="red", marker="o")
        ax[1].set_title("Cost Over Time")
        ax[1].set_xlabel("Requests")
        ax[1].set_ylabel("Cost (USD)")
        ax[1].legend()

        st.pyplot(fig)
    except FileNotFoundError:
        st.error(f"Log file not found: {log_file_path}")
    except Exception as e:
        st.error(f"Error loading historical logs: {str(e)}")
