/* table des utilisateurs avec mdp salté */
CREATE DATABASE IF NOT EXISTS db;
USE db;
CREATE TABLE IF NOT EXISTS users (
        userID      INT UNSIGNED    NOT NULL AUTO_INCREMENT,
        username    VARCHAR(30)     NOT NULL,
        pass_salt   BINARY(4)       NOT NULL,
        pass_md5    CHAR(32)        NOT NULL,
        hint        VARCHAR(50)     ,
        PRIMARY KEY (userID)
);

/* usernames et mdp pour comptes fictifs, le seul important c'est c.hackleburry */
INSERT INTO users (username, pass_salt, pass_md5) VALUES
         ('p.escobar', 'Jdhy', 'c4598aadc36b55ba1a4f64f16e2b32f1'),
         ('g.dupuy', 'Kujh', '0fd221fc1358c698ae5db16992703bcd'),
         ('a.capone', 'hTjl', '23afc9d3a96e5c338f7ba7da4f8d59f8'),
         ('c.manson', 'YbEr', 'ife3437f0308c444f0b536841131f5274');

INSERT INTO users (username, pass_salt, pass_md5, hint) VALUES
         ('c.hackle', 'yhbG', '83f9dcad901e128922d0b12d55fcb9e1', 'I don\'t need any hints man!');
