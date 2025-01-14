from sqlalchemy.orm import Session
from .models import Series

def get_series_by_id(db: Session, series_id: str):
    return db.query(Series).filter(Series.series_id == series_id).first()
