import json
import os
from sqlalchemy.orm import Session
from ..models import Series, Episode
from datetime import datetime

def load_json_to_db(json_path: str, db: Session):
    with open(json_path, 'r') as f:
        data = json.load(f)

    series = db.query(Series).filter(Series.series_id == data["series_id"]).first()
    if not series:
        file_date_modified=datetime.fromtimestamp(os.path.getmtime(json_path))
        file_name=os.path.basename(json_path)
        timestamp = os.path.getmtime(json_path)
        file_date_modified = datetime.fromtimestamp(timestamp)
        print(file_name)
        print(file_date_modified)
        series = Series(
            series_id=data["series_id"],
            series_title=data["series_title"],
            overview=data["overview"],
            status=data["status"],
            first_aired=data["first_aired"],
            last_aired=data["last_aired"],
            original_country=data["original_country"],
            original_language=data["original_language"],
            image=data["image"],
            genre=",".join(data["genre"]),
            file_name=json_path,
            file_date_modified=file_date_modified

        )
        db.add(series)
        db.commit()
        db.refresh(series)

    for ep in data["episodes"]:
        episode = db.query(Episode).filter(Episode.episode_id == ep["episode_id"]).first()
        if not episode:
            episode = Episode(
                series_id=series.id,
                season=ep["season"],
                episode_number=ep["episode_number"],
                title=ep["title"],
                description=ep["description"],
                aired=ep["aired"],
                image=ep["image"],
                video_link=",".join(ep["video_link"]),
                has_video_link=ep["has_video_link"],
                episode_id=ep["episode_id"],
                runtime=ep["runtime"]
            )
            db.add(episode)

    db.commit()

def load_all_json_to_db(db: Session):
    json_dir = "./database/cartoon_jsons"
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(json_dir, filename)
            load_json_to_db(json_path, db)


def update_fields_if_modified(series, data, db):
    updated = False

    # Check and update series fields if necessary
    if series.series_title != data["series_title"]:
        series.series_title = data["series_title"]
        updated = True
    if series.overview != data["overview"]:
        series.overview = data["overview"]
        updated = True
    if series.status != data["status"]:
        series.status = data["status"]
        updated = True
    if series.first_aired != data["first_aired"]:
        series.first_aired = data["first_aired"]
        updated = True
    if series.last_aired != data["last_aired"]:
        series.last_aired = data["last_aired"]
        updated = True
    if series.original_country != data["original_country"]:
        series.original_country = data["original_country"]
        updated = True
    if series.original_language != data["original_language"]:
        series.original_language = data["original_language"]
        updated = True
    if series.image != data["image"]:
        series.image = data["image"]
        updated = True
    if series.genre != ",".join(data["genre"]):
        series.genre = ",".join(data["genre"])
        updated = True

    return updated

def update_episodes_if_modified(series, episodes, db):
    updated = False

    for ep in episodes:
        # Find the episode in the database
        episode = db.query(Episode).filter(Episode.episode_id == ep["episode_id"]).first()

        if episode:
            # Check each field and update if necessary
            if episode.title != ep["title"]:
                episode.title = ep["title"]
                updated = True
            if episode.description != ep["description"]:
                episode.description = ep["description"]
                updated = True
            if episode.aired != ep["aired"]:
                episode.aired = ep["aired"]
                updated = True
            if episode.image != ep["image"]:
                episode.image = ep["image"]
                updated = True
            if episode.video_link != ",".join(ep["video_link"]):
                episode.video_link = ",".join(ep["video_link"])
                updated = True
            if episode.has_video_link != ep["has_video_link"]:
                episode.has_video_link = ep["has_video_link"]
                updated = True
            if episode.runtime != ep["runtime"]:
                episode.runtime = ep["runtime"]
                updated = True
        else:
            # Add the episode if it doesn't exist
            episode = Episode(
                series_id=series.id,
                season=ep["season"],
                episode_number=ep["episode_number"],
                title=ep["title"],
                description=ep["description"],
                aired=ep["aired"],
                image=ep["image"],
                video_link=",".join(ep["video_link"]),
                has_video_link=ep["has_video_link"],
                episode_id=ep["episode_id"],
                runtime=ep["runtime"]
            )
            db.add(episode)
            updated = True

    return updated


def update_file_in_db(json_path: str, db: Session):
    # Get the last modified timestamp of the file
    file_date_modified = datetime.fromtimestamp(os.path.getmtime(json_path))
    
    # Load JSON data
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    # Check if the series already exists in the database
    series = db.query(Series).filter(Series.series_id == data["series_id"]).first()
    
    if series:
        # Compare file date modified
        if series.file_date_modified < file_date_modified:
            print(f"File {json_path} has been modified. Updating DB.")
            
            # Update file_date_modified and fields if necessary
            series.file_date_modified = file_date_modified

            # Update all fields and episodes
            series_updated = update_fields_if_modified(series, data, db)
            episodes_updated = update_episodes_if_modified(series, data["episodes"], db)

            # Commit if any updates were made
            if series_updated or episodes_updated:
                db.commit()
                db.refresh(series)
            else:
                print(f"No changes detected in {json_path}.")
    else:
        # If the series doesn't exist, insert it as a new record
        print(f"File {json_path} not found in the database. Adding as a new entry.")
        load_json_to_db(json_path, db)


def update_all_files_in_db(db: Session):
    json_dir = "./database/cartoon_jsons"
    for filename in os.listdir(json_dir):
        if filename.endswith(".json"):
            json_path = os.path.join(json_dir, filename)
            update_file_in_db(json_path, db)
            update_episodes(json_path, db)


def update_episode_fields(db: Session, episode: Episode, ep_data: dict):
    """Update the fields of an episode if they have been changed."""
    updated = False

    if episode.season != ep_data["season"]:
        episode.season = ep_data["season"]
        updated = True

    if episode.episode_number != ep_data["episode_number"]:
        episode.episode_number = ep_data["episode_number"]
        updated = True

    if episode.title != ep_data["title"]:
        episode.title = ep_data["title"]
        updated = True

    if episode.description != ep_data.get("description"):
        episode.description = ep_data.get("description")
        updated = True

    if episode.aired != ep_data["aired"]:
        episode.aired = ep_data["aired"]
        updated = True

    if episode.image != ep_data.get("image"):
        episode.image = ep_data.get("image")
        updated = True

    # Check for changes in video links
    video_links_str = ",".join(ep_data["video_link"])
    if episode.video_link != video_links_str:
        episode.video_link = video_links_str
        updated = True

    if episode.has_video_link != ep_data["has_video_link"]:
        episode.has_video_link = ep_data["has_video_link"]
        updated = True

    if episode.episode_id != ep_data["episode_id"]:
        episode.episode_id = ep_data["episode_id"]
        updated = True

    if episode.runtime != ep_data["runtime"]:
        episode.runtime = ep_data["runtime"]
        updated = True

    return updated


def update_episodes(json_path: str, db: Session):
    with open(json_path, 'r') as f:
        data = json.load(f)

    series = db.query(Series).filter(Series.series_id == data["series_id"]).first()
    if not series:
        # Insert new series if it doesn't exist
        series = Series(
            series_id=data["series_id"],
            series_title=data["series_title"],
            overview=data["overview"],
            status=data["status"],
            first_aired=data["first_aired"],
            last_aired=data["last_aired"],
            original_country=data["original_country"],
            original_language=data["original_language"],
            image=data["image"],
            genre=",".join(data["genre"])
        )
        db.add(series)
        db.commit()
        db.refresh(series)

    for ep in data["episodes"]:
        episode = db.query(Episode).filter(Episode.episode_id == ep["episode_id"]).first()
        if not episode:
            # Insert new episode if it doesn't exist
            episode = Episode(
                series_id=series.id,
                season=ep["season"],
                episode_number=ep["episode_number"],
                title=ep["title"],
                description=ep["description"],
                aired=ep["aired"],
                image=ep["image"],
                video_link=",".join(ep["video_link"]),
                has_video_link=ep["has_video_link"],
                episode_id=ep["episode_id"],
                runtime=ep["runtime"]
            )
            db.add(episode)
        else:
            # Update episode fields if they have changed
            if update_episode_fields(db, episode, ep):
                db.add(episode)  # Add updated episode to session for commit

    db.commit()

