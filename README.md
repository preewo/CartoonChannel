# CartoonChannel

**CartoonChannel** is an open-source, interactive 
Python script that allows users to search for their favorite 
**cartoon series**, fetch detailed information from [thetvdb.com](https://thetvdb.com), 
and organize the data into a structured **JSON** database. 
This project aims to build a collaborative platform where users 
can **contribute** to a growing repository of cartoons and their 
public video links. The ultimate goal is to create a **community-powered** 
web-based streaming schedule, **free from ads and downloads**.

---

### 📚 Features
**1. Search for Cartoon Series** \
With CartoonChannel, users can search for any cartoon series using the interactive shell. The results are fetched from the TVDB API and displayed in a user-friendly format for easy selection.

**2. Select and List Episodes** \
Once a series is selected, users can list all available episodes, including the season number, episode number, and episode name, allowing easy navigation through the series.

**3. Automatic JSON Database Generation** \
After selecting a cartoon, CartoonChannel automatically generates a JSON database that stores the details of the selected series, such as the series name, ID, and episode list. This JSON file can be easily extended with more data, making it a valuable resource for future use.

**4. Contribute Public Video Links** \
Users can manually add video links for specific episodes to the JSON database. Alternatively, they can build their own web scrapers to automatically populate episode details with public links to video streams. By contributing to this effort, users help create a more complete and shareable cartoon database.

**5. Community Goal: Web-Based Schedule** \
The ultimate objective of this project is to develop a web-based schedule interface where users can drop in their favorite series and stream episodes directly from anywhere in the house. This feature will eliminate the need to visit ad-ridden websites or download episodes. Imagine being able to watch your favorite shows without interruptions, thanks to a community-driven effort!

---
### 🛠 How It Works
**1. Search for Series:** Users input the cartoon name they want to search for, and the script queries the TVDB API, returning a list of matching series.

**2. Select Series:** From the search results, the user selects the series they are interested in, and the script pulls details from the API.

**3. Generate JSON:** The series information (including episodes) is automatically stored in a JSON file for future use or to be shared.

**4. Add Video Links:** Users can manually contribute episode video links to the JSON file or develop a web scraper to automate this task.

**5. Collaborate:** By contributing more data, we build toward creating a fully functioning, ad-free streaming platform for cartoons.

---
### 🔑 Requirements
To use **CartoonChannel**, you will need:

- A free API key from [thetvdb.com](https://thetvdb.com). The script relies on this API to retrieve cartoon details.

---
### 🌟 Why Should You Contribute?
- **Ad-Free Streaming:** Help build a platform where you can watch cartoons without the hassle of intrusive ads.
- **No Downloads Needed:** Users will be able to stream episodes directly without needing to download any files.
- **Collaborative Database:** By contributing public video links and adding new series to the JSON database, you are participating in a growing community effort to organize cartoon data in one place.
- **Community-Powered:** The more people contribute, the richer the collection becomes—ultimately allowing us to provide a seamless viewing experience.

---
### 🚀 How to Get Started
1. **Clone the Repository:**

```bash  
git clone https://github.com/preewo/CartoonChannel.git
```

2. **Install Dependencies:** \
Ensure that you have Python installed, then install the necessary packages by running:

```bash 
pip3 install -r requirements.txt
```

3. **Set Up Your API Key:** \
Sign up for a free account at [thetvdb.com](https://thetvdb.com) and generate an API key.
Change the `API_KEY` value in the `config.py` file


4. **Run the Interactive Shell:** \
Run the script and start searching for your favorite cartoons by typing:

```bash
python3 cartoon.py
```

---
### 👥 Contributions Welcome
This project thrives on community collaboration. Whether you're a Python developer interested in adding features, a web scraper enthusiast looking to contribute public links, or simply a fan of cartoons who wants to organize your favorites—your help is invaluable!

Feel free to fork the repository, submit pull requests, or open issues for any bugs or feature requests.