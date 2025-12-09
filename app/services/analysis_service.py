import numpy as np
import pandas as pd
from typing import Dict, List
from datetime import datetime


class AnalysisService:
    @staticmethod
    def calculate_statistics(metrics: List[Dict]) -> Dict:
        """
        Calculate statistical measures for resource usage
        """
        if not metrics:
            return {}

        df = pd.DataFrame(metrics)
        
        stats = {
            "cpu": {
                "mean": float(df["cpu_usage"].mean()) if "cpu_usage" in df else 0,
                "median": float(df["cpu_usage"].median()) if "cpu_usage" in df else 0,
                "std": float(df["cpu_usage"].std()) if "cpu_usage" in df else 0,
                "min": float(df["cpu_usage"].min()) if "cpu_usage" in df else 0,
                "max": float(df["cpu_usage"].max()) if "cpu_usage" in df else 0,
                "p95": float(df["cpu_usage"].quantile(0.95)) if "cpu_usage" in df else 0,
                "p99": float(df["cpu_usage"].quantile(0.99)) if "cpu_usage" in df else 0,
            },
            "memory": {
                "mean": float(df["memory_usage"].mean()) if "memory_usage" in df else 0,
                "median": float(df["memory_usage"].median()) if "memory_usage" in df else 0,
                "std": float(df["memory_usage"].std()) if "memory_usage" in df else 0,
                "min": float(df["memory_usage"].min()) if "memory_usage" in df else 0,
                "max": float(df["memory_usage"].max()) if "memory_usage" in df else 0,
                "p95": float(df["memory_usage"].quantile(0.95)) if "memory_usage" in df else 0,
                "p99": float(df["memory_usage"].quantile(0.99)) if "memory_usage" in df else 0,
            },
            "disk": {
                "mean": float(df["disk_usage"].mean()) if "disk_usage" in df else 0,
                "median": float(df["disk_usage"].median()) if "disk_usage" in df else 0,
                "std": float(df["disk_usage"].std()) if "disk_usage" in df else 0,
                "min": float(df["disk_usage"].min()) if "disk_usage" in df else 0,
                "max": float(df["disk_usage"].max()) if "disk_usage" in df else 0,
                "p95": float(df["disk_usage"].quantile(0.95)) if "disk_usage" in df else 0,
                "p99": float(df["disk_usage"].quantile(0.99)) if "disk_usage" in df else 0,
            },
            "total_samples": len(metrics),
        }
        
        return stats

    @staticmethod
    def calculate_resource_recommendations(stats: Dict) -> Dict:
        """
        Calculate recommended resources based on statistical analysis
        Uses p95 percentile with 20% buffer for safety
        """
        buffer_factor = 1.2
        
        recommendations = {
            "cpu": {
                "recommended_millicores": int(stats["cpu"]["p95"] * buffer_factor * 1000),
                "min_millicores": int(stats["cpu"]["mean"] * 1000),
                "max_observed_millicores": int(stats["cpu"]["max"] * 1000),
            },
            "memory": {
                "recommended_mb": int(stats["memory"]["p95"] * buffer_factor),
                "min_mb": int(stats["memory"]["mean"]),
                "max_observed_mb": int(stats["memory"]["max"]),
            },
            "disk": {
                "recommended_mb": int(stats["disk"]["p95"] * buffer_factor),
                "min_mb": int(stats["disk"]["mean"]),
                "max_observed_mb": int(stats["disk"]["max"]),
            }
        }
        
        return recommendations

    @staticmethod
    def generate_analysis_summary(stats: Dict, recommendations: Dict) -> str:
        """
        Generate a human-readable analysis summary
        """
        summary = f"""
Resource Analysis Summary:
==========================

CPU Usage:
- Average: {stats['cpu']['mean']:.2f}%
- Peak (99th percentile): {stats['cpu']['p99']:.2f}%
- Recommended CPU: {recommendations['cpu']['recommended_millicores']} millicores

Memory Usage:
- Average: {stats['memory']['mean']:.2f} MB
- Peak (99th percentile): {stats['memory']['p99']:.2f} MB
- Recommended Memory: {recommendations['memory']['recommended_mb']} MB

Disk Usage:
- Average: {stats['disk']['mean']:.2f} MB
- Peak (99th percentile): {stats['disk']['p99']:.2f} MB
- Recommended Disk: {recommendations['disk']['recommended_mb']} MB

Total Samples Analyzed: {stats['total_samples']}
"""
        return summary
