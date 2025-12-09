from elasticsearch import Elasticsearch
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import pandas as pd
import logging

logger = logging.getLogger(__name__)


class ElasticsearchService:
    def __init__(self, es_url: str, index: str):
        self.client = Elasticsearch([es_url])
        self.index = index

    def query_metrics(
        self,
        app_name: str,
        namespace: str,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        hours: int = 24
    ) -> List[Dict]:
        """
        Query Elasticsearch for resource metrics
        """
        if not end_time:
            end_time = datetime.utcnow()
        if not start_time:
            start_time = end_time - timedelta(hours=hours)

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"app_name": app_name}},
                        {"match": {"namespace": namespace}},
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": start_time.isoformat(),
                                    "lte": end_time.isoformat()
                                }
                            }
                        }
                    ]
                }
            },
            "sort": [{"@timestamp": {"order": "asc"}}],
            "size": 10000
        }

        try:
            response = self.client.search(index=self.index, body=query)
            hits = response["hits"]["hits"]
            
            metrics = []
            for hit in hits:
                source = hit["_source"]
                metrics.append({
                    "timestamp": source.get("@timestamp"),
                    "cpu_usage": source.get("cpu_usage_percent", 0),
                    "memory_usage": source.get("memory_usage_mb", 0),
                    "disk_usage": source.get("disk_usage_mb", 0),
                    "cpu_cores": source.get("cpu_cores", 1),
                    "memory_total": source.get("memory_total_mb", 0),
                    "disk_total": source.get("disk_total_mb", 0),
                })
            
            return metrics
        except Exception as e:
            logger.error(f"Error querying Elasticsearch: {e}")
            return []

    def get_aggregated_stats(
        self,
        app_name: str,
        namespace: str,
        hours: int = 24
    ) -> Dict:
        """
        Get aggregated statistics for the specified time period
        """
        end_time = datetime.utcnow()
        start_time = end_time - timedelta(hours=hours)

        query = {
            "query": {
                "bool": {
                    "must": [
                        {"match": {"app_name": app_name}},
                        {"match": {"namespace": namespace}},
                        {
                            "range": {
                                "@timestamp": {
                                    "gte": start_time.isoformat(),
                                    "lte": end_time.isoformat()
                                }
                            }
                        }
                    ]
                }
            },
            "aggs": {
                "cpu_stats": {
                    "stats": {"field": "cpu_usage_percent"}
                },
                "memory_stats": {
                    "stats": {"field": "memory_usage_mb"}
                },
                "disk_stats": {
                    "stats": {"field": "disk_usage_mb"}
                }
            }
        }

        try:
            response = self.client.search(index=self.index, body=query)
            aggs = response.get("aggregations", {})
            
            return {
                "cpu": aggs.get("cpu_stats", {}),
                "memory": aggs.get("memory_stats", {}),
                "disk": aggs.get("disk_stats", {})
            }
        except Exception as e:
            logger.error(f"Error getting aggregated stats: {e}")
            return {}
