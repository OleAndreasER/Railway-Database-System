CREATE TABLE RailwayStation(
    name TEXT,
    altitude REAL,
    PRIMARY KEY(name)
);

CREATE TABLE SubSection(
    subSectionID INTEGER,
    length REAL,
    trackType TEXT NOT NULL,
    PRIMARY KEY(subSectionID)
);

CREATE TABLE BetweenStations(
    subSectionID INTEGER,
    stationName TEXT,
    PRIMARY KEY(subSectionID, stationName),
    FOREIGN KEY(subSectionID) REFERENCES SubSection(subSectionID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(stationName) REFERENCES RailwayStation(name) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE StationOnTrack(
    trackSectionID INTEGER,
    stationIndex INTEGER,
    stationName TEXT,
    PRIMARY KEY(trackSectionID, stationIndex),
    FOREIGN KEY(trackSectionID) REFERENCES TrackSection(trackSectionID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(stationName) REFERENCES RailwayStation(name) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE SubSectionOf(
    subSectionID INTEGER,
    trackSectionID INTEGER,
    PRIMARY KEY(subSectionID, trackSectionID),
    FOREIGN KEY(subSectionID) REFERENCES SubSection(subSectionID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(trackSectionID) REFERENCES TrackSection(trackSectionID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE TrackSection(
    trackSectionID INTEGER,
    name TEXT NOT NULL,
    drivingEnergy TEXT NOT NULL,
    PRIMARY KEY(trackSectionID)
);

CREATE TABLE TrainRoute(
    trainRouteID INTEGER,
    direction TEXT NOT NULL,
    trackSectionID INTEGER,
    arrangementId INTEGER,
    operatorId TEXT,
    PRIMARY KEY(trainRouteID),
    FOREIGN KEY(trackSectionID) REFERENCES TrackSection(trackSectionID) ON UPDATE CASCADE ON DELETE CASCADE,
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
    trackSectionID INTEGER,
    stationIndex INTEGER,
    trainRouteID INTEGER,
    PRIMARY KEY(entryId),
    FOREIGN KEY(trackSectionID) REFERENCES TrackSection(trackSectionID) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(stationIndex) REFERENCES StationOnTrack(stationIndex) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(trainRouteID) REFERENCES TrainRoute(trainRouteID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE TrainOccurence(
    trainOccurenceId INTEGER,
    date TEXT NOT NULL,
    trainRouteID INTEGER,
    PRIMARY KEY(trainOccurenceId),
    FOREIGN KEY(trainRouteID) REFERENCES TrainRoute(trainRouteID) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE Weekday(
    name TEXT,
    PRIMARY KEY(name)
);

CREATE TABLE RunsOnWeekday(
    trainRouteID INTEGER,
    weekdayName TEXT,
    PRIMARY KEY (trainRouteID, weekdayName),
    FOREIGN KEY(trainRouteID) REFERENCES TrainRoute(trainRouteID) ON UPDATE CASCADE ON DELETE CASCADE,
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
    mobileNr INTEGER,
    PRIMARY KEY(customerId)
);

CREATE TABLE CommonCustomerRegistry(
    operatorId TEXT,
    customerId INTEGER,
    PRIMARY KEY (operatorId, customerId),
    FOREIGN KEY(operatorId) REFERENCES Operator(operatorId) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY(customerId) REFERENCES Customer(customerId) ON UPDATE CASCADE ON DELETE CASCADE
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
    trackSectionID INTEGER,
    startIndex INTEGER,
    endIndex INTEGER,
    PRIMARY KEY(ticketId),
    FOREIGN KEY(orderNr) REFERENCES CustomerOrder(orderNr),
    FOREIGN KEY(trackSectionID) REFERENCES TrackSection(trackSectionID) ON UPDATE CASCADE ON DELETE CASCADE,
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