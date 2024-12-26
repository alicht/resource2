import streamlit as st
from llm_insights import track_openai_usage
from aws_metrics import fetch_aws_metrics
from historical_logs import display_historical_logs
from utils import load_environment_variables
from prediction import train_prediction_model, predict_future_value  # Import the prediction module
import openai
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import os


# Load environment variables
load_environment_variables()

# Set OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("OpenAI API key is missing. Check your .env file or environment variables.")

# Streamlit App
st.title("Unified Resource Monitor")

# LLM Insights Section
st.header("LLM Insights")
prompt = st.text_area("Enter your LLM prompt:")
if st.button("Track LLM Usage"):
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

# Cost Alerts Section
st.sidebar.header("Cost Alerts")
llm_cost_threshold = st.sidebar.number_input("LLM Daily Cost Threshold ($)", min_value=0.0, value=10.0, step=0.1)
aws_cost_threshold = st.sidebar.number_input("AWS Monthly Cost Threshold ($)", min_value=0.0, value=100.0, step=1.0)

# AWS Metrics Section (Below LLM Insights)
st.header("AWS Metrics")
region = os.getenv("AWS_REGION")
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")

if st.button("Fetch AWS Metrics"):
    metrics = fetch_aws_metrics(region, access_key, secret_key)
    if "error" in metrics:
        st.error(metrics["error"])
    else:
        if metrics:
            st.subheader("Fetched AWS Metrics")
            metrics_df = pd.DataFrame(metrics)
            st.write(metrics_df)
        else:
            st.write("No metrics available.")

# Historical Logs Section
st.sidebar.header("Historical Logs")
log_file_path = "llm_usage_logs.csv"
if st.sidebar.button("View Historical Logs"):
    display_historical_logs(log_file_path)

# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed by Spaire Team")
