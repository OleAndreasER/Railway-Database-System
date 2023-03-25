import sqlite3
from story_d import time_is_valid
import datetime
from sqlite3 import Cursor
'''
g) Registered customers should be able to find available tickets for a desired train route and
purchase the tickets they would like. This functionality should be programmed.
• Make sure to only sell available seats.
'''

def main():
    '''
    date = input("Date (YYYY-MM-DD): ")

    time = input("Time (HH:MM): ")
    if not time_is_valid(time):
        print("Invalid time")
        return
    time += ":00"
    '''
    start_station = "Trondheim"
    end_station = "Mo i Rana"
    date = "2023-04-03"
    time = "23:05:00"

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT
            Seat.seatNr,
            Seatrow.rowNr,
            Bed.bedNr,
            TimeTableEntry.time,
            TrainOccurence.trainOccurenceId
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
            StationOnTrack.stationName = ?)
    ''', (date, time, start_station, end_station))

    for stationName in cursor.fetchall():
        print(stationName)

    #TICKET PURCHASE EXAMPLE
    '''
    customer_id = 1
    train_occurence_id = 2

    cursor.execute('''
    '''
        INSERT INTO CustomerOrder(day, time, customerId, trainOccurenceId)
        VALUES (DATE('now'), TIME(), ?, ?)
    '''
    ''', (customer_id, train_occurence_id))

    order_nr = cursor.lastrowid
    track_section_id = 1
    start_index = 0
    end_index = 1
    chair_car_id = 1
    sleeping_car_id = 2
    bed_nr = 3
    row_nr = 1
    seat_nr = 3
    insert_sleeping_car_ticket(
        order_nr,
        track_section_id,
        start_index,
        end_index,
        sleeping_car_id,
        bed_nr,
        cursor
    )

    insert_chair_car_ticket(
        order_nr,
        track_section_id,
        start_index,
        end_index,
        chair_car_id,
        seat_nr,
        row_nr,
        cursor
    )
    '''

    connection.commit()
    connection.close()

def insert_ticket(
    order_nr: int,
    track_section_id: int,
    start_index: int,
    end_index: int,
    cursor: Cursor
):
    cursor.execute('''
        INSERT INTO Ticket(orderNr, trackSectionId, startIndex, endIndex)
        VALUES (?, ?, ?, ?)
    ''', (order_nr, track_section_id, start_index, end_index))

def insert_sleeping_car_ticket(
    order_nr: int,
    track_section_id: int,
    start_index: int,
    end_index: int,
    car_id: int,
    bed_nr: int,
    cursor: Cursor
):
    insert_ticket(order_nr, track_section_id, start_index, end_index, cursor)
    ticket_id = cursor.lastrowid
    cursor.execute('''
        INSERT INTO SleepingCarTicket(ticketId, carId, bedNr)
        VALUES (?, ?, ?)
    ''', (ticket_id, car_id, bed_nr))

def insert_chair_car_ticket(
    order_nr: int,
    track_section_id: int,
    start_index: int,
    end_index: int,
    car_id: int,
    seat_nr: int,
    row_nr: int,
    cursor: Cursor
):
    insert_ticket(order_nr, track_section_id, start_index, end_index, cursor)
    ticket_id = cursor.lastrowid
    cursor.execute('''
        INSERT INTO ChairCarTicket(ticketId, carId, rowNr, seatNr)
        VALUES (?, ?, ?, ?)
    ''', (ticket_id, car_id, row_nr, seat_nr))


if __name__ == "__main__": main()
