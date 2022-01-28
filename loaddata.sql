CREATE TABLE "Users" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
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
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "user_id" INTEGER,
  "category_id" INTEGER,
  "title" varchar,
  "publication_date" date,
  "content" varchar
);

CREATE TABLE "Comments" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "author_id" INTEGER,
  "content" varchar,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users`(`id`)
);


CREATE TABLE "Tags" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);

CREATE TABLE "PostTags" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "post_id" INTEGER,
  "tag_id" INTEGER,
  FOREIGN KEY(`post_id`) REFERENCES `Posts`(`id`),
  FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`)
);

CREATE TABLE "Categories" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "label" varchar
);
CREATE TABLE "Subscriptions" (
  "id" INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
  "follower_id" INTEGER,
  "author_id" INTEGER,
  "created_on" date,
  FOREIGN KEY (`follower_id`) REFERENCES `Users` (`id`),
  FOREIGN KEY(`author_id`) REFERENCES `Users` (`id`)
)

INSERT INTO Categories ('label') VALUES ('News');
INSERT INTO Tags ('label') VALUES ('JavaScript');


insert into Posts values (null, 1, 1, 'title', 'date', 'content');
insert into Posts values (null, 1, 1, 'title 2', 'date 2', 'content 2');
insert into PostTags values (null, 1, 1);

