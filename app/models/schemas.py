from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    username: str
    password: str


class User(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class ConfigurationBase(BaseModel):
    app_name: str
    namespace: str
    grafana_url: str
    grafana_bearer_token: str
    elasticsearch_url: str
    elasticsearch_index: str
    ai_model: str = "gpt-3.5-turbo"
    ai_temperature: str = "0.7"
    ai_max_tokens: str = "1000"
    analysis_window_hours: int = 24


class ConfigurationCreate(ConfigurationBase):
    pass


class ConfigurationUpdate(BaseModel):
    app_name: Optional[str] = None
    namespace: Optional[str] = None
    grafana_url: Optional[str] = None
    grafana_bearer_token: Optional[str] = None
    elasticsearch_url: Optional[str] = None
    elasticsearch_index: Optional[str] = None
    ai_model: Optional[str] = None
    ai_temperature: Optional[str] = None
    ai_max_tokens: Optional[str] = None
    analysis_window_hours: Optional[int] = None


class Configuration(ConfigurationBase):
    id: int
    user_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class AnalysisRequest(BaseModel):
    configuration_id: int
    start_time: Optional[str] = None
    end_time: Optional[str] = None


class ResourceMetrics(BaseModel):
    timestamp: datetime
    cpu_usage: float
    memory_usage: float
    disk_usage: float


class AnalysisResult(BaseModel):
    configuration_id: int
    metrics: list
    statistical_analysis: dict
    ai_recommendations: str
    recommended_resources: dict
