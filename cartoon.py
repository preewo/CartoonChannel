import requests
import sources.tvdb as tvdb
import sources.config as config
import sources.authentication
import urllib.parse

# Function to search for series by name and return the series ID
def search_series(headers, series_name):
    url = f"{config.QUERY_URL}{urllib.parse.quote(series_name)}"
    response = requests.get(url, headers=headers,verify=True)

    if response.status_code == 200:
        search_results = response.json()["data"]

        # Print all matching series
        for idx, series in enumerate(search_results):
            if series['type'] == "series" or series['type'] == "movie":
                year = 'Undefined'
                if 'year' in series and series['year'] is not None:
                    year = series['year']
                print(f"{idx + 1}. {series['name']} ({year}) [{series['type'].title()}]")
            else:
                print(f"{idx + 1}. {series['name']} [{series['type'].title()}]")


        # Allow user to choose a series
        if len(search_results) > 0:
            choice = input("Select the series by number (or type 'q' to quit): ")
            if choice.lower() != 'q' and choice.isdigit():
                idx = int(choice) - 1
                return search_results[idx]['name'],search_results[idx]['id']
            else:
                print("Returning to Main Menu...")
                return None, None
        else:
            print("No results found.")
            return None,None
    else:
        print(f"Failed to search for series: {response.status_code} - {response.text}")
        return None,None


# Interactive shell to search for series and get the series ID
def list_episode_names(headers,series_id):
    print(series_id)
    #episodes_url = f'https://api4.thetvdb.com/v4/series/{series_id.split('-')[1]}/episodes/default'
    episodes_url = f'https://api4.thetvdb.com/v4/series/{series_id.split('-')[1]}/extended?meta=episodes'
    response = requests.get(episodes_url, headers=headers, verify=True)
    if response.status_code == 200:
        episodes = response.json()['data']['episodes']
        for episode in episodes:
            print(f"Season: {episode['seasonNumber']} Episodes: {episode['number']} Name: {episode['name']}")


def create_extended_json(series_id):
    tvdb.get_tvdb_details(series_id)
    pass


def interactive_shell():
    # Authenticate and get the token
    headers = sources.authentication.authenticate()


    while True:
        print("\nTVDB Interactive Shell")
        series_name = input("Enter the name of the series to search for (or type 'q' to quit): ")

        if series_name.lower() == 'q':
            print("Goodbye!")
            break

        title, series_id = search_series(headers, series_name)

        if series_id:
            print(f"\n\nYou have selected: {title}")
            while True:
                print("\nWhat would you like to do?")
                print("1. List episode names")
                print("2. Create new extended JSON format")

                choice = input("Enter the number of your choice (or type 'q' to quit): ")

                if choice.isdigit():
                    choice = int(choice)

                    if choice == 1:
                        list_episode_names(headers, series_id)
                    elif choice == 2:
                        create_extended_json(series_id)
                    else:
                        print("Invalid choice. Please select a number from the list.")
                elif choice == "q":
                    print("Backing...back!")
                    break
                else:
                    print("Invalid input. Please enter a valid number.")
# Run the interactive shell
interactive_shell()
