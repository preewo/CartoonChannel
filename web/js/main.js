const mainCartoonsTable = document.getElementById("main-cartoons");
const episodeTable = document.getElementById("episode-list");
const paginationDiv = document.getElementById("pagination");

const itemsPerPage = 20;
let currentPage = 1;
let filteredMainCartoons = [];

const fetchMainCartoons = () => {
  const selectedGenre = document.getElementById("genre-select").value;
  fetch("http://localhost:3000/api/main-cartoons")
    .then(response => response.json())
    .then(mainCartoons => {
      filteredMainCartoons = mainCartoons.filter(mainCartoon => {
        if (selectedGenre === "all") {
          return true;
        } else {
          const genres = mainCartoon.genre.split(",");
          return genres.includes(selectedGenre);
        }
      });
      currentPage = 1;
      renderMainCartoons();
      renderPagination();
    })
    .catch(error => console.error(error));
};

const genreSelect = document.getElementById("genre-select");
genreSelect.addEventListener("change", () => {
  fetchMainCartoons();
});


const renderMainCartoons = () => {
  mainCartoonsTable.innerHTML = "";
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  filteredMainCartoons.slice(startIndex, endIndex).forEach(mainCartoon => {
    const row = document.createElement("tr");
    const posterCell = document.createElement("td");
    const posterImg = document.createElement("img");
    posterImg.src = mainCartoon.poster_url;
    posterImg.alt = mainCartoon.main_title;
    posterImg.width = 100;
    posterCell.appendChild(posterImg);
    row.appendChild(posterCell);
    const titleCell = document.createElement("td");
    titleCell.textContent = mainCartoon.main_title;
    row.appendChild(titleCell);
    const summaryCell = document.createElement("td");
    summaryCell.textContent = mainCartoon.summary;
    row.appendChild(summaryCell);
    if (mainCartoon.seen === 1) {
      row.classList.add("seen");
    }
    mainCartoonsTable.appendChild(row);
    row.addEventListener("click", () => {
      fetch(`http://localhost:3000/api/episodes/${mainCartoon.id}`)
        .then(response => response.json())
        .then(episodes => {
          episodeTable.innerHTML = "";
          episodes.forEach(episode => {
            const row = document.createElement("tr");
            const titleCell = document.createElement("td");
            titleCell.textContent = episode.title;
            if (episode.seen === 1) {
              titleCell.classList.add("seen");
            }
            row.appendChild(titleCell);
            const summaryCell = document.createElement("td");
            summaryCell.textContent = episode.quality;
            row.appendChild(summaryCell);
            const durationCell = document.createElement("td");
            durationCell.textContent = episode.vid_lenght;
            row.appendChild(durationCell);
            episodeTable.appendChild(row);
          });
        });
    });
  });
};

const renderPagination = () => {
  const numPages = Math.ceil(filteredMainCartoons.length / itemsPerPage);
  paginationDiv.innerHTML = "";
  for (let i = 1; i <= numPages; i++) {
    const button = document.createElement("button");
    button.textContent = i;
    if (i === currentPage) {
      button.classList.add("active");
    }
    button.addEventListener("click", () => {
      currentPage = i;
      renderMainCartoons();
      renderPagination();
    });
    paginationDiv.appendChild(button);
  }
};

fetchMainCartoons();
