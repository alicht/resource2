from google.cloud import monitoring_v3

def fetch_gcp_metrics(project_id):
    try:
        client = monitoring_v3.MetricServiceClient()
        project_name = f"projects/{project_id}"

        # Fetch metric descriptors
        metric_descriptors = list(client.list_metric_descriptors(name=project_name))
        metrics_data = []

        for descriptor in metric_descriptors[:5]:  # Limit to 5 metrics for simplicity
            # Query metric data
            interval = monitoring_v3.TimeInterval(
                {
                    "end_time": {"seconds": int(time.time())},
                    "start_time": {"seconds": int(time.time()) - 3600},  # Last hour
                }
            )
            results = client.list_time_series(
                request={
                    "name": project_name,
                    "filter": f'metric.type = "{descriptor.type}"',
                    "interval": interval,
                    "view": monitoring_v3.ListTimeSeriesRequest.TimeSeriesView.FULL,
                }
            )

            for metric in results:
                # Safeguard against None values
                end_time = metric.points[0].interval.end_time if metric.points else None
                start_time = metric.points[0].interval.start_time if metric.points else None

                if end_time and start_time:
                    time_difference = end_time - start_time
                    duration = time_difference.seconds  # Safeguard here
                else:
                    duration = "N/A"  # Assign a fallback value if data is missing

                metrics_data.append({
                    "metric_name": descriptor.type,
                    "description": descriptor.description,
                    "duration": duration
                })

        return metrics_data
    except Exception as e:
        return {"error": str(e)}
