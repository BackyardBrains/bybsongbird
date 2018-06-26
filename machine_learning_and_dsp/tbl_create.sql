CREATE TABLE sampleInfo (
  sampleid  INTEGER PRIMARY KEY,
  deviceid  INTEGER,
  added     TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  latitude  FLOAT,
  longitude FLOAT,
  humidity  FLOAT,
  temp      FLOAT,
  light     FLOAT,
  type1     VARCHAR(40),
  per1      FLOAT,
  type2     VARCHAR(40),
  per2      FLOAT,
  type3     VARCHAR(40),
  per3      FLOAT
);

/* This creates the table for results from the classifier to be put into, the python function should do this automatically so you should
not have to worry about running it manually during setup */
