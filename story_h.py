import sqlite3
import datetime
'''
h) All information about purchases made for future trips should be available for a user. This
functionality should be programmed.
'''

def main():
    customer_id = input("Customer id: ")
    today_date = input("Today's date (YYYY-MM-DD): ")
    try: datetime.date.fromisoformat(today_date)
    except:
        print("Invalid date")
        return

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT
            CustomerOrder.orderNr,
            TrainOccurence.date,
            TimeTableEntry.time,
            StartStation.stationName,
            EndStation.stationName,
            ChairCarTicket.carNr,
            ChairCarTicket.rowNr,
            ChairCarTicket.seatNr,
            SleepingCarTicket.carNr,
            SleepingCarTicket.bedNr
        FROM
            CustomerOrder
        INNER JOIN Customer ON
            CustomerOrder.customerId = Customer.customerId
        INNER JOIN Ticket ON
            CustomerOrder.orderNr = Ticket.orderNr
        INNER JOIN TrainOccurence ON
            TrainOccurence.trainOccurenceId = CustomerOrder.trainOccurenceId
        INNER JOIN TimeTableEntry ON
            TimeTableEntry.trainRouteId = TrainOccurence.trainRouteId
        INNER JOIN StationOnTrack as StartStation ON
            StartStation.stationIndex = Ticket.startIndex
        INNER JOIN StationOnTrack as EndStation ON
            EndStation.stationIndex = Ticket.endIndex
        LEFT JOIN ChairCarTicket ON
		    ChairCarTicket.ticketId = Ticket.ticketId
	    LEFT JOIN SleepingCarTicket ON
		    SleepingCarTicket.ticketId = Ticket.ticketId
        WHERE 
            Customer.customerId = ? AND
            TrainOccurence.date >= ? AND
            TimeTableEntry.stationIndex = Ticket.startIndex
    ''', (customer_id, today_date))

    # Group orders for printing
    tickets_grouped = {}
    for (
        order_nr,
        date,
        time,
        start_station,
        end_station,
        chair_car_nr,
        row_nr,
        seat_nr,
        sleeping_car_nr,
        bed_nr
    ) in cursor.fetchall():
        orders = tickets_grouped.setdefault(date, {})
        order = orders.setdefault(order_nr, {
            "time": time,
            "start_station": start_station,
            "end_station": end_station,
            "chair_tickets": [],
            "bed_tickets": []
        })
        if not seat_nr is None:
            order["chair_tickets"].append((
                chair_car_nr,
                row_nr,
                seat_nr
            ))
        elif not bed_nr is None:
            order["bed_tickets"].append((
                sleeping_car_nr,
                bed_nr
            ))

    # Printing
    for date, orders in tickets_grouped.items():
        print(f"{date}:")
        for order in orders.values():
            print(f"{order['time'][:-3]} from {order['start_station']} to {order['end_station']}")
            if order["chair_tickets"]:
                print("Car - Row - Seat")
                for car_nr, row_nr, seat_nr in order["chair_tickets"]:
                    print(f"{car_nr} - {row_nr} - {seat_nr}")
            if order["bed_tickets"]:
                print("Car - Bed")
                for (car_nr, bed_nr) in order["bed_tickets"]:
                    print(f"{car_nr} - {bed_nr}")
            print()

    connection.close();

if __name__ == "__main__": main()
