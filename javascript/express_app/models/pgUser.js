module.exports = (sequelize, DataTypes) => {
    return sequelize.define('User', {
      firstname: { type: DataTypes.STRING, allowNull: false },
      lastname: { type: DataTypes.STRING, allowNull: false },
      patronymic: { type: DataTypes.STRING, allowNull: false },
      age: { type: DataTypes.INTEGER, allowNull: false }
    }, {
      tableName: 'users',
      timestamps: false
    });
  };
