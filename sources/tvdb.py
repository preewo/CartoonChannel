import os
import sources.authentication
import requests
import json
import re
from sources.config import QUERY_URL,JSON_SAVE_PATH
from sources.enums import SeriesResponseKeys as Series,EpisodeResponseKeys as Episodes


def clean_title(title):
    cleaned_title = re.sub(r"[&!,‘'`’?:]", '', title)
    cleaned_title = cleaned_title.replace('  ', ' ').replace(' ', '-')  # Replace spaces with dashes
    return cleaned_title.strip()


def get_tvdb_details(series_id):
    search_url = f"{QUERY_URL}{series_id}"
    headers = sources.authentication.authenticate()
    if headers == None:
        "Exiting..."
        return None
    response = requests.get(search_url, headers=headers, verify=False)

    if response.status_code == 200:
        series_data = response.json()['data']
        series_id = series_data[0]['id'].split("-")[-1]  # Assuming the first result is correct
        print(f"Series ID: {series_id}")
    else:
        print(f"Error: {response.status_code} - {response.text}")

    # Fetch series info
    series_url = f'https://api4.thetvdb.com/v4/series/{series_id}/extended?meta=translations'
    response = requests.get(series_url, headers=headers, verify=False)

    if response.status_code == 200:
        series_response = response.json()['data']

        series_title = series_response[Series.NAME.value]
        episodes_data = {
            "series_title": series_title,
            "series_id": series_id,
            "overview": series_response[Series.OVERVIEW.value],
            "status": series_response[Series.STATUS.value]['name'],
            "first_aired": series_response[Series.FIRST_AIRED.value],
            "last_aired": series_response[Series.LAST_AIRED.value],
            "original_country": series_response[Series.ORIGINAL_COUNTRY.value],
            "original_language": series_response[Series.ORIGINAL_LANGUAGE.value],
            "image": series_response[Series.IMAGE.value],
            "genre": [genre['name'] for genre in series_response[Series.GENRES.value]],
            "episodes": []
        }
    else:
        print(f"Error: {response.status_code} - {response.text}")

    # Fetch episodes for the series
    episodes_url = f'https://api4.thetvdb.com/v4/series/{series_id}/episodes/default'
    response = requests.get(episodes_url, headers=headers, verify=False)

    if response.status_code == 200:
        episodes = response.json()['data']['episodes']

        for episode in episodes:
            episode_data = {
                "season": episode[Episodes.SEASON_NUMBER.value],
                "episode_number": episode[Episodes.EPISODE_NUMBER.value],
                "title": episode[Episodes.TITLE.value],
                "description": episode.get(Episodes.OVERVIEW.value, 'No description available'),
                "aired": episode[Episodes.AIRED.value],
                "image": episode[Episodes.IMAGE.value],
                "video_link": [],
                "has_video_link": "No"
            }
            episodes_data["episodes"].append(episode_data)

        # Save the structured JSON to a file
        title = clean_title(series_title)
        file_path = f"{JSON_SAVE_PATH}{title}.json"

        # Check if the file already exists
        if os.path.exists(file_path):
            print(f"File '{file_path}' already exists. Skipping save to avoid overwrite.")
        else:
            # Save the structured JSON to a file
            with open(file_path, "w") as json_file:
                json.dump(episodes_data, json_file, indent=4)
            print(f"JSON data for episodes saved as '{file_path}'")
    else:
        print(f"Error: {response.status_code} - {response.text}")
