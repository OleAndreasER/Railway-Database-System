import sqlite3
from sqlite3 import Cursor 
'''
d) Bruker skal kunne søke etter togruter som går mellom en startstasjon og en sluttstasjon, med
utgangspunkt i en dato og et klokkeslett. Alle ruter den samme dagen og den neste skal
returneres, sortert på tid. Denne funksjonaliteten skal programmeres.
'''

def main():
    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    

    connection.close();


def get_train_routes(
    start_station: str,
    end_station: str,
    date: str,
    time: str,
    cursor: Cursor
) -> list:
    # list is the return type of cursor.fetchall()
    return []

if __name__ == "__main__": main()
