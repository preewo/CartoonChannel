import os
import subprocess
import tempfile
from threading import Thread
from typing import List
from fastapi import FastAPI, HTTPException, Request, Query, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import math
from fastapi.responses import HTMLResponse
from sqlalchemy import and_
from database import models
from database.database import SessionLocal, engine, Session
from database.migrations import migrate_json
from pydantic import BaseModel

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.on_event("startup")
async def startup_event():
    db = next(get_db())
    # This is where we load JSON data to the database on startup
    migrate_json.load_all_json_to_db(db)
    migrate_json.update_all_files_in_db(db)


app.mount("/static", StaticFiles(directory="static"), name="static")
CARTOON_FOLDER = "./DB/cartoon_jsons"
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def get_series(request: Request, param: str = None, page: int = Query(1, ge=1), page_size: int = Query(12, ge=1), db: Session = Depends(get_db)):
    alphabet = [chr(i) for i in range(ord('A'), ord('Z') + 1)]  # List of A-Z

    query = db.query(models.Series)

    if param:
        # Filter series by the first letter of the series_title
        query = query.filter(models.Series.series_title.ilike(f"{param}%"))

    # Count the total series
    total_series = query.count()

    # Apply pagination
    series = query.order_by(models.Series.series_title)\
                  .offset((page - 1) * page_size)\
                  .limit(page_size)\
                  .all()

    # Convert series data to a dictionary to pass to the template
    series_data = [{
        "file_name": f"{ser.series_title}.json",  # Optional if you want to keep this field
        "series_title": ser.series_title,
        "series_id": ser.series_id,
        "series_image": ser.image,
        "genre": ser.genre
    } for ser in series]

    # Calculate total pages for pagination
    total_pages = math.ceil(total_series / page_size)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "series": series_data,
        "page": page,
        "total_pages": total_pages,
        "alphabet": alphabet
    })

# Helper function to convert SQLAlchemy objects to dictionaries
def episode_to_dict(episode):
    return {
        "episode_id": episode.episode_id,
        "title": episode.title,
        "season": episode.season,
        "episode_number": episode.episode_number,
        "description": episode.description,
        "aired": episode.aired,
        "image": episode.image,
        "video_link": episode.video_link,
        "has_video_link": episode.has_video_link,
        "runtime": episode.runtime
    }


@app.get("/series/{id}", response_class=HTMLResponse)
async def read_episodes(request: Request, id: int, page: int = Query(1, ge=1), page_size: int = Query(12, ge=1), db: Session = Depends(get_db)):
    # Get series data from the database
    series = db.query(models.Series).filter(models.Series.series_id == id).first()

    if not series:
        return HTMLResponse(content="Series not found", status_code=404)

    # Query episodes for the series, filtering for those that have video links
    episodes_query = db.query(models.Episode).filter(
        and_(
            models.Episode.series_id == series.id,
            models.Episode.has_video_link == "Yes"
        )
    )

    # Sort episodes by season and episode_number
    episodes = episodes_query.order_by(models.Episode.season, models.Episode.episode_number).all()
    episodes_data = [episode_to_dict(episode) for episode in episodes]

    # Pagination logic
    total_episodes = len(episodes_data)
    start = (page - 1) * page_size
    end = start + page_size
    paginated_episodes = episodes_data[start:end]
    
    # Calculate total pages
    total_pages = math.ceil(total_episodes / page_size)

    return templates.TemplateResponse("index.html", {
        "request": request,
        "series_data": series,
        "series_id": id,
        "episodes": paginated_episodes,
        "page": page,
        "total_pages": total_pages,
    })

class Episode(BaseModel):
    title: str
    season: int
    episodeNumber: int
    runtime: int
    videoLink: str
    imgSrc: str
    episodeId: str

class Schedule(BaseModel):
    episodes: List[Episode]


def run_ffmpeg_in_background(video_links: List[str]):
    playlist_file_path = "playlist.txt"
    
    with open(playlist_file_path, 'w') as playlist_file:
        for link in video_links:
            playlist_file.write(f"file '{link}'\n")

    ffmpeg_command = [
        'ffmpeg', '-f', 'concat', '-safe', '0', '-re', '-protocol_whitelist', 'file,http,https,tcp,tls', '-i', f'{playlist_file_path}',
        '-c:v', 'libx264', '-maxrate', '600k' , '-bufsize', '800k', '-f', 'flv', 'rtmp://localhost/live/stream_key'
    ]
    print(" ".join(ffmpeg_command))
    subprocess.Popen(ffmpeg_command)


@app.post("/api/save-schedule")
async def save_schedule(schedule: Schedule):
    video_links = [episode.videoLink for episode in schedule.episodes]

    if not video_links:
        raise HTTPException(status_code=400, detail="No video links found in the schedule.")

    thread = Thread(target=run_ffmpeg_in_background, args=(video_links,))
    thread.start()

    return {"message": "Streaming started successfully in the background."}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)