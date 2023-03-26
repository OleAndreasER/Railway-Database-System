//Chair car tickets
        SELECT
            CarInArrangement.carNr,
            Seatrow.rowNr,
            Seat.seatNr
        FROM CarArrangement
        INNER JOIN CarInArrangement ON
            CarArrangement.arrangementId = CarInArrangement.arrangementId
        INNER JOIN ChairCar ON
            CarInArrangement.carId = ChairCar.carId
        INNER JOIN SeatRow ON
            ChairCar.carId = SeatRow.carId
        INNER JOIN Seat ON
            SeatRow.carId = Seat.carId AND
            SeatRow.rowNr = Seat.rowNr
        WHERE
            CarArrangement.arrangementId = :arrangement_id AND
            (Seat.carId, Seat.seatNr, Seat.rowNr) NOT IN (
                SELECT
                    carId,
                    seatNr,
                    rowNr
                FROM TrainOccurence
                INNER JOIN CustomerOrder ON
                    TrainOccurence.trainOccurenceId = CustomerOrder.trainOccurenceId
                INNER JOIN Ticket ON
                    CustomerOrder.orderNr = Ticket.orderNr
                INNER JOIN ChairCarTicket ON
                    Ticket.ticketId = ChairCarTicket.ticketId
                WHERE
                    TrainOccurence = ? AND
                    ((:start_index > Ticket.startIndex AND
                    :start_index < Ticket.endIndex) OR
                    (:end_index > Ticket.startIndex AND
                    :end_index < Ticket.endIndex))
            )

//Sleeping car tickets
        SELECT
            CarInArrangement.carNr,
            Bed.bedNr
        FROM CarArrangement
        INNER JOIN CarInArrangement ON
            CarArrangement.arrangementId = CarInArrangement.arrangementId
        INNER JOIN SleepingCar ON
            CarInArrangement.carId = SleepingCar.carId
        INNER JOIN Bed ON
            SleepingCar.carId = Bed.carId
        WHERE
            CarArrangement.arrangementId = ? AND
            (carId, FLOOR((bedNr + 1) / 2)) NOT IN (
                SELECT
                    carId,
                    FLOOR((bedNr + 1) / 2)
                FROM TrainOccurence
                INNER JOIN CustomerOrder ON
                    TrainOccurence.trainOccurenceId = CustomerOrder.trainOccurenceId
                INNER JOIN Ticket ON
                    CustomerOrder.orderNr = Ticket.orderNr
                INNER JOIN SleepingCarTicket ON
                    Ticket.ticketId = SleepingCarTicket.ticketId
                WHERE
                    TrainOccurence = ?
            )


        INSERT INTO CustomerOrder(day, time, customerId, trainOccurenceId)
        VALUES (DATE('now'), TIME(), ?, ?);

        INSERT INTO Ticket(orderNr, trackSectionId, startIndex, endIndex)
        VALUES (?, ?, ?, ?);

        INSERT INTO SleepingCarTicket(ticketId, carId, bedNr)
        VALUES (?, ?, ?);

        INSERT INTO ChairCarTicket(ticketId, carId, rowNr, seatNr)
        VALUES (?, ?, ?, ?);


        SELECT customerId, name
        FROM Customer
        WHERE Customer.customerId = ?

        SELECT
            trainOccurenceId,
            arrangementId,
            EndStation.stationIndex,
            StartStation.stationIndex
        FROM TrainOccurence
        INNER JOIN TrainRoute ON
            TrainRoute.trainRouteId = TrainOccurence.trainRouteId
        INNER JOIN TimeTableEntry AS StartStationEntry ON
            TrainRoute.trainRouteId = StartStationEntry.trainRouteId
        INNER JOIN TimeTableEntry AS EndStationEntry ON
            TrainRoute.trainRouteId = EndStationEntry.trainRouteId
        INNER JOIN StationOnTrack AS StartStation ON
            StartStationEntry.trackSectionId = StartStation.trackSectionId AND
            StartStationEntry.stationIndex = StartStation.stationIndex
        INNER JOIN StationOnTrack AS EndStation ON
            EndStationEntry.trackSectionId = EndStation.trackSectionId AND
            EndStationEntry.stationIndex = EndStation.stationIndex
        WHERE
            TrainOccurence.date = ? AND
            StartStationEntry.time = ? AND
            StartStation.stationName = ? AND
            EndStation.stationName = ?

            SELECT
                carId,
                FLOOR((bedNr + 1) / 2)
            FROM TrainOccurence
            INNER JOIN CustomerOrder ON
                TrainOccurence.trainOccurenceId = CustomerOrder.trainOccurenceId
            INNER JOIN Ticket ON
                CustomerOrder.orderNr = Ticket.orderNr
            INNER JOIN SleepingCarTicket ON
                Ticket.ticketId = SleepingCarTicket.ticketId
            WHERE
                TrainOccurence = ?


        SELECT
            CarInArrangement.carId,
            Seatrow.rowNr,
            Seat.seatNr
        FROM CarArrangement
        INNER JOIN CarInArrangement ON
            CarArrangement.arrangementId = CarInArrangement.arrangementId
        INNER JOIN ChairCar ON
            CarInArrangement.carId = ChairCar.carId
        INNER JOIN SeatRow ON
            ChairCar.carId = SeatRow.carId
        INNER JOIN Seat ON
            SeatRow.carId = Seat.carId AND
            SeatRow.rowNr = Seat.rowNr
        WHERE
            CarArrangement.arrangementId = :arrangement_id AND
            (Seat.carId, Seat.seatNr, Seat.rowNr) NOT IN (
                SELECT
                    carId,
                    seatNr,
                    rowNr
                FROM TrainOccurence
                INNER JOIN CustomerOrder ON
                    TrainOccurence.trainOccurenceId = CustomerOrder.trainOccurenceId
                INNER JOIN Ticket ON
                    CustomerOrder.orderNr = Ticket.orderNr
                INNER JOIN ChairCarTicket ON
                    Ticket.ticketId = ChairCarTicket.ticketId
                WHERE
                    TrainOccurence.trainOccurenceId = :train_occurence_id AND

                    ((:start_index >= Ticket.startIndex AND
                    :start_index < Ticket.endIndex) OR
                    (:end_index > Ticket.startIndex AND
                    :end_index <= Ticket.endIndex) OR
                    (Ticket.startIndex >= :start_index AND
                    Ticket.startIndex < :end_index) OR
                    (Ticket.endIndex > :start_index AND
                    Ticket.endIndex <= :end_index))
            )

                    ((:end_index >= Ticket.endIndex AND //
                    :end_index < Ticket.startIndex) OR //
                    (:start_index > Ticket.endIndex AND //
                    :start_index <= Ticket.startIndex) OR //
                    (Ticket.endIndex >= :end_index AND //
                    Ticket.endIndex < :start_index) OR //
                    (Ticket.startIndex > :end_index AND //
                    Ticket.startIndex <= :start_index)) //