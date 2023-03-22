import sqlite3
'''
g) Registered customers should be able to find available tickets for a desired train route and
purchase the tickets they would like. This functionality should be programmed.
• Make sure to only sell available seats.
'''

def main():
    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    

    connection.close();

if __name__ == "__main__": main()
