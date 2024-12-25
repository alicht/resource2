import os
import streamlit as st
from llm_insights import track_openai_usage
from aws_metrics import fetch_aws_metrics
from azure_metrics import fetch_azure_metrics
from gcp_metrics import fetch_gcp_metrics
from historical_logs import display_historical_logs
from utils import load_environment_variables
import openai

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

# Azure Metrics Section
st.sidebar.header("Azure Metrics")
if st.sidebar.button("Fetch Azure Metrics"):
    metrics = fetch_azure_metrics()
    if "error" in metrics:
        st.error(metrics["error"])
    else:
        st.subheader("Azure Metrics")
        st.write(metrics)

# GCP Metrics Section
st.sidebar.header("GCP Metrics")
if st.sidebar.button("Fetch GCP Metrics"):
    metrics = fetch_gcp_metrics()
    if "error" in metrics:
        st.error(metrics["error"])
    else:
        st.subheader("GCP Metrics")
        st.write(metrics)

# Historical Logs Section
st.sidebar.header("Historical Logs")
if st.sidebar.button("View Historical Logs"):
    display_historical_logs()
