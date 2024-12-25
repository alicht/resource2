import streamlit as st
from llm_insights import track_openai_usage
from aws_metrics import fetch_aws_metrics
from azure_metrics import fetch_azure_metrics
from gcp_metrics import fetch_gcp_metrics
from historical_logs import display_historical_logs

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
    # Fetch and display AWS metrics
    pass

# Azure Metrics Section
st.sidebar.header("Azure Metrics")
if st.sidebar.button("Fetch Azure Metrics"):
    # Fetch and display Azure metrics
    pass

# GCP Metrics Section
st.sidebar.header("GCP Metrics")
if st.sidebar.button("Fetch GCP Metrics"):
    # Fetch and display GCP metrics
    pass

# Historical Logs Section
st.sidebar.header("Historical Logs")
if st.sidebar.button("View Historical Logs"):
    display_historical_logs()
