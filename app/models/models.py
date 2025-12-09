from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    configurations = relationship("Configuration", back_populates="owner")


class Configuration(Base):
    __tablename__ = "configurations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    app_name = Column(String, nullable=False)
    namespace = Column(String, nullable=False)
    grafana_url = Column(String, nullable=False)
    grafana_bearer_token = Column(String, nullable=False)
    elasticsearch_url = Column(String, nullable=False)
    elasticsearch_index = Column(String, nullable=False)
    ai_model = Column(String, default="gpt-3.5-turbo")
    ai_temperature = Column(String, default="0.7")
    ai_max_tokens = Column(String, default="1000")
    analysis_window_hours = Column(Integer, default=24)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    owner = relationship("User", back_populates="configurations")
