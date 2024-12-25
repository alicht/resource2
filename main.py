import streamlit as st
from llm_insights import track_openai_usage
from aws_metrics import fetch_aws_metrics
from historical_logs import display_historical_logs
from utils import load_environment_variables
import openai
import os

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
region = os.getenv("AWS_REGION")
access_key = os.getenv("AWS_ACCESS_KEY_ID")
secret_key = os.getenv("AWS_SECRET_ACCESS_KEY")
if st.sidebar.button("Fetch AWS Metrics"):
    metrics = fetch_aws_metrics(region, access_key, secret_key)
    if "error" in metrics:
        st.error(metrics["error"])
    else:
        st.write(metrics)

# Historical Logs Section
st.sidebar.header("Historical Logs")
log_file_path = "llm_usage_logs.csv"
if st.sidebar.button("View Historical Logs"):
    logs = display_historical_logs(log_file_path)
    if "error" in logs:
        st.error(logs["error"])
    else:
        st.write(logs["dataframe"])
        st.pyplot(logs["plot"])
        st.write(f"Predicted Total Tokens: {logs['predictions']['tokens']:.2f}")
        st.write(f"Predicted Cost: ${logs['predictions']['cost']:.4f}")
