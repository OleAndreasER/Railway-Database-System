/*
a) Databasen skal kunne registrere data om alle jernbanestrekninger i Norge. Dere skal legge inn
data for Nordlandsbanen (som vist i figuren). Dette kan gjøres med et skript, dere trenger ikke å
programmere støtte for denne funksjonaliteten.
*/

INSERT INTO TrackSection(trackSectionId, name, drivingEnergy)
VALUES (1, 'Nordlandsbanen', 'diesel');

INSERT INTO RailwayStation(name, altitude)
VALUES
	('Bodø', 4.1),
	('Fauske', 34.0),
	('Mo i Rana', 3.5),
	('Mosjøen', 6.8),
    ('Steinkjer', 3.6),
	('Trondheim', 5.1);

INSERT INTO StationOnTrack(trackSectionID, stationIndex, stationName)
VALUES
    (1, 0, 'Trondheim'),
    (1, 1, 'Steinkjer'),
    (1, 2, 'Mosjøen'),
    (1, 3, 'Mo i Rana'),
    (1, 4, 'Fauske'),
    (1, 5, 'Bodø');

INSERT INTO SubSection(subSectionID, length, trackType)
VALUES
    (1, 120, 'double'),
    (2, 280, 'single'),
    (3, 90, 'single'),
    (4, 170, 'single'),
    (5, 60, 'single');

INSERT INTO BetweenStations(subSectionID, stationName)
VALUES
    (1, 'Trondheim'),
    (1, 'Steinkjer'),
    (2, 'Steinkjer'),
    (2, 'Mosjøen'),
    (3, 'Mosjøen'),
    (3, 'Mo i Rana'),
    (4, 'Mo i Rana'),
    (4, 'Fauske'),
    (5, 'Fauske'),
    (5, 'Bodø');

INSERT INTO SubSectionOf(subSectionID, trackSectionID)
VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1);
