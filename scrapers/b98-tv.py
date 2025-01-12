#### This scraper is almost finished , problems with titlecase's in url.
#### Had to modify Video URL's manually

import re
import requests
import json
from bs4 import BeautifulSoup
from titlecase import titlecase

MAIN_TITLE = "The Sylvester & Tweety Mysteries"

MAIN_URL = 'https://www.b98.tv/videos_categories/series'
SERIES_URL = 'https://www.b98.tv/videos_categories'
JSON_FILE = '../DB/json/'


def clean_title(title):
    # Define a regular expression pattern to remove unwanted characters
    cleaned_title = re.sub(r"[&!,‘'`’?:]", '', title)  # Remove &, !, ‘, ', :, and `
    cleaned_title = cleaned_title.replace('  ', ' ').replace(' ','-')  # Remove any double spaces caused by symbol removal
    return cleaned_title.strip()


# Function to get the last page number from the pagination
def get_last_page_number(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the last page number from the pagination
    pagination = soup.find('ul', class_='page-numbers')
    if not pagination:
        return 1
    page_numbers = pagination.find_all('a', class_='page-numbers')

    # Get the last page number
    last_page_number = int(page_numbers[-2].text)  # The second-to-last item is the last page number
    return last_page_number


# Function to get video titles from a specific page
def get_video_titles_from_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract all video titles (assuming they are in h3 elements with class 'title')
    titles = soup.find_all('h3', class_='title')
    video_titles = [title.get_text(strip=True) for title in titles]

    return video_titles

# Function to get all video titles from all pages
def get_all_video_titles(base_url):
    last_page_number = get_last_page_number(base_url)
    all_video_titles = []

    for page_number in range(1, last_page_number + 1):
        page_url = f"{base_url}/page/{page_number}/" if page_number > 1 else base_url
        print(f"Scraping page {page_number}...")

        # Get video titles from the current page
        video_titles = get_video_titles_from_page(page_url)
        all_video_titles.extend(video_titles)

    return all_video_titles


def update_video_links(episodes_data, video_titles, main_title):
    for episode in episodes_data["episodes"]:
        for video_title in video_titles:
            # For easier debugging purposes ->
            first = clean_title(episode['title']).lower()
            second = clean_title(video_title).lower()
            if first in second:
                cleaned_video_title = clean_title(video_title)
                #video_url = f"https://ww.b98.tv/video/{main_title}-{cleaned_video_title.title().replace(' ', '-').replace("-Of-","-of-").replace("-To-","-to-").replace("-The-","-the-").replace("-For-","-for-").replace("-Is-","-is-").replace("-A-","-a-").replace("-And-","-and-").replace("-As-","-as-")}.mp4"
                video_url = f"https://ww.b98.tv/video/{main_title}-{titlecase(cleaned_video_title.title().replace(' ', '-'))}.mp4"
                if video_url not in episode['video_link']:
                    episode['video_link'].append(video_url)
                    episode['has_video_link'] = 'Yes'
    return episodes_data

print(MAIN_TITLE)
cleaned_main_title = clean_title(MAIN_TITLE)
url = f"{SERIES_URL}/{clean_title(MAIN_TITLE)}"
print(url)

all_episode_titles = get_all_video_titles(url)

print(all_episode_titles)

with open(f"{JSON_FILE}{cleaned_main_title}.json", "r") as json_file:
    episodes_data = json.load(json_file)
# Update the episodes data with video links
updated_episodes_data = update_video_links(episodes_data, all_episode_titles, cleaned_main_title)

# Save the updated episodes data to a new JSON file
with open(f"{JSON_FILE}{cleaned_main_title}.json", "w") as json_file:
    json.dump(updated_episodes_data, json_file, indent=4)

print(f"Updated JSON data saved as '{cleaned_main_title}.json'")
