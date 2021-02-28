------------- Countries -------------
CREATE TABLE Countries
(
    id    serial PRIMARY KEY,
    label char(50) NOT NULL
);

INSERT INTO Countries (label)
VALUES ('poland'),
       ('england');
----------- END Countries -----------

------------- League -------------
CREATE TABLE League
(
    id    serial PRIMARY KEY,
    label char(50) NOT NULL
);
----------- END League -----------

------------- Seasons -------------
CREATE TABLE Seasons
(
    id    serial PRIMARY KEY,
    label char(50) NOT NULL
);
----------- END Seasons -----------

------------- Clubs -------------
CREATE TABLE Clubs
(
    id      serial PRIMARY KEY,
    country integer references Countries (id),
    name    char(50) NOT NULL
);
----------- END Clubs -----------

------------- Result -------------
CREATE TABLE Result
(
    id          serial PRIMARY KEY,
    first_club  integer,
    second_club integer
);
----------- END Result -----------

------------- Matches -------------
CREATE TABLE Matches
(
    id          serial PRIMARY KEY,
    first_club  integer references Clubs (id),
    second_club integer references Clubs (id),
    match_day   date
);
----------- END Matches -----------