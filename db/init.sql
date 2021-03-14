------------- Countries -------------
CREATE TABLE Countries
(
    id    serial PRIMARY KEY,
    label char(50) UNIQUE NOT NULL
);

INSERT INTO Countries (label)
VALUES ('poland'),
       ('england');
----------- END Countries -----------

------------- League -------------
CREATE TABLE League
(
    id      serial PRIMARY KEY,
    label   char(50) UNIQUE NOT NULL,
    href    char(250) UNIQUE NOT NULL,
    country integer references Countries (id)
);
----------- END League -----------

------------- Seasons -------------
CREATE TABLE Seasons
(
    id    serial PRIMARY KEY,
    label char(50) UNIQUE NOT NULL
);
----------- END Seasons -----------

------------- Clubs -------------
CREATE TABLE Clubs
(
    id   serial PRIMARY KEY,
    name char(50) UNIQUE NOT NULL
);
----------- END Clubs -----------

------------- Result -------------
CREATE TABLE Result
(
    id          serial PRIMARY KEY,
    first_club  integer NOT NULL,
    second_club integer NOT NULL,
    title char(50) UNIQUE NOT NULL
);
----------- END Result -----------

------------- Matches -------------
CREATE TABLE Matches
(
    id          serial PRIMARY KEY,
    first_club  integer references Clubs (id),
    second_club integer references Clubs (id),
    league_id   integer references League (id),
    seasons_id  integer references Seasons (id),
    result_id   integer references Result (id),
    match_day   date
);
----------- END Matches -----------