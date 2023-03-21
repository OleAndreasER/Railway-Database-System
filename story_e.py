import sqlite3
from sqlite3 import Cursor 
import re
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
    phone_nr: str,
    cursor: Cursor
):
    if not email_is_valid(email): return
    if not phone_nr_is_valid(phone_nr): return

valid_email = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
def email_is_valid(email: str) -> bool:
    return re.fullmatch(valid_email, email)

#https://www.epinova.no/folg-med/blogg/2020/regex-huskeliste-for-norske-formater-i-episerver-forms/
valid_phone_nr = r'^((0047)?|(\+47)?)[4|9]\d{7}$'
def phone_nr_is_valid(phone_nr: str) -> bool:
    return re.fullmatch(valid_phone_nr, phone_nr)

if __name__ == "__main__": main()
