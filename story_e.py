import sqlite3
from sqlite3 import Cursor 
'''
e) En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.
'''

def main():
    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    

    connection.close();

def register_customer(
    name: str,
    email: str,
    phoneNr: str,
    cursor: Cursor
):
    #Validate email and phoneNr
    return

if __name__ == "__main__": main()
