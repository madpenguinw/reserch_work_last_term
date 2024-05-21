const express = require('express');
const mongoose = require('mongoose');
const { MongoClient } = require('mongodb');
const { Sequelize, DataTypes } = require('sequelize');
const { Pool } = require('pg');
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const mongoUrl = 'mongodb://admin:12345678@localhost:3456';
const pgUrl = 'postgres://admin:12345678@localhost:1234/VKR';

// MongoDB setup
// mongoose
const mongooseOptions = {
  useNewUrlParser: true,
  useUnifiedTopology: true,
  dbName: 'VKR',
}
//
mongoose.connect(mongoUrl, mongooseOptions);
const mongoUser = require('./models/mongoUser');
const mongoClient = new MongoClient(mongoUrl, { useNewUrlParser: true, useUnifiedTopology: true });

// PostgreSQL setup
const sequelize = new Sequelize(pgUrl, { dialect: 'postgres' });
const pgUser = require('./models/pgUser')(sequelize, DataTypes);
const pgPool = new Pool({
  connectionString: pgUrl
});

// Endpoints
app.get('/empty', (req, res) => {
  res.json([]);
});

app.get('/readfile/:filename', (req, res) => {
  const filename = req.params.filename;
  fs.readFile(path.join(__dirname, filename), 'utf8', (err, data) => {
    if (err) {
      return res.status(404).json({ error: 'File not found' });
    }
    res.json(JSON.parse(data));
  });
});

app.get('/mongo/get_users_odm/:count', async (req, res) => {
  const count = parseInt(req.params.count, 10);
  const users = await mongoUser.find().limit(count);
  res.json(users);
});

app.get('/mongo/get_users/:count', async (req, res) => {
  const count = parseInt(req.params.count, 10);
  await mongoClient.connect();
  const db = mongoClient.db("VKR");
  const users = await db.collection('users').find().limit(count).toArray();
  res.json(users);
});

app.get('/postgres/get_users_orm/:count', async (req, res) => {
  const count = parseInt(req.params.count, 10);
  const users = await pgUser.findAll({ limit: count });
  res.json(users);
});

app.get('/postgres/get_users/:count', async (req, res) => {
  const count = parseInt(req.params.count, 10);
  const client = await pgPool.connect();
  const result = await client.query(`SELECT * FROM users LIMIT ${count}`);
  client.release();
  res.json(result.rows);
});

app.post('/mongo/populate_odm', async (req, res) => {
  const data = require('./data.json');
  await mongoUser.insertMany(data);
  res.json({ status: 'success' });
});

app.post('/mongo/populate', async (req, res) => {
  const data = require('./data.json');
  await mongoClient.connect();
  const db = mongoClient.db("VKR");
  await db.collection('users').insertMany(data);
  res.json({ status: 'success' });
});

app.post('/postgres/populate_orm', async (req, res) => {
  const data = require('./data.json');
  await pgUser.bulkCreate(data);
  res.json({ status: 'success' });
});

app.post('/postgres/populate', async (req, res) => {
  const data = require('./data.json');
  const client = await pgPool.connect();
  const query = `
    INSERT INTO users (firstname, lastname, patronymic, age) VALUES ($1, $2, $3, $4)
  `;
  for (const user of data) {
    await client.query(query, [user.firstname, user.lastname, user.patronymic, user.age]);
  }
  client.release();
  res.json({ status: 'success' });
});

const PORT = process.env.PORT || 9002;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
