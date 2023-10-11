CREATE TABLE zipcodeData
(zipcode  char(5) Primary Key,
 medianIncome             int,
 meanIncome               int,
 population                int
);

CREATE TABLE Business
(bus_id                  char(22) Primary Key,
 zip  char(5) references zipcodeData(zipcode),
 name                             varchar(72),
 address                          varchar(80),
 city                             varchar(32),
 state                             varchar(2),
 reviewcount                              int,
 reviewrating                           float,
 bus_rating                             float,
 numCheckins                              int,
 popularity                              float
);

CREATE TABLE Review
(rev_id                  char(22) PRIMARY KEY,
 bus_id  char(22) REFERENCES Business(bus_id),
 rating                                   int,
 year                                     int,
 reviewtext                      varchar(1024)
);

CREATE TABLE Category
(cat                              varchar(40),
 bus_id  char(22) REFERENCES Business(bus_id),
 PRIMARY KEY(cat, bus_id)
); 