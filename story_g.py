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
    # DETERMINE TRAIN ROUTE
    date = input("Date (YYYY-MM-DD): ")
    try: datetime.date.fromisoformat(date)
    except:
        print("Invalid date")
        return

    time = input("Time (HH:MM): ")
    if not time_is_valid(time):
        print("Invalid time")
        return
    time += ":00"

    start_station = input("Start station: ")
    end_station = input("End station: ")


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

    (
        start_index,
        end_index,
        train_occurence_id,
        arrangement_id,
        track_section_id,
        direction
    ) = train_route_data

    # AVAILABLE TICKETS
    available_chair_car_tickets = get_available_chair_car_tickets(
        start_index,
        end_index,
        train_occurence_id,
        arrangement_id,
        direction,
        cursor
    )

    available_sleeping_car_tickets = get_available_sleeping_car_tickets(
        train_occurence_id,
        arrangement_id,
        cursor
    )
    pretty_print(available_chair_car_tickets, available_sleeping_car_tickets)

    # DETERMINE CUSTOMER
    customer_id = maybe_int_input("Enter your customer id: ")
    if customer_id is None:
        print("Invalid id")
        return

    customer = get_customer(customer_id, cursor)
    if not customer:
        print("No customer with this id")
        return
    
    print(f"Hello {customer[1]}!")

    # START CUSTOMER ORDER
    cursor.execute('''
        INSERT INTO CustomerOrder(day, time, customerId, trainOccurenceId)
        VALUES (DATE('now'), TIME(), ?, ?)
    ''', (customer_id, train_occurence_id))
    order_nr = cursor.lastrowid

    is_chair_car_nr = lambda car_nr: any(
        car_nr == chair_car[0]
        for chair_car in available_chair_car_tickets
    )

    is_sleeping_car_nr = lambda car_nr: any(
        car_nr == sleeping_car[0]
        for sleeping_car in available_sleeping_car_tickets
    )

    def purchase_chair_car_ticket(car_nr: int, row_nr: int, seat_nr: int):
        insert_chair_car_ticket(
            order_nr,
            track_section_id,
            start_index,
            end_index,
            car_nr,
            seat_nr,
            row_nr,
            cursor
        )
        available_chair_car_tickets.remove((car_nr, row_nr, seat_nr))
    
    def purchase_sleeping_car_ticket(car_nr: int, bed_nr: int):
        insert_sleeping_car_ticket(
            order_nr,
            track_section_id,
            start_index,
            end_index,
            car_nr,
            bed_nr,
            cursor
        )
        available_sleeping_car_tickets.remove((car_nr, bed_nr))


    # ADD TICKETS TO ORDER
    purchased_ticket = False
    while True:
        if "y" != input("Do you want to add a ticket to your order (y/N)? ").lower():
            break

        car_nr = maybe_int_input("Car: ")

        if is_chair_car_nr(car_nr):
            row_nr = maybe_int_input("Row: ")
            seat_nr = maybe_int_input("Seat: ")
            if (car_nr, row_nr, seat_nr) in available_chair_car_tickets:
                purchase_chair_car_ticket(car_nr, row_nr, seat_nr)
                purchased_ticket = True
            else:
                print("That is not an available seat")
        elif is_sleeping_car_nr(car_nr):
            bed_nr = maybe_int_input("Bed: ")
            if (car_nr, bed_nr) in available_sleeping_car_tickets:
                purchase_sleeping_car_ticket(car_nr, bed_nr)
                purchased_ticket = True
            else:
                print("That is not an available bed")
        else:
            print("No such car")       
    
    # Only insert order if a ticket was purchased.
    if purchased_ticket:
        connection.commit()
        print("Tickets purchased")

    connection.close()

def maybe_int_input(prompt: str) -> int or None: 
    try: return int(input(prompt))
    except: return None

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
    car_nr: int,
    bed_nr: int,
    cursor: Cursor
):
    insert_ticket(order_nr, track_section_id, start_index, end_index, cursor)
    ticket_id = cursor.lastrowid
    cursor.execute('''
        INSERT INTO SleepingCarTicket(ticketId, carNr, bedNr)
        VALUES (?, ?, ?)
    ''', (ticket_id, car_nr, bed_nr))

def insert_chair_car_ticket(
    order_nr: int,
    track_section_id: int,
    start_index: int,
    end_index: int,
    car_nr: int,
    seat_nr: int,
    row_nr: int,
    cursor: Cursor
):
    insert_ticket(order_nr, track_section_id, start_index, end_index, cursor)
    ticket_id = cursor.lastrowid
    cursor.execute('''
        INSERT INTO ChairCarTicket(ticketId, carNr, rowNr, seatNr)
        VALUES (?, ?, ?, ?)
    ''', (ticket_id, car_nr, row_nr, seat_nr))

overlaps = {
    "main": '''
        (:start_index >= Ticket.startIndex AND
        :start_index < Ticket.endIndex) OR
        (:end_index > Ticket.startIndex AND
        :end_index <= Ticket.endIndex) OR
        (Ticket.startIndex >= :start_index AND
        Ticket.startIndex < :end_index) OR
        (Ticket.endIndex > :start_index AND
        Ticket.endIndex <= :end_index)
    ''',
    "opposite": '''
        (:end_index >= Ticket.endIndex AND
        :end_index < Ticket.startIndex) OR
        (:start_index > Ticket.endIndex AND
        :start_index <= Ticket.startIndex) OR
        (Ticket.endIndex >= :end_index AND
        Ticket.endIndex < :start_index) OR
        (Ticket.startIndex > :end_index AND
        Ticket.startIndex <= :start_index)
    '''
}

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
    direction: str,
    cursor: Cursor
) -> list:
    cursor.execute(f'''
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
            (CarInArrangement.carNr, Seat.seatNr, Seat.rowNr) NOT IN (
                SELECT
                    carNr,
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
                    ({overlaps[direction]})
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
            (CarInArrangement.carNr, FLOOR((bedNr + 1) / 2)) NOT IN (
                SELECT
                    carNr,
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
    customer_id: int,
    cursor: Cursor
) -> tuple[int, str] or None:
    cursor.execute('''
        SELECT customerId, name
        FROM Customer
        WHERE Customer.customerId = ?
    ''', (customer_id,))
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
            arrangementId,
            TrainRoute.trackSectionId,
            TrainRoute.direction
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

def pretty_print(seat_tickets: list, bed_tickets: list):
    if seat_tickets:
        print("Chair cars:")
        print("Car - Row - Seat")
        for car_nr, row_nr, seat_nr in seat_tickets:
            print(f"{car_nr} - {row_nr} - {seat_nr}")

    if bed_tickets:
        print("Sleeping cars:")
        print("Car - Compartment - Bed")
        for car_nr, bed_nr in bed_tickets:
            print(f"{car_nr} - {(bed_nr + 1) // 2} - {bed_nr}")

if __name__ == "__main__": main()
