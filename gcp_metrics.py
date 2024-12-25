from google.cloud import monitoring_v3
import time

def fetch_gcp_metrics(project_id):
    """
    Fetches GCP metrics for virtual machines.
    :param project_id: GCP project ID.
    :return: A list of dictionaries containing GCP metrics.
    """
    try:
        client = monitoring_v3.MetricServiceClient()
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
