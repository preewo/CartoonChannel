FILE_TO_CHECK= "../DB/json/The-Sylvester-Tweety-Mysteries.json"

import requests
import json

# Load the JSON data from a file (replace 'file.json' with your actual file path)
with open(FILE_TO_CHECK, 'r') as json_file:
    data = json.load(json_file)

# Function to check the status of each video URL
def check_video_links(episodes):
    for episode in episodes:
        for url in episode['video_link']:
            try:
                response = requests.head(url, timeout=5)  # Use HEAD to avoid downloading the content
                if response.status_code != 200:
                    print(f"URL {url} is valid (status code: {response.status_code}).")
            except requests.RequestException as e:
                print(f"Failed to check URL {url}. Error: {e}")

# Iterate through the episodes in the JSON data
if 'episodes' in data:
    check_video_links(data['episodes'])
else:
    print("No episodes found in the JSON data.")
