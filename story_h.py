import sqlite3
'''
h) All information about purchases made for future trips should be available for a user. This
functionality should be programmed.
'''

def main():
    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    

    connection.close();

if __name__ == "__main__": main()
