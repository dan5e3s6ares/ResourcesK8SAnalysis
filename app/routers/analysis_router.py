from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.database import get_db
from app.models import models, schemas
from app.routers.auth_router import get_current_user
from app.services import ElasticsearchService, AnalysisService, AIService

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/run", response_model=schemas.AnalysisResult)
def run_analysis(
    request: schemas.AnalysisRequest,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Get configuration
    config = db.query(models.Configuration).filter(
        models.Configuration.id == request.configuration_id,
        models.Configuration.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    try:
        # Initialize Elasticsearch service
        es_service = ElasticsearchService(
            es_url=config.elasticsearch_url,
            index=config.elasticsearch_index
        )
        
        # Parse time parameters
        start_time = None
        end_time = None
        if request.start_time:
            start_time = datetime.fromisoformat(request.start_time)
        if request.end_time:
            end_time = datetime.fromisoformat(request.end_time)
        
        # Query metrics from Elasticsearch
        metrics = es_service.query_metrics(
            app_name=config.app_name,
            namespace=config.namespace,
            start_time=start_time,
            end_time=end_time,
            hours=config.analysis_window_hours
        )
        
        if not metrics:
            raise HTTPException(
                status_code=404,
                detail="No metrics found for the specified criteria"
            )
        
        # Perform statistical analysis
        analysis_service = AnalysisService()
        stats = analysis_service.calculate_statistics(metrics)
        recommendations = analysis_service.calculate_resource_recommendations(stats)
        
        # Generate AI recommendations
        ai_service = AIService(
            model=config.ai_model,
            temperature=float(config.ai_temperature),
            max_tokens=int(config.ai_max_tokens)
        )
        ai_recommendations = ai_service.generate_recommendations(
            stats=stats,
            recommendations=recommendations,
            app_name=config.app_name,
            namespace=config.namespace
        )
        
        return {
            "configuration_id": config.id,
            "metrics": metrics[:100],  # Return first 100 samples to avoid large response
            "statistical_analysis": stats,
            "ai_recommendations": ai_recommendations,
            "recommended_resources": recommendations
        }
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error performing analysis: {str(e)}"
        )


@router.get("/test-connection/{config_id}")
def test_elasticsearch_connection(
    config_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    config = db.query(models.Configuration).filter(
        models.Configuration.id == config_id,
        models.Configuration.user_id == current_user.id
    ).first()
    
    if not config:
        raise HTTPException(status_code=404, detail="Configuration not found")
    
    try:
        es_service = ElasticsearchService(
            es_url=config.elasticsearch_url,
            index=config.elasticsearch_index
        )
        
        # Try to get a small sample
        stats = es_service.get_aggregated_stats(
            app_name=config.app_name,
            namespace=config.namespace,
            hours=1
        )
        
        return {
            "status": "connected",
            "message": "Successfully connected to Elasticsearch",
            "sample_data": stats
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to connect: {str(e)}"
        }
