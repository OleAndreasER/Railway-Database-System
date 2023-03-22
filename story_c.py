import sqlite3
from sqlite3 import Cursor 
'''
c) For en stasjon som oppgis, skal bruker få ut alle togruter som er innom stasjonen en gitt ukedag.
Denne funksjonaliteten skal programmeres.
'''

def main():
    station = input("Name of station: ")
    weekday = input("Weekday: ").lower()

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT TrainRoute.trainRouteId
        FROM StationOnTrack
        INNER JOIN TimeTableEntry ON
            TimeTableEntry.trackSectionId = StationOnTrack.trackSectionId AND
            TimeTableEntry.stationIndex = StationOnTrack.stationIndex
        INNER JOIN TrainRoute ON
            TimeTableEntry.trainRouteId = TrainRoute.TrainRouteId
        INNER JOIN RunsOnWeekday ON
            TrainRoute.trainRouteId = RunsOnWeekday.trainRouteId
        WHERE
            StationOnTrack.stationName = ? AND
            RunsOnWeekday.weekdayName = ?
    ''', (station, weekday))
    print(cursor.fetchall())
    connection.commit()
    connection.close();

if __name__ == "__main__": main()
