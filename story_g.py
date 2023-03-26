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
    start_station = "Steinkjer"
    end_station = "Mo i Rana"
    date = "2023-04-03"
    time = "00:57:00"

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()

    train_route_data = get_train_route_data(
        start_station,
        end_station,
        date,
        time,
        cursor
    )

    if not train_route_data:
        print("No such train route.")
        return

    available_chair_car_tickets = get_available_chair_car_tickets(
        *train_route_data,
        cursor
    )
    for row in available_chair_car_tickets:
        print(row)

    (_, _, train_occurence_id, arrangement_id) = train_route_data
    available_sleeping_car_tickets = get_available_sleeping_car_tickets(
        train_occurence_id,
        arrangement_id,
        cursor
    )
    for row in available_sleeping_car_tickets:
        print(row)

    return
    #TICKET PURCHASE EXAMPLE
    customer_id = 1
    train_occurence_id = 2

    cursor.execute('''
        INSERT INTO CustomerOrder(day, time, customerId, trainOccurenceId)
        VALUES (DATE('now'), TIME(), ?, ?)
    ''', (customer_id, train_occurence_id))

    order_nr = cursor.lastrowid
    track_section_id = 1
    start_index = 0
    end_index = 3
    chair_car_id = 1
    sleeping_car_id = 2
    bed_nr = 4
    row_nr = 2
    seat_nr = 4
    '''
    insert_sleeping_car_ticket(
        order_nr,
        track_section_id,
        start_index,
        end_index,
        sleeping_car_id,
        bed_nr,
        cursor
    )
    '''
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

'''
It should not be possible to buy tickets for seats that are 
already sold. However, the same seat can be sold to several
customers as long as their journeys do not overlap.
'''
def get_available_chair_car_tickets(
    start_index: int,
    end_index: int,
    train_occurence_id: int,
    arrangement_id: int,
    cursor: Cursor
) -> list:
    cursor.execute('''
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
                    TrainOccurence.trainOccurenceId = :train_occurence_id AND
                    ((:start_index > Ticket.startIndex AND
                    :start_index < Ticket.endIndex) OR
                    (:end_index > Ticket.startIndex AND
                    :end_index < Ticket.endIndex))
            )
    ''', {
        "arrangement_id": arrangement_id,
        "train_occurence_id": train_occurence_id,
        "start_index": start_index,
        "end_index": end_index
    })
    return cursor.fetchall()

'''
A customer can buy one or two places in a sleeping compartment.
If a customer has reserved a bed in a sleeping compartment, we
cannot sell the available bed to another customer. If someone
has a ticket for one of the beds in a sleeping compartment on
a part of the route, we do not sell the seats in the compartment
to others, even if their journey does not overlap with the
journey of the person who has already purchased a sleeping space.
'''
def get_available_sleeping_car_tickets(
    train_occurence_id: int,
    arrangement_id: int,
    cursor: Cursor
) -> list:
    cursor.execute('''
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
            (SleepingCar.carId, FLOOR((bedNr + 1) / 2)) NOT IN (
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
                    TrainOccurence.trainOccurenceId = ?
            )
    ''', (arrangement_id, train_occurence_id))
    return cursor.fetchall()

def get_customer(
    customer_nr: int,
    cursor: Cursor
) -> tuple[int, str] or None:
    cursor.execute('''
        SELECT customerNr, name
        FROM Customer
        WHERE Customer.customerId = ?
    ''', (customer_nr,))
    return cursor.fetchone()

# Assumes there is only one train occurence given this info.
# The first one is returned.
def get_train_route_data(
    start_station: str,
    end_station: str,
    date: str,
    time: str,
    cursor: Cursor
) -> tuple or None:
    cursor.execute('''
        SELECT
            StartStation.stationIndex,
            EndStation.stationIndex,
            trainOccurenceId,
            arrangementId
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
    ''', (date, time, start_station, end_station))
    return cursor.fetchone()

if __name__ == "__main__": main()
