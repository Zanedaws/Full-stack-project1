PRAGMA foreign_keys = ON;
CREATE TABLE users (name TEXT,pass TEXT,hash INT PRIMARY KEY);
CREATE TABLE posts (userHash INT , time TEXT DEFAULT CURRENT_TIMESTAMP,
postHash INT PRIMARY KEY, likes INT, content TEXT, title TEXT, FOREIGN KEY (userHash) REFERENCES users (hash));
CREATE TABLE likes (userHash INT, postHash INT, type INT, FOREIGN KEY (userHash) REFERENCES users (hash));