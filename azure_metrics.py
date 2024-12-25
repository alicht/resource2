from azure.identity import DefaultAzureCredential
from azure.mgmt.monitor import MonitorManagementClient

def fetch_azure_metrics(subscription_id, resource_group):
    """
    Fetches Azure resource metrics such as CPU and Network utilization.
    :param subscription_id: Azure subscription ID.
    :param resource_group: Azure resource group name.
    :return: A dictionary with Azure resource metrics.
    """
    try:
        credential = DefaultAzureCredential()
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
