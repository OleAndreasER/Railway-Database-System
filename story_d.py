import sqlite3
from sqlite3 import Cursor 
import re
from datetime import date
'''
d) Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
returneres, sortert på tid. Denne funksjonaliteten skal programmeres.
'''
weekdays = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
]

def main():
    time = input("Time (HH:MM): ")
    if not time_is_valid(time):
        print("Invalid time")
        return
    time += ":00"

    dateStr = input("Date (YYYY-MM-DD): ")
    
    try:
        weekdayIndex = date.fromisoformat(dateStr).weekday()
    except:
        print("Invalid date")
        return

    weekdayToday = weekdays[weekdayIndex]
    weekdayTomorrow = weekdays[(weekdayIndex + 1) % len(weekdays)]

    print(time)
    print(weekdayToday)
    print(weekdayTomorrow)

    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()

    #query

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
