from typing import Dict, Optional
import os
import logging

logger = logging.getLogger(__name__)


class AIService:
    def __init__(self, model: str = "gpt-3.5-turbo", temperature: float = 0.7, max_tokens: int = 1000):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.api_key = os.getenv("OPENAI_API_KEY")

    def generate_recommendations(
        self,
        stats: Dict,
        recommendations: Dict,
        app_name: str,
        namespace: str
    ) -> str:
        """
        Generate AI-powered recommendations for Kubernetes pod configuration
        """
        # If OpenAI API key is not set, return rule-based recommendations
        if not self.api_key:
            return self._generate_rule_based_recommendations(stats, recommendations, app_name, namespace)
        
        try:
            from openai import OpenAI
            client = OpenAI(api_key=self.api_key)
            
            prompt = self._create_prompt(stats, recommendations, app_name, namespace)
            
            response = client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a Kubernetes resource optimization expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return self._generate_rule_based_recommendations(stats, recommendations, app_name, namespace)

    def _create_prompt(self, stats: Dict, recommendations: Dict, app_name: str, namespace: str) -> str:
        """
        Create a detailed prompt for the AI model
        """
        prompt = f"""
Analyze the following Kubernetes pod resource usage data and provide optimization recommendations:

Application: {app_name}
Namespace: {namespace}

CPU Usage Statistics:
- Average: {stats['cpu']['mean']:.2f}%
- Median: {stats['cpu']['median']:.2f}%
- 95th Percentile: {stats['cpu']['p95']:.2f}%
- 99th Percentile: {stats['cpu']['p99']:.2f}%
- Max: {stats['cpu']['max']:.2f}%
- Standard Deviation: {stats['cpu']['std']:.2f}%

Memory Usage Statistics (MB):
- Average: {stats['memory']['mean']:.2f} MB
- Median: {stats['memory']['median']:.2f} MB
- 95th Percentile: {stats['memory']['p95']:.2f} MB
- 99th Percentile: {stats['memory']['p99']:.2f} MB
- Max: {stats['memory']['max']:.2f} MB
- Standard Deviation: {stats['memory']['std']:.2f} MB

Disk Usage Statistics (MB):
- Average: {stats['disk']['mean']:.2f} MB
- Median: {stats['disk']['median']:.2f} MB
- 95th Percentile: {stats['disk']['p95']:.2f} MB
- 99th Percentile: {stats['disk']['p99']:.2f} MB
- Max: {stats['disk']['max']:.2f} MB
- Standard Deviation: {stats['disk']['std']:.2f} MB

Calculated Recommendations:
- CPU: {recommendations['cpu']['recommended_millicores']} millicores
- Memory: {recommendations['memory']['recommended_mb']} MB
- Disk: {recommendations['disk']['recommended_mb']} MB

Please provide:
1. An analysis of the resource usage patterns
2. Specific recommendations for CPU requests and limits
3. Specific recommendations for memory requests and limits
4. Recommendations for storage provisioning
5. Any potential optimization strategies
6. Warnings about any concerning patterns (e.g., high variance, spikes)
"""
        return prompt

    def _generate_rule_based_recommendations(
        self,
        stats: Dict,
        recommendations: Dict,
        app_name: str,
        namespace: str
    ) -> str:
        """
        Generate rule-based recommendations when AI is not available
        """
        cpu_variance = stats['cpu']['std'] / stats['cpu']['mean'] if stats['cpu']['mean'] > 0 else 0
        mem_variance = stats['memory']['std'] / stats['memory']['mean'] if stats['memory']['mean'] > 0 else 0
        
        recommendations_text = f"""
AI-Powered Recommendations for {app_name} in {namespace}:

RESOURCE CONFIGURATION:
======================
CPU Configuration:
- Request: {recommendations['cpu']['min_millicores']}m (based on average usage)
- Limit: {recommendations['cpu']['recommended_millicores']}m (based on p95 + 20% buffer)

Memory Configuration:
- Request: {recommendations['memory']['min_mb']}Mi (based on average usage)
- Limit: {recommendations['memory']['recommended_mb']}Mi (based on p95 + 20% buffer)

Storage Configuration:
- Recommended PV Size: {recommendations['disk']['recommended_mb']}Mi

ANALYSIS:
=========
"""
        
        # Add CPU analysis
        if cpu_variance > 0.5:
            recommendations_text += f"""
⚠️  HIGH CPU VARIANCE DETECTED (CV: {cpu_variance:.2f})
- Your CPU usage shows high variability, consider:
  * Implementing horizontal pod autoscaling (HPA)
  * Setting limits higher than requests for burst capacity
  * Investigating causes of CPU spikes
"""
        else:
            recommendations_text += f"""
✓ CPU usage is relatively stable (CV: {cpu_variance:.2f})
- Current configuration should work well
- Consider minor adjustments based on observed patterns
"""
        
        # Add memory analysis
        if mem_variance > 0.5:
            recommendations_text += f"""
⚠️  HIGH MEMORY VARIANCE DETECTED (CV: {mem_variance:.2f})
- Your memory usage shows high variability, consider:
  * Investigating memory leaks
  * Reviewing application memory management
  * Setting appropriate memory limits to prevent OOM
"""
        else:
            recommendations_text += f"""
✓ Memory usage is relatively stable (CV: {mem_variance:.2f})
- Current configuration should work well
"""
        
        # Add optimization tips
        recommendations_text += """

KUBERNETES YAML EXAMPLE:
=======================
resources:
  requests:
    cpu: {cpu_request}m
    memory: {mem_request}Mi
  limits:
    cpu: {cpu_limit}m
    memory: {mem_limit}Mi

ADDITIONAL RECOMMENDATIONS:
===========================
1. Monitor these metrics continuously using Grafana
2. Adjust limits based on actual production load
3. Consider implementing Quality of Service (QoS) classes
4. Use resource quotas at namespace level for better control
5. Implement pod disruption budgets for high availability

Note: These recommendations are based on mathematical analysis. For AI-powered insights, 
please configure your OpenAI API key.
""".format(
            cpu_request=recommendations['cpu']['min_millicores'],
            mem_request=recommendations['memory']['min_mb'],
            cpu_limit=recommendations['cpu']['recommended_millicores'],
            mem_limit=recommendations['memory']['recommended_mb']
        )
        
        return recommendations_text
