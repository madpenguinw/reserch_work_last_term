const express = require('express');
const { Sequelize, DataTypes } = require('sequelize');
const { Pool, Client } = require('pg');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const pgUrl = 'postgres://admin:12345678@localhost:1234/VKR';

const sequelize = new Sequelize(pgUrl, { dialect: 'postgres' });
const pgUser = require('./models/pgUser')(sequelize, DataTypes);
const pgPool = new Pool({
  connectionString: pgUrl
});

const pgClient = new Client({
  connectionString: pgUrl
});
pgClient.connect();


app.get('/empty', (req, res) => {
  res.json([]);
});

app.get('/readfile/async/:filename', (req, res) => {
  const filename = req.params.filename;
  fs.readFile(path.join(__dirname, filename), 'utf8', (err, data) => {
    res.json(JSON.parse(data));
  });
});

app.get('/readfile/sync/:filename', (req, res) => {
  const filename = req.params.filename;
  const data = fs.readFileSync(path.join(__dirname, filename), 'utf8');
  res.json(JSON.parse(data));
});

app.get('/postgres/get_users_sequelize_findall/:count', async (req, res) => {
  const count = parseInt(req.params.count, 10);
  const users = await pgUser.findAll({ limit: count });
  res.json(users);
});

app.get('/postgres/get_users_sequelize_text/:count', async (req, res) => {
  const count = parseInt(req.params.count, 10);
  const users = await sequelize.query(`SELECT * FROM users LIMIT ${count}`, {
    type: Sequelize.QueryTypes.SELECT
  });
  res.json(users);
});

app.get('/postgres/get_users_pgpool/:count', async (req, res) => {
  const count = parseInt(req.params.count, 10);
  const client = await pgPool.connect();
  const result = await client.query(`SELECT * FROM users LIMIT ${count}`);
  client.release();
  res.json(result.rows);
});

app.get('/postgres/get_users_pgclient/:count', async (req, res) => {
  const count = parseInt(req.params.count, 10);
  const result = await pgClient.query(`SELECT * FROM users LIMIT ${count}`);
  res.json(result.rows);
});


const PORT = process.env.PORT || 9002;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
