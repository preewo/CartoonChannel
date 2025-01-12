import re
import requests
import json
from bs4 import BeautifulSoup
from sources.tvdb import get_tvdb_details
from titlecase import titlecase

MAIN_URL = 'https://www.b98.tv/videos_categories/series'
SERIES_URL = 'https://www.b98.tv/videos_categories'


def clean_title(title):
    # Define a regular expression pattern to remove unwanted characters
    cleaned_title = re.sub(r"[&!,‘'`’?:]", '', title)  # Remove &, !, ‘, ', :, and `
    cleaned_title = cleaned_title.replace('  ', ' ')  # Remove any double spaces caused by symbol removal
    return cleaned_title.strip()


def get_cartoon_titles(URL):
    response = requests.get(URL)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find all h3 elements with the class 'title'
    title_elements = soup.find_all('h3', class_='title')
    # Extract and clean the titles from the h3 elements
    titles = [clean_title(title.get_text(strip=True)) for title in title_elements]
    titles.remove('Merrie Melodies')
    print(titles)
    return titles

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
    # First, get the last page number
    last_page_number = get_last_page_number(base_url)
    all_video_titles = []

    # Iterate through each page and scrape the video titles
    for page_number in range(1, last_page_number + 1):
        page_url = f"{base_url}/page/{page_number}/" if page_number > 1 else base_url
        print(f"Scraping page {page_number}...")

        # Get video titles from the current page
        video_titles = get_video_titles_from_page(page_url)
        all_video_titles.extend(video_titles)

    return all_video_titles

# Function to update JSON with video links
def update_video_links(episodes_data, video_titles, main_title):
    for episode in episodes_data["episodes"]:
        for video_title in video_titles:
            if episode['title'] == video_title:
                cleaned_video_title = titlecase(clean_title(video_title))
                cleaned_main_title = clean_title(main_title)
                video_url = f"https://ww.b98.tv/video/{cleaned_main_title.replace(" ","-").replace("--","-")}-{cleaned_video_title.title().replace(' ', '-')}.mp4"
                episode['video_link'] = [video_url]
                episode['has_video_link'] = 'Yes'
    return episodes_data

all_cartoon_titles = get_cartoon_titles(MAIN_URL)
for main_title in all_cartoon_titles:
    print(main_title)
    # Get all video titles from all pages
    cleaned_title = clean_title(main_title).replace(' ', '-').replace("--","-").lower()
    get_tvdb_details(main_title,cleaned_title)
    url = F"{SERIES_URL}/{cleaned_title}"
    all_episode_titles = get_all_video_titles(url)

    with open(f"{cleaned_title}.json", "r") as json_file:
        episodes_data = json.load(json_file)
    # Update the episodes data with video links
    updated_episodes_data = update_video_links(episodes_data, all_episode_titles, main_title)

    # Save the updated episodes data to a new JSON file
    with open(f"{cleaned_title}.json", "w") as json_file:
        json.dump(updated_episodes_data, json_file, indent=4)

    print(f"Updated JSON data saved as '{cleaned_title}.json'")
