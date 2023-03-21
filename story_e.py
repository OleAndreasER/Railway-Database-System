import sqlite3
from sqlite3 import Cursor 
import re
'''
e) En bruker skal kunne registrere seg i kunderegisteret. Denne funksjonaliteten skal programmeres.
'''

def main():
    # User inputs
    name = input('name: ')    
    email = input('email: ')    
    mobile_nr = input('mobileNr: ')    

    # Validation
    if not email_is_valid(email):
        print("Invalid email")
        return
    if not mobile_nr_is_valid(mobile_nr):
        print("Invalid mobileNr")
        return

    # Add new Customer
    connection = sqlite3.connect("railwaySystem.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT INTO Customer (name, email, mobileNr) VALUES (?, ?, ?)",
        (name, email, mobile_nr)
    )
    customer_id = cursor.lastrowid
    connection.commit()
    connection.close();

    print("Added:", (customer_id, name, email, mobile_nr))


valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def email_is_valid(email: str) -> bool:
    return re.fullmatch(valid_email, email)

#https://www.epinova.no/folg-med/blogg/2020/regex-huskeliste-for-norske-formater-i-episerver-forms/
valid_mobile_nr = r'^((0047)?|(\+47)?)[4|9]\d{7}$'
def mobile_nr_is_valid(mobile_nr: str) -> bool:
    return re.fullmatch(valid_mobile_nr, mobile_nr)

if __name__ == "__main__": main()
