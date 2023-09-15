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
('Adam','Bomb','http://none_yet');

CREATE TABLE posts
(
  post_id SERIAL PRIMARY KEY,
  title TEXT NOT NULL,
  content TEXT NOT NULL,
  created_at timestamp NOT NULL,
  user_id INT NOT NULL
);

INSERT INTO posts (title, content, created_at, user_id)
VALUES
('first post', 'This is the very first post.  This is the content!', CURRENT_TIMESTAMP, 1),
('second post', 'This is the only the  secont post.  This is the second post content!', CURRENT_TIMESTAMP , 1);

CREATE TABLE tags
(
  t_id SERIAL PRIMARY KEY,
  t_name TEXT NOT NULL
);

INSERT INTO tags (t_name)
VALUES
('first tag');

CREATE TABLE post_tag (
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (post_id, tag_id),
    FOREIGN KEY (post_id) REFERENCES posts (post_id),
    FOREIGN KEY (tag_id) REFERENCES tags (t_id)
);
INSERT INTO post_tag (post_id, tag_id)
VALUES
(1,1);