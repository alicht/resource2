import streamlit as st
from llm_insights import track_openai_usage
from aws_metrics import fetch_aws_metrics
from historical_logs import display_historical_logs
from utils import load_environment_variables
import openai
import pandas as pd
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import numpy as np
import os
from recommendations import generate_cost_saving_recommendations


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

# Sidebar: Cost Alerts and Recommendations
st.sidebar.header("Cost Alerts")
llm_cost_threshold = st.sidebar.number_input("LLM Daily Cost Threshold ($)", min_value=0.0, value=10.0, step=0.1)
aws_cost_threshold = st.sidebar.number_input("AWS Monthly Cost Threshold ($)", min_value=0.0, value=100.0, step=1.0)
st.sidebar.write("Configure cost thresholds to receive alerts when usage exceeds defined limits.")
recipient_email = st.sidebar.text_input("Notification Email (optional):")

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
        st.subheader("AWS Metrics")
        st.write(metrics)

# Historical Logs Section
st.sidebar.header("Historical Logs")
log_file_path = "llm_usage_logs.csv"
if st.sidebar.button("View Historical Logs"):
    try:
        result = display_historical_logs(log_file_path)

        if "error" in result:
            st.error(result["error"])
        else:
            df = result["dataframe"]
            st.subheader("Historical LLM Usage Logs and Predictions")
            st.pyplot(result["plot"])

            st.write("## Predictions")
            st.write(f"Predicted Total Tokens for Tomorrow: {result['predictions']['tokens']:.2f}")
            st.write(f"Predicted Cost for Tomorrow: ${result['predictions']['cost']:.4f}")

            # Threshold Monitoring Logic
            exceeded_thresholds = []

            # LLM Daily Cost Monitoring
            daily_llm_cost = df[df["Timestamp"].dt.date == pd.Timestamp.now().date()]["Cost"].sum()
            if daily_llm_cost > llm_cost_threshold:
                exceeded_thresholds.append(f"LLM daily cost exceeded: ${daily_llm_cost:.2f} (Threshold: ${llm_cost_threshold:.2f})")

            # AWS Monthly Cost Monitoring
            aws_monthly_cost = 50.0  # Example value, replace with dynamic data
            if aws_monthly_cost > aws_cost_threshold:
                exceeded_thresholds.append(f"AWS monthly cost exceeded: ${aws_monthly_cost:.2f} (Threshold: ${aws_cost_threshold:.2f})")

            # Display Alerts
            if exceeded_thresholds:
                st.warning("⚠️ **Cost Threshold Alerts:**")
                for alert in exceeded_thresholds:
                    st.write(alert)

                # Send Email Notifications
                if recipient_email:
                    email_subject = "Resource Monitor: Cost Threshold Breached"
                    email_body = "\n".join(exceeded_thresholds)
                    email_status = send_email_notification(email_subject, email_body, recipient_email)
                    if isinstance(email_status, int) and email_status == 202:
                        st.success("📧 Email notification sent successfully.")
                    else:
                        st.error(f"Failed to send email: {email_status}")
            else:
                st.success("✅ No cost thresholds exceeded.")

    except Exception as e:
        st.error(f"Error loading historical data: {e}")

        # Historical Logs Section
st.sidebar.header("Historical Logs2")
log_file_path = "llm_usage_logs.csv"
if st.sidebar.button("View Historical Logs2"):
    try:
        df = pd.read_csv(log_file_path)
        st.subheader("Historical LLM Usage Logs and Recommendations")

        if not all(col in df.columns for col in ["Timestamp", "Model", "Total Tokens", "Cost", "Prompt"]):
            st.error("The required columns 'Timestamp', 'Model', 'Total Tokens', 'Cost', and 'Prompt' are missing from the log file.")
        else:
            # Generate recommendations
            recommendations = generate_cost_saving_recommendations(df)

            # Display recommendations
            st.write("### Cost-Saving Recommendations")
            if recommendations:
                for rec in recommendations:
                    st.info(f"💡 {rec}")
            else:
                st.success("No cost-saving recommendations at this time.")
    except Exception as e:
        st.error(f"Error loading historical data: {e}")


# Footer
st.sidebar.markdown("---")
st.sidebar.write("Developed by Spaire Team")