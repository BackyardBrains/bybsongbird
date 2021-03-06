CREATE TABLE userInfo (
	username VARCHAR(256) PRIMARY KEY,
	password VARCHAR(256)
);

CREATE TABLE sampleInfo (
	sampleid  INTEGER PRIMARY KEY,
	deviceid  INTEGER,
	added     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	latitude  FLOAT,
	longitude FLOAT,
	humidity  INTEGER,
	temp      FLOAT,
	light     FLOAT,
	type1     VARCHAR(40),
	per1      FLOAT,
	type2     VARCHAR(40),
	per2      FLOAT,
	type3     VARCHAR(40),
	per3      FLOAT,
	user      VARCHAR(256),
	FOREIGN KEY (user) REFERENCES userInfo (username)
);

CREATE TABLE songInfo (
	sampleid INTEGER PRIMARY KEY,
	songid   VARCHAR(20),
	format   VARCHAR(20)
);

