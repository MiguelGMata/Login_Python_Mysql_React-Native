CREATE DATABASE login_users;

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY(id), 
    nameUser VARCHAR(255), 
    email VARCHAR(255), 
    password VARCHAR(255)
);

INSERT INTO users 
    (nameUser, email, password) 
    VALUES 
    (
        'Miguel', 
        'miguelmata@gmail.com',
        'pbkdf2:sha256:260000$e4qUx47eALWO0Inb$cd3c192a9a885a8309a6077cec193db284e0690a5efe1cd6aa2a9f2c20b238cc'
    );

CREATE TABLE users (
    id INT NOT NULL AUTO_INCREMENT, 
    PRIMARY KEY(id), 
    name VARCHAR(255), 
    email VARCHAR(255), 
    password VARCHAR(255)
);