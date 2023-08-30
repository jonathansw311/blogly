DROP DATABASE IF EXISTS  blogly;

CREATE DATABASE blogly;

\c blogly

CREATE TABLE blogger
(
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  image_url TEXT
);

INSERT INTO blogger (first_name, last_name, image_url)
VALUES
('Jim','Jones','http://none_yet'),
('Billy','Bob','http://none_yet'),
('Jonathan','Wilson','http://none_yet'),
('Ray','Decay','http://none_yet'),
('Adam','Bomb','http://none_yet')