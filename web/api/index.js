const express = require('express');
const sqlite3 = require('sqlite3');

const app = express();
const db = new sqlite3.Database('Cartoon_db.sqlite');

const cors = require('cors');
app.use(cors());

app.get('/api/episodes/:main_id', (req, res) => {
  const mainId = req.params.main_id;

  db.all(`SELECT * FROM Episodes WHERE main_id = ${mainId}`, (err, rows) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('Server Error');
      return;
    }
    res.json(rows);
  });
});


app.get('/api/main-cartoons', (req, res) => {
  db.all('SELECT * FROM Main_Cartoons', (err, rows) => {
    if (err) {
      console.error(err.message);
      res.status(500).send('Server Error');
      return;
    }
    res.json(rows);
  });
});

app.listen(3000, () => {
  console.log('Server started on port 3000');
});

