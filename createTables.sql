CREATE TABLE RailwayStation(
    name TEXT,
    altitude REAL,
    PRIMARY KEY(name)
);

CREATE TABLE SubSection(
    subSectionId INTEGER,
    length REAL,
    trackType TEXT NOT NULL,
    PRIMARY KEY(subSectionId)
);

CREATE TABLE BetweenStations(
    subSectionId INTEGER,
    stationName TEXT,
    PRIMARY KEY(subSectionId, stationName),
    FOREIGN KEY(subSectionId) REFERENCES SubSection(subSectionId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(stationName) REFERENCES RailwayStation(name) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE StationOnTrack(
    trackSectionId INTEGER,
    stationIndex INTEGER,
    stationName TEXT,
    PRIMARY KEY(trackSectionId, stationIndex),
    FOREIGN KEY(trackSectionId) REFERENCES TrackSection(trackSectionId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(stationName) REFERENCES RailwayStation(name) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SubSectionOf(
    subSectionId INTEGER,
    trackSectionId INTEGER,
    PRIMARY KEY(subSectionId, trackSectionId),
    FOREIGN KEY(subSectionId) REFERENCES SubSection(subSectionId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(trackSectionId) REFERENCES TrackSection(trackSectionId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE TrackSection(
    trackSectionId INTEGER,
    name TEXT NOT NULL,
    drivingEnergy TEXT NOT NULL,
    PRIMARY KEY(trackSectionId)
);

CREATE TABLE TrainRoute(
    trainRouteId INTEGER,
    direction TEXT NOT NULL,
    trackSectionId INTEGER,
    arrangementId INTEGER,
    operatorId TEXT,
    PRIMARY KEY(trainRouteId),
    FOREIGN KEY(trackSectionId) REFERENCES TrackSection(trackSectionId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(arrangementId) REFERENCES CarArrangement(arrangementId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(operatorId) REFERENCES Operator(operatorId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE CarArrangement(
    arrangementId INTEGER,
    PRIMARY KEY(arrangementId)
);

CREATE TABLE Operator(
    operatorId TEXT,
    PRIMARY KEY(operatorId)
);

CREATE TABLE TimeTableEntry(
    entryId INTEGER,
    time TEXT NOT NULL,
    trackSectionId INTEGER,
    stationIndex INTEGER,
    trainRouteId INTEGER,
    PRIMARY KEY(entryId),
    FOREIGN KEY(trackSectionId) REFERENCES TrackSection(trackSectionId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(stationIndex) REFERENCES StationOnTrack(stationIndex) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(trainRouteId) REFERENCES TrainRoute(trainRouteId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE TrainOccurence(
    trainOccurenceId INTEGER,
    date TEXT NOT NULL,
    trainRouteId INTEGER,
    PRIMARY KEY(trainOccurenceId),
    FOREIGN KEY(trainRouteId) REFERENCES TrainRoute(trainRouteId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Weekday(
    name TEXT,
    PRIMARY KEY(name)
);

CREATE TABLE RunsOnWeekday(
    trainRouteId INTEGER,
    weekdayName TEXT,
    PRIMARY KEY (trainRouteId, weekdayName),
    FOREIGN KEY(trainRouteId) REFERENCES TrainRoute(trainRouteId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(weekdayName) REFERENCES Weekday(name) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE CarInArrangement(
    arrangementId INTEGER,
    carNr INTEGER,
    carId INTEGER,
    PRIMARY KEY(arrangementId, carNr),
    FOREIGN KEY(arrangementId) REFERENCES CarArrangement(arrangementId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(carId) REFERENCES Car(carId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Car(
    carId INTEGER,
    operatorId TEXT,
    PRIMARY KEY(carId),
    FOREIGN KEY(carId) REFERENCES Operator(operatorId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Customer(
    customerId INTEGER,
    name TEXT,
    email TEXT,
    mobileNr TEXT,
    PRIMARY KEY(customerId)
);

CREATE TABLE CustomerOrder(
    orderNr INTEGER,
    day TEXT NOT NULL,
    time TEXT NOT NULL,
    customerId INTEGER,
    trainOccurenceId INTEGER,
    PRIMARY KEY(orderNr),
    FOREIGN KEY(customerId) REFERENCES Customer(customerId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(trainOccurenceId) REFERENCES TrainOccurence(trainOccurenceId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SleepingCar(
    carId INTEGER,
    PRIMARY KEY (carId),
    FOREIGN KEY(carId) REFERENCES Car(carId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SleepingCompartment(
    carId INTEGER,
    compartmentNr INTEGER,
    PRIMARY KEY (carId, compartmentNr),
    FOREIGN KEY(carId) REFERENCES Car(carId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Bed(
    carId INTEGER,
    bedNr INTEGER,
    PRIMARY KEY (carId, bedNr),
    FOREIGN KEY(carId) REFERENCES Car(carId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(bedNr) REFERENCES SleepingCompartment(compartmentNr) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ChairCar(
    carId INTEGER,
    PRIMARY KEY (carId),
    FOREIGN KEY(carId) REFERENCES Car(carId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SeatRow(
    carId INTEGER,
    rowNr INTEGER,
    PRIMARY KEY (carId, rowNr),
    FOREIGN KEY(carId) REFERENCES Car(carId) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Seat(
    carId INTEGER,
    rowNr INTEGER,
    seatNr INTEGER,
    PRIMARY KEY (carId, rowNr,seatNr),
    FOREIGN KEY(carId) REFERENCES Car(carId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(rowNr) REFERENCES SeatRow(rowNr) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Ticket(
    ticketId INTEGER,
    orderNr INTEGER,
    trackSectionId INTEGER,
    startIndex INTEGER,
    endIndex INTEGER,
    PRIMARY KEY(ticketId),
    FOREIGN KEY(orderNr) REFERENCES CustomerOrder(orderNr),
    FOREIGN KEY(trackSectionId) REFERENCES TrackSection(trackSectionId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(startIndex) REFERENCES TimeTableEntry(stationIndex) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(endIndex) REFERENCES TimeTableEntry(stationIndex) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE ChairCarTicket(
    ticketId INTEGER,
    carId INTEGER,
    rowNr INTEGER,
    seatNr INTEGER,
    PRIMARY KEY (ticketId),
    FOREIGN KEY(ticketId) REFERENCES Ticket(ticketId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(carId) REFERENCES ChairCar(carId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(rowNr) REFERENCES SeatRow(rowNr) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(seatNr) REFERENCES Seat(seatNr) on UPDATE CASCADE on DELETE CASCADE
);

CREATE TABLE SleepingCarTicket(
    ticketId INTEGER,
    carId INTEGER,
    bedNr INTEGER,
    PRIMARY KEY (ticketId),
    FOREIGN KEY(ticketId) REFERENCES Ticket(ticketId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(carId) REFERENCES SleepingCar(carId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(bedNr) REFERENCES Bed(bedNr) ON UPDATE CASCADE ON DELETE CASCADE
);
