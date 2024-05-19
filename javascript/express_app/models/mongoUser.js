const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  firstname: { type: String, required: true },
  lastname: { type: String, required: true },
  patronymic: { type: String, required: true },
  age: { type: Number, required: true }
});

module.exports = mongoose.model('User', userSchema);
