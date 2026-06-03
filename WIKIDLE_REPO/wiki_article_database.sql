DROP TABLE IF EXISTS plays;
DROP TABLE IF EXISTS daily_game;
DROP TABLE IF EXISTS player;
DROP TABLE IF EXISTS wikipedia_articles;

CREATE TABLE wikipedia_articles (
	article_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
	title VARCHAR(255),
	summary TEXT,
	category VARCHAR(100),
	picture TEXT);

CREATE TABLE Player (
	player_id int PRIMARY KEY
);

CREATE TABLE Daily_game (
	date DATE PRIMARY KEY
);

CREATE TABLE Plays (
	guess_amount INT,
	player_id INT REFERENCES Player(player_id) ON DELETE CASCADE,
	date DATE REFERENCES Daily_game(date) ON DELETE CASCADE
	);