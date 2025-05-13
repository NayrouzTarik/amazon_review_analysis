db.createUser({
    user: "admin",
    pwd: "password",
    roles: [{ role: "readWrite", db: "reviews_db" }]
  });
  

db.createCollection("reviews");
