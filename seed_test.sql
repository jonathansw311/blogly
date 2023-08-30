DROP DATABASE IF EXISTS  blogly_test;

CREATE DATABASE blogly_test;

\c blogly_test

CREATE TABLE blogger
(
  id SERIAL PRIMARY KEY,
  first_name TEXT NOT NULL,
  last_name TEXT NOT NULL,
  image_url TEXT
);

INSERT INTO blogger (first_name, last_name, image_url)
VALUES
('Brian','Bills','http://')
