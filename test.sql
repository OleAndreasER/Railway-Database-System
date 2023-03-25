        SELECT
            *
        FROM TrainOccurence
        INNER JOIN TrainRoute ON
            TrainOccurence.trainRouteId = TrainRoute.trainRouteId
        INNER JOIN TimeTableEntry ON
            TrainRoute.trainRouteId = TimeTableEntry.trainRouteId
        INNER JOIN StationOnTrack ON
            TimeTableEntry.trackSectionId = StationOnTrack.trackSectionId AND
            TimeTableEntry.stationIndex = StationOnTrack.stationIndex
        INNER JOIN CarArrangement ON
            CarArrangement.arrangementId = TrainRoute.arrangementId
        INNER JOIN CarInArrangement ON
            CarArrangement.arrangementId = CarInArrangement.arrangementId
        INNER JOIN Car ON
            CarInArrangement.carId = Car.carId
        LEFT JOIN ChairCar ON
            Car.carId = ChairCar.carId
        LEFT JOIN SleepingCar ON
            Car.carId = SleepingCar.carId
        LEFT JOIN SeatRow ON
            ChairCar.carId = SeatRow.carId
        LEFT JOIN Seat ON
            SeatRow.carId = Seat.carId AND
            SeatRow.rowNr = Seat.rowNr
        LEFT JOIN Bed ON
            SleepingCar.carId = Bed.carId
        WHERE
            TrainOccurence.date = ? AND
            TimeTableEntry.time = ? AND
            (StationOnTrack.stationName = ? OR
            StationOnTrack.stationName = ?);


        SELECT *
        FROM TrainOccurence
        INNER JOIN CustomerOrder ON
            TrainOccurence.trainOccurenceId = CustomerOrder.trainOccurenceId
        INNER JOIN Ticket ON
            CustomerOrder.orderNr = Ticket.orderNr


        INSERT INTO CustomerOrder(day, time, customerId, trainOccurenceId)
        VALUES (DATE('now'), TIME(), ?, ?)

        INSERT INTO Ticket(orderNr, trackSectionId, startIndex, endIndex)
        VALUES (?, ?, ?, ?)

        INSERT INTO SleepingCarTicket(ticketId, carId, bedNr)
        VALUES (?, ?, ?)

        INSERT INTO ChairCarTicket(ticketId, carId, rowNr, seatNr)
        VALUES (?, ?, ?, ?)