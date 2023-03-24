/*
a) The database should be able to register data about all railway routes in Norway. You should enter
data for Nordlandsbanen (as shown in the figure above). This can be done with a script and you
do not need to program support for this functionality.
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

INSERT INTO StationOnTrack(trackSectionId, stationIndex, stationName)
VALUES
    (1, 0, 'Trondheim'),
    (1, 1, 'Steinkjer'),
    (1, 2, 'Mosjøen'),
    (1, 3, 'Mo i Rana'),
    (1, 4, 'Fauske'),
    (1, 5, 'Bodø');

INSERT INTO SubSection(subSectionId, length, trackType)
VALUES
    (1, 120, 'double'),
    (2, 280, 'single'),
    (3, 90, 'single'),
    (4, 170, 'single'),
    (5, 60, 'single');

INSERT INTO BetweenStations(subSectionId, stationName)
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

INSERT INTO SubSectionOf(subSectionId, trackSectionId)
VALUES
    (1, 1),
    (2, 1),
    (3, 1),
    (4, 1),
    (5, 1);
