db.createUser({
    user: 'admin',
    pwd: '12345678',
    roles: [{
      role: 'readWrite',
      db: 'VKR'
    }]
  });
  
  db = new Mongo().getDB("VKR");
  
  db.createCollection('users');
  