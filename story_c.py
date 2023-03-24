import sqlite3
'''
c) For en stasjon som oppgis, skal bruker få ut alle togruter som er innom stasjonen en gitt ukedag.
Denne funksjonaliteten skal programmeres.
'''

def main():
    station = input("Name of station: ")
    day = input("day: ").lower()

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    cursor.execute('''
        SELECT
            TimeTableEntry.time,
            TrackSection.name
        FROM
            StationOnTrack
        INNER JOIN TimeTableEntry ON
            TimeTableEntry.trackSectionId = StationOnTrack.trackSectionId AND
            TimeTableEntry.stationIndex = StationOnTrack.stationIndex
        INNER JOIN TrainRoute ON
            TimeTableEntry.trainRouteId = TrainRoute.TrainRouteId
        INNER JOIN RunsOnDay ON
            TrainRoute.trainRouteId = RunsOnDay.trainRouteId
        INNER JOIN TrackSection ON
            TrainRoute.trackSectionId = TrackSection.trackSectionId
        WHERE
            StationOnTrack.stationName = ? AND
            RunsOnDay.DayName = ?
        ORDER BY
            TimeTableEntry.time DESC
    ''', (station, day))

    for (time, trackSection) in cursor.fetchall():
        print(f"{time} on {trackSection}")

    connection.commit()
    connection.close();

if __name__ == "__main__": main()
