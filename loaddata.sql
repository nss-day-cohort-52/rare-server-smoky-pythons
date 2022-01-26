CREATE TABLE "Users" (
  "id" INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
  "first_name" varchar,
  "last_name" varchar,
  "email" varchar,
  "bio" varchar,
  "username" varchar,
  "password" varchar,
  "profile_image_url" varchar,
  "created_on" date,
  "active" bit
);

CREATE TABLE "Posts" (
  "id" INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "content" varchar
);

CREATE TABLE "Comments" (
  "id" INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);


CREATE TABLE "Tags" (
  "id" INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER PRIMARY KEY NOT NULL AUTOINCREMENT,
  "label" varchar
);

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');


insert into Posts values (null, 1, 1, 'title', 'date', 'content');
insert into Posts values (null, 1, 1, 'title 2', 'date 2', 'content 2');
insert into PostTags values (null, 1, 1);

