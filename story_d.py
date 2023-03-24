import sqlite3
from datetime import date
'''
d) Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
returneres, sortert på tid. Denne funksjonaliteten skal programmeres.
'''
days = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]

def main():
    startStation = input("Start station: ")
    endStation = input("End station: ")
    time = input("Time (HH:MM): ")
    if not time_is_valid(time):
        print("Invalid time")
        return
    time += ":00"

    dateStr = input("Date (YYYY-MM-DD): ")
    
    try:
        dayIndex = date.fromisoformat(dateStr).weekday()
    except:
        print("Invalid date")
        return

    dayToday = days[dayIndex]
    dayTomorrow = days[(dayIndex + 1) % len(days)]

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()

    cursor.execute('''
        SELECT
            RunsOnDay.DayName,
            StartStationEntry.time,
            EndStationEntry.time
        FROM RunsOnDay
        INNER JOIN TrainRoute ON
            TrainRoute.trainRouteId = RunsOnDay.trainRouteId
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
            ((DayName = ? AND StartStationEntry.time > ?) OR
            DayName = ?) AND
            StartStation.stationName = ? AND
            EndStation.stationName = ? AND
            ((TrainRoute.direction = 'main' AND
            StartStation.stationIndex <= EndStation.stationIndex) OR
            (TrainRoute.direction = 'opposite' AND
            EndStation.stationIndex <= StartStation.stationIndex))
        ORDER BY
            StartStationEntry.time ASC
    ''', (dayToday, time, dayTomorrow, startStation, endStation))

    rows = cursor.fetchall()
    byDay = {
        dayToday: [
            (startTime, endTime)
            for (day, startTime, endTime) in rows
            if day == dayToday
        ],
        dayTomorrow: [
            (startTime, endTime)
            for (day, startTime, endTime) in rows
            if day == dayTomorrow
        ],
    }

    for (day, rows) in byDay.items():
        print(f"{day.capitalize()}:")
        for (startTime, endTime) in rows:
            print(f"  {startStation} ({startTime[:-3]}) - {endStation} ({endTime[:-3]})")

    connection.close();

def time_is_valid(time: str) -> bool:
    split = time.split(":")
    if not len(split) == 2: return False
    if not split[0].isdigit(): return False
    if not split[1].isdigit(): return False
    hour = int(split[0])
    minute = int(split[1])
    if hour < 0 or hour >= 24: return False
    if minute < 0 or minute >= 60: return False
    return True


if __name__ == "__main__": main()
