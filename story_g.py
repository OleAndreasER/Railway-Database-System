import sqlite3
from story_d import time_is_valid
import datetime
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
    date = "2023-04-03"
    time = "23:05:00"

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT
            StationOnTrack.stationName
        FROM TrainOccurence
        INNER JOIN TrainRoute ON
            TrainOccurence.trainRouteId = TrainRoute.trainRouteId
        INNER JOIN TimeTableEntry ON
            TrainRoute.trainRouteId = TimeTableEntry.trainRouteId
        INNER JOIN StationOnTrack ON
            TimeTableEntry.trackSectionId = StationOnTrack.trackSectionId AND
            TimeTableEntry.stationIndex = StationOnTrack.stationIndex
        WHERE
            TrainOccurence.date = ? AND
            TimeTableEntry.time = ?
    ''', (date, time))
    '''
        start_station = input("Start-station: ")
        end_station = input("End-station: ")
    '''
    for (stationName,) in cursor.fetchall():
        print(stationName)

    connection.close();

if __name__ == "__main__": main()
