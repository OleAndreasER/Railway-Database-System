import sqlite3
import datetime

'''
h) All information about purchases made for future trips should be available for a user. This
functionality should be programmed.
'''

def main():
    customer_id = input("CustomerId: ")
    date = input("Date (YYYY-MM-DD): ")
    try: datetime.date.fromisoformat(date)
    except:
        print("Invalid date")
        return

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT
            TrainOccurence.date,
            TimeTableEntry.time,
            StartStation.stationName,
            EndStation.stationName,
            ChairCarTicket.rowNr,
            ChairCarTicket.seatNr,
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
    ''', (customer_id, date))
    

    for (date,tid,startStation,endStation,rowNr, seatNr, bedNr) in cursor.fetchall():
        print(f"dato: {date} boardingtidspunkt: {tid} fra {startStation} til {endStation}. rad: {rowNr} sete: {seatNr} seng: {bedNr}")

    connection.close();

if __name__ == "__main__": main()