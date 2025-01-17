// Function to load schedule from localStorage
function loadSchedule() {
    const storedSchedule = localStorage.getItem('schedule');
    if (storedSchedule) {
        const episodes = JSON.parse(storedSchedule);
        episodes.forEach(episode => {
            addEpisodeToSchedule(episode.title, episode.season, episode.episodeNumber, episode.runtime, episode.videoLink, episode.imgSrc, episode.episodeId);
        });
    }
}

// Function to save schedule to localStorage
function saveToSchedule(title, season, episodeNumber, runtime, videoLink, imgSrc, episodeId) {
    const storedSchedule = localStorage.getItem('schedule');
    let episodes = [];
    if (storedSchedule) {
        episodes = JSON.parse(storedSchedule);
    }

    // Add new episode
    episodes.push({ title, season, episodeNumber, runtime, videoLink, imgSrc, episodeId });

    // Save updated schedule to localStorage
    localStorage.setItem('schedule', JSON.stringify(episodes));
}


function sendScheduleToAPI() {
    const storedSchedule = localStorage.getItem('schedule');
    if (storedSchedule) {
        const episodes = JSON.parse(storedSchedule);

        fetch('/api/save-schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ episodes: episodes })
        })
        .then(response => response.json())
        .then(data => {
            console.log('Schedule saved successfully:', data);
            alert('Schedule saved to server!');
        })
        .catch(error => {
            console.error('Error saving schedule:', error);
            alert('Error saving schedule to server.');
        });
    } else {
        alert('No schedule to save.');
    }
}

function stringToArray(str) {
    // Check if the string starts with [ and ends with ]
    if (str.startsWith('[') && str.endsWith(']')) {
        // Remove the square brackets and split the string by commas
        const cleanedStr = str.slice(1, -1); // Remove the first and last character ([ and ])
        return cleanedStr.split(',').map(item => item.trim().replace(/^['"]|['"]$/g, '')); // Split by commas, trim spaces, and remove quotes if any
    }
    // If it's not a valid array format, return as is or handle the case
    return [str];
}

// Function to add an episode to the Schedule drop zone
function addEpisodeToSchedule(title, season, episodeNumber, runtime, videoLink, imgSrc, episodeId) {
    const episodeDiv = document.createElement('div');
    episodeDiv.classList.add('episode-item');
    videos = stringToArray(videoLink)
    let videoLinkHtml = '';
for (let i = 0; i < videos.length; i++) {
    videoLinkHtml += `<a href="${videos[i]}" target="_blank">Watch ${i + 1}</a><br>`;
}
episodeDiv.innerHTML = `
        <strong>${title} <br>(S${season}E${episodeNumber})</strong><br>
        ${runtime} min.<br>
        
        <button class="delete-btn">X</button><br>
        <div class=schedule_links hidden>
        ${videoLinkHtml}
        </div>
    `;

    document.getElementById('schedule-dropzone').appendChild(episodeDiv);

    // Add delete event
    episodeDiv.querySelector('.delete-btn').addEventListener('click', function() {
        episodeDiv.remove();
        deleteFromSchedule(episodeId);
    });

    // Remove placeholder message if exists
    const placeholder = document.querySelector('.drop-zone p');
    if (placeholder) {
        placeholder.remove();
    }
}

// Function to delete an episode from schedule in localStorage
function deleteFromSchedule(episodeId) {
    const storedSchedule = localStorage.getItem('schedule');
    if (storedSchedule) {
        let episodes = JSON.parse(storedSchedule);

        // Filter out the episode to be deleted by episodeId
        episodes = episodes.filter(episode => episode.episodeId !== episodeId);

        // Save updated schedule back to localStorage
        localStorage.setItem('schedule', JSON.stringify(episodes));
    }
}

// Function to clear the entire schedule list
function clearSchedule() {
    // Clear localStorage
    localStorage.removeItem('schedule');

    // Clear schedule in UI
    document.getElementById('schedule-dropzone').innerHTML = '<p>Drag episodes here</p>';
}

// Function to handle click on the series (navigates to URL)
document.querySelectorAll('.series-link').forEach(link => {
    link.addEventListener('click', function (e) {
        e.preventDefault(); // Prevent default anchor behavior (optional)
        let episodeId = this.getAttribute('data-id'); // Get the episode's data-id
        let episodeDetailsDiv = document.getElementsByClassName('episode-details')[0];
        let seriesDetailsDiv = document.getElementsByClassName('series-details')[0];

        // Search for the episode with matching episode_id in episodes array
        if (cartoon_type === 'episodes') {
            // Unhide the episode-details div and hide series-details
            let episode = episode_details_data.find(ep => ep.episode_id == episodeId);

            episodeDetailsDiv.removeAttribute('hidden');
            seriesDetailsDiv.setAttribute('hidden', true);

            // Split the video links by comma into an array
            let videoLinks = episode.video_link ? episode.video_link.split(',') : [];

            // Fill the episode-details div with the retrieved episode's details
            episodeDetailsDiv.innerHTML = `<strong>${episode.title}</strong><br>
            <img src="${episode.image}" alt="Episode Image" width="300"><br>
            <strong>Description:</strong> ${episode.description}<br>
            <strong>Runtime:</strong> ${episode.runtime} minutes<br>
            <strong>Air Date:</strong> ${episode.aired}<br>
            <br>
            ${
                episode.has_video_link === 'Yes' && videoLinks.length > 0 
                ? videoLinks.map((link, index) => `<a href="${link.trim()}" target="_blank">Watch Episode (${index + 1})</a><br>`).join('') 
                : 'No video available'
            }`;
        } else {
            window.location.href = this.getAttribute('data-url');
        }
    });
});

// Add event listeners for dragging and dropping episodes
document.querySelectorAll('.drag-episode').forEach(episode => {
    episode.addEventListener('dragstart', function (e) {
        // Set data for the dragged episode
        const videoLinkElement = this.querySelector('.video-links');
        const videoLinkHref = videoLinkElement.innerText ? videoLinkElement.innerText.split(',') : [];

        e.dataTransfer.setData('title', this.getAttribute('data-title'));
        e.dataTransfer.setData('season', this.getAttribute('data-season'));
        e.dataTransfer.setData('episode_number', this.getAttribute('data-episode-number'));
        e.dataTransfer.setData('runtime', this.getAttribute('data-runtime'));
        e.dataTransfer.setData('video_link', videoLinkHref); // Use the href of the <a> tag
        e.dataTransfer.setData('img', this.getAttribute('data-img'));
        e.dataTransfer.setData('id', this.getAttribute('data-id'));
    });
});

// Drop zone event listeners
const dropZone = document.getElementById('schedule-dropzone');
dropZone.addEventListener('dragover', function (e) {
    e.preventDefault(); // Allows dropping
});

dropZone.addEventListener('drop', function (e) {
    e.preventDefault();

    // Get episode data from drag event
    const title = e.dataTransfer.getData('title');
    const season = e.dataTransfer.getData('season');
    const episodeNumber = e.dataTransfer.getData('episode_number');
    const runtime = e.dataTransfer.getData('runtime');
    const videoLink = e.dataTransfer.getData('video_link');
    const imgSrc = e.dataTransfer.getData('img');
    const episodeId = e.dataTransfer.getData('id');

    // Add episode to the schedule
    addEpisodeToSchedule(title, season, episodeNumber, runtime, videoLink, imgSrc, episodeId);

    // Save episode to localStorage
    saveToSchedule(title, season, episodeNumber, runtime, videoLink, imgSrc, episodeId);
});

// Clear Schedule List event listener
document.getElementById('clearSchedule').addEventListener('click', clearSchedule);

// Load schedule when the page loads
document.addEventListener('DOMContentLoaded', loadSchedule);
