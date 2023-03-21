import sqlite3
from sqlite3 import Cursor 
'''
c) For en stasjon som oppgis, skal bruker få ut alle togruter som er innom stasjonen en gitt ukedag.
Denne funksjonaliteten skal programmeres.
'''

def main():
    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    

    connection.close();

def get_train_routes(station_name: str, weekday: str, cursor: Cursor) -> list:
    # list is the return type of cursor.fetchall()
    return []

if __name__ == "__main__": main()
