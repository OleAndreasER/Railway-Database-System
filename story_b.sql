/*
b) Dere skal kunne registrere data om togruter. Dere skal legge inn data for de tre togrutene på
Nordlandsbanen som er beskrevet i vedlegget til denne oppgave. Dette kan gjøres med et skript,
dere trenger ikke å programmere støtte for denne funksjonaliteten.
*/

INSERT INTO TrainRoute(
    trainRouteId,
    direction,
    trackSectionId,
    arrangementId,
    operatorId
)
VALUES
    -- This train route runs every weekday and has a car setup with two chair cars of type SJ-chair car-1
    (1, 'main', 1, 1, 'SJ'),
    -- This train route runs every weekday and has a car setup with one chair car of type SJ-chair car-1, followed by one sleeping car of type SJ-sleeping car-1
    (2, 'main', 1, 2, 'SJ'),
    -- This train route runs every weekday (Monday to Friday) and has a car setup with one chair car of typeSJ-chair car-1
    (3, 'opposite', 1, 3, 'SJ');


INSERT INTO Operator(operatorId)
VALUES ('SJ');

INSERT INTO Car(carId, operatorId)
VALUES
    (1, 'SJ'),
    (2, 'SJ');

INSERT INTO CarInArrangement(arrangementId, carNr, carId)
VALUES
    (1, 1, 1),
    (1, 2, 1),
    (2, 1, 1),
    (2, 2, 2),
    (3, 1, 1);

INSERT INTO ChairCar(carId)
VALUES (1);

INSERT INTO SeatRow(carId, rowNr)
VALUES
    (1, 1),
    (1, 2),
    (1, 3);

INSERT INTO Seat(carId, rowNr, seatNr)
VALUES
    (1, 1, 1),
    (1, 1, 2),
    (1, 1, 3),
    (1, 1, 4),
    (1, 2, 5),
    (1, 2, 6),
    (1, 2, 7),
    (1, 2, 8),
    (1, 3, 9),
    (1, 3, 10),
    (1, 3, 11),
    (1, 3, 12);


INSERT INTO SleepingCar(carId)
VALUES (2);

INSERT INTO SleepingCompartment(carId, compartmentNr)
VALUES
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4);

INSERT INTO Bed(carId, bedNr)
VALUES
    (2, 1),
    (2, 2),
    (2, 3),
    (2, 4),
    (2, 5),
    (2, 6),
    (2, 7),
    (2, 8);

INSERT INTO CarArrangement(arrangementId)
VALUES
    (1),
    (2),
    (3);

INSERT INTO TimeTableEntry(
    entryId,
    time,
    trackSectionId,
    stationIndex,
    trainRouteId
)
VALUES
    (1, '07:49:00', 1, 0, 1),
    (2, '09:51:00', 1, 1, 1),
    (3, '13:20:00', 1, 2, 1),
    (4, '14:31:00', 1, 3, 1),
    (5, '16:49:00', 1, 4, 1),
    (6, '17:34:00', 1, 5, 1),

    (7, '23:05:00', 1, 0, 2),
    (8, '00:57:00', 1, 1, 2),
    (9, '04:41:00', 1, 2, 2),
    (10, '05:55:00', 1, 3, 2),
    (11, '08:19:00', 1, 4, 2),
    (12, '09:05:00', 1, 5, 2),

    (13, '08:11:00', 1, 3, 3),
    (14, '09:14:00', 1, 2, 3),
    (15, '12:31:00', 1, 1, 3),
    (16, '14:13:00', 1, 0, 3);

INSERT INTO Weekday(name)
VALUES
    ('monday'),
    ('tuesday'),
    ('wednesday'),
    ('thursday'),
    ('friday');

INSERT INTO RunsOnWeekday(trainRouteId, weekdayName)
VALUES
    (1, 'monday'),
    (1, 'tuesday'),
    (1, 'wednesday'),
    (1, 'thursday'),
    (1, 'friday'),

    (2, 'monday'),
    (2, 'tuesday'),
    (2, 'wednesday'),
    (2, 'thursday'),
    (2, 'friday'),

    (3, 'monday'),
    (3, 'tuesday'),
    (3, 'wednesday'),
    (3, 'thursday'),
    (3, 'friday');
