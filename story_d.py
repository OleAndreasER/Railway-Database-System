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
    start_station = input("Start station: ")
    end_station = input("End station: ")
    time = input("Time (HH:MM): ")
    if not time_is_valid(time):
        print("Invalid time")
        return
    time += ":00"

    date_str = input("Date (YYYY-MM-DD): ")
    
    try:
        day_index = date.fromisoformat(date_str).weekday()
    except:
        print("Invalid date")
        return

    day_today = days[day_index]
    day_tomorrow = days[(day_index + 1) % len(days)]

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
    ''', (day_today, time, day_tomorrow, start_station, end_station))

    rows = cursor.fetchall()
    by_day = {
        day_today: [
            (start_time, end_time)
            for (day, start_time, end_time) in rows
            if day == day_today
        ],
        day_tomorrow: [
            (start_time, end_time)
            for (day, start_time, end_time) in rows
            if day == day_tomorrow
        ],
    }

    for (day, rows) in by_day.items():
        print(f"{day.capitalize()}:")
        for (start_time, end_time) in rows:
            print(f"  {start_station} ({start_time[:-3]}) - {end_station} ({end_time[:-3]})")

    connection.close();

def time_is_valid(time: str) -> bool:
    time_parts = time.split(":")
    if not len(time_parts) == 2: return False
    if not time_parts[0].isdigit(): return False
    if not time_parts[1].isdigit(): return False
    hour = int(time_parts[0])
    minute = int(time_parts[1])
    if hour < 0 or hour >= 24: return False
    if minute < 0 or minute >= 60: return False
    return True


if __name__ == "__main__": main()
