from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class Series(Base):
    __tablename__ = 'series'
    
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(String, unique=True, index=True)
    series_title = Column(String)
    overview = Column(Text)
    status = Column(String)
    first_aired = Column(String)
    last_aired = Column(String)
    original_country = Column(String)
    original_language = Column(String)
    image = Column(String)
    genre = Column(String)
    file_name = Column(String)
    file_date_modified = Column(DateTime, default=datetime.utcnow)
    
    episodes = relationship("Episode", back_populates="series")

class Episode(Base):
    __tablename__ = 'episodes'
    
    id = Column(Integer, primary_key=True, index=True)
    series_id = Column(Integer, ForeignKey('series.id'))
    season = Column(Integer)
    episode_number = Column(Integer)
    title = Column(String)
    description = Column(Text)
    aired = Column(String)
    image = Column(String)
    video_link = Column(Text)
    has_video_link = Column(String)
    episode_id = Column(Integer)
    runtime = Column(Integer)

    series = relationship("Series", back_populates="episodes")
