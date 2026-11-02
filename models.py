from sqlalchemy import Column, Integer, String, Float, DateTime
from .database import Base
from datetime import datetime, timezone

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(String, primary_key=True, index=True) # E.g., 'POST123'
    user_id = Column(Integer) # In a real app this would be a ForeignKey
    platform = Column(String, index=True)
    post_date = Column(DateTime)
    post_time = Column(String)
    content_type = Column(String)
    content_category = Column(String)
    followers = Column(Integer, default=0)
    impressions = Column(Integer, default=0)
    reach = Column(Integer, default=0)
    views = Column(Integer, default=0)
    likes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    shares = Column(Integer, default=0)
    saves = Column(Integer, default=0)
    video_duration = Column(Float, default=0.0)
    caption_length = Column(Integer, default=0)
    hashtag_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class AnalyticsSummary(Base):
    __tablename__ = "analytics_summary"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime)
    platform = Column(String)
    total_posts = Column(Integer)
    total_engagement = Column(Integer)
    average_engagement_rate = Column(Float)
    total_reach = Column(Integer)
    total_views = Column(Integer)

class Prediction(Base):
    __tablename__ = "predictions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer)
    input_features = Column(String) # Stored as JSON string
    predicted_engagement = Column(Float)
    model_name = Column(String)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
