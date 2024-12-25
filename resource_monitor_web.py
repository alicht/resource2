import os
import time
import csv
import pandas as pd
import numpy as np
import streamlit as st
from dotenv import load_dotenv
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import openai
from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError
from google.cloud import monitoring_v3

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# AWS Credentials Setup
AWS_REGION = os.getenv("AWS_REGION")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")

# Azure credentials setup
credential = DefaultAzureCredential()
subscription_id = os.getenv("AZURE_SUBSCRIPTION_ID")
resource_group = os.getenv("AZURE_RESOURCE_GROUP")

# File paths
llm_log_file = "llm_usage_logs.csv"

# Ensure log file exists
if not os.path.exists(llm_log_file):
    with open(llm_log_file, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Timestamp", "Total Tokens", "Prompt Tokens", "Cost"])

# Function to fetch AWS metrics
def fetch_aws_metrics():
    try:
        ec2_client = boto3.client(
            "ec2",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )
        cloudwatch_client = boto3.client(
            "cloudwatch",
            region_name=AWS_REGION,
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        # Get list of instances
        instances = ec2_client.describe_instances()
        instance_metrics = []

        for reservation in instances["Reservations"]:
            for instance in reservation["Instances"]:
                instance_id = instance["InstanceId"]

                # Fetch CPU Utilization
                cpu_data = cloudwatch_client.get_metric_statistics(
                    Namespace="AWS/EC2",
                    MetricName="CPUUtilization",
                    Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                    StartTime=time.time() - 3600,
                    EndTime=time.time(),
                    Period=300,
                    Statistics=["Average"],
                )

                # Fetch Network In
                network_in_data = cloudwatch_client.get_metric_statistics(
                    Namespace="AWS/EC2",
                    MetricName="NetworkIn",
                    Dimensions=[{"Name": "InstanceId", "Value": instance_id}],
                    StartTime=time.time() - 3600,
                    EndTime=time.time(),
                    Period=300,
                    Statistics=["Average"],
                )

                instance_metrics.append({
                    "Instance ID": instance_id,
                    "CPU Utilization (%)": cpu_data["Datapoints"][0]["Average"] if cpu_data["Datapoints"] else "N/A",
                    "Network In (Bytes)": network_in_data["Datapoints"][0]["Average"] if network_in_data["Datapoints"] else "N/A"
                })

        return instance_metrics
    except NoCredentialsError:
        return {"error": "AWS credentials not found. Please check your environment variables or AWS configuration."}
    except PartialCredentialsError:
        return {"error": "Incomplete AWS credentials. Please verify your AWS access key and secret key."}
    except Exception as e:
        return {"error": str(e)}

# Function to fetch Azure resource metrics
def fetch_azure_metrics():
    try:
        monitor_client = MonitorManagementClient(credential, subscription_id)
        metrics_data = monitor_client.metrics.list(
            resource_id=f"/subscriptions/{subscription_id}/resourceGroups/{resource_group}/providers/Microsoft.Compute/virtualMachines/",
            timespan="PT1H",
            interval="PT1M",
            metricnames="Percentage CPU, Network In, Network Out",
            aggregation="Average"
        )

        metrics = {}
        for item in metrics_data.value:
            metrics[item.name.value] = [data.average for data in item.timeseries[0].data if data.average is not None]

        return metrics
    except Exception as e:
        return {"error": str(e)}

# Function to fetch GCP metrics
def fetch_gcp_metrics():
    try:
        client = monitoring_v3.MetricServiceClient()
        project_id = os.getenv("GCP_PROJECT_ID")
        project_name = f"projects/{project_id}"

        interval = monitoring_v3.TimeInterval()
        interval.end_time.seconds = int(time.time())
        interval.start_time.seconds = interval.end_time.seconds - 3600

        results = client.list_time_series(
            request={
                "name": project_name,
                "filter": 'metric.type = "compute.googleapis.com/instance/cpu/utilization"',
                "interval": interval,
                "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL
            }
        )

        gcp_metrics = []
        for result in results:
            gcp_metrics.append({
                "Instance": result.resource.labels["instance_id"],
                "CPU Utilization": [point.value.double_value for point in result.points]
            })

        return gcp_metrics
    except Exception as e:
        return {"error": str(e)}

# Streamlit App
st.title("Resource Monitor with AWS, Azure, and GCP Metrics")

# Sidebar for LLM Insights
st.sidebar.header("LLM Insights")
prompt = st.sidebar.text_area("Enter your LLM prompt:")
if st.sidebar.button("Track Usage"):
    if prompt:
        result = track_openai_usage(prompt)
        if "error" in result:
            st.error(result["error"])
        else:
            st.subheader("OpenAI API Response")
            st.write(result["response"])

            st.subheader("Usage Details")
            st.write(f"**Total Tokens Used:** {result['total_tokens']}")
            st.write(f"**Prompt Tokens:** {result['prompt_tokens']}")
            st.write(f"**Completion Tokens:** {result['completion_tokens']}")
            st.write(f"**Cost of Request:** ${result['cost']:.4f}")

# AWS Metrics Section
st.sidebar.header("AWS Metrics")
if st.sidebar.button("Fetch AWS Metrics"):
    metrics = fetch_aws_metrics()
    if isinstance(metrics, list):
        st.subheader("AWS Metrics")
        for metric in metrics:
            st.write(f"**Instance ID:** {metric['Instance ID']}")
            st.write(f"CPU Utilization: {metric['CPU Utilization (%)']}%")
            st.write(f"Network In: {metric['Network In (Bytes)']} Bytes")
            st.write("---")
        st.success("Fetched AWS metrics successfully.")
    else:
        st.error(metrics["error"])

# Azure Resource Metrics
st.sidebar.header("Azure Metrics")
if st.sidebar.button("Fetch Azure Metrics"):
    metrics = fetch_azure_metrics()
    if "error" in metrics:
        st.error(metrics["error"])
    else:
        st.subheader("Azure Resource Metrics")
        for key, values in metrics.items():
            st.write(f"**{key}:** {values}")
        st.success("Fetched Azure metrics successfully.")

# GCP Metrics Section
st.sidebar.header("GCP Metrics")
if st.sidebar.button("Fetch GCP Metrics"):
    metrics = fetch_gcp_metrics()
    if isinstance(metrics, list):
        st.subheader("GCP Metrics")
        for metric in metrics:
            st.write(f"**Instance ID:** {metric['Instance']}")
            st.write(f"CPU Utilization: {metric['CPU Utilization']}")
            st.write("---")
        st.success("Fetched GCP metrics successfully.")
    else:
        st.error(metrics["error"])

# Historical Logs and Trends
st.sidebar.header("Historical LLM Logs")
if st.sidebar.button("View Historical LLM Usage"):
    try:
        df = pd.read_csv(llm_log_file, header=0)

        # Display DataFrame
        st.subheader("Historical LLM Usage Logs")
        st.dataframe(df)

        # Visualize trends
        st.subheader("LLM Usage Trends")
        fig, ax = plt.subplots(1, 2, figsize=(12, 6))

        ax[0].plot(df["Total Tokens"], label="Total Tokens", marker="o")
        ax[0].set_title("Token Usage Over Time")
        ax[0].set_xlabel("Requests")
        ax[0].set_ylabel("Tokens")
        ax[0].legend()

        ax[1].plot(df["Cost"], label="Cost", color="red
