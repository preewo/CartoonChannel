<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Cartoons</title>
    <link rel="stylesheet" href="style.css">
  </head>
  <body>
    <header>
      <h1>Cartoons</h1>
      <label for="genre-select">Filter by genre:</label>
      <select id="genre-select">
        <option value="all">All genres</option>
        <option value="Comedy">Comedy</option>
        <option value="Fantasy">Fantasy</option>
        <option value="Musical">Musical</option>
      </select>
    </header>
    <main>
      <div id="main-cartoons-container">
        <h2>Main Cartoons</h2>
        <table id="main-cartoons">
          <thead>
            <tr>
              <th>Poster</th>
              <th>Title</th>
              <th>Summary</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
      <div id="episode-list-container">
        <h2>Episodes</h2>
        <table id="episode-list">
          <thead>
            <tr>
              <th>Title</th>
              <th>Quality</th>
              <th>Duration</th>
            </tr>
          </thead>
          <tbody></tbody>
        </table>
      </div>
      <div id="pagination"></div>
    </main>
    <script src="js/main.js"></script>
  </body>
</html>

