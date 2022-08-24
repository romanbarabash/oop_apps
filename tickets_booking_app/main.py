import random
import string

from fpdf import FPDF
from sqlalchemy import create_engine, MetaData, Table

banking_db_path = "C:\\Users\\RomanBarabash\\PycharmProjects\\oop_apps\\tickets_booking_app\\banking.db"
banking_db = create_engine(f'sqlite:///{banking_db_path}', echo=True)
banking_db_metadata = MetaData()
card_table = Table('Card', banking_db_metadata, autoload=True, autoload_with=banking_db)

cinema_db_path = "C:\\Users\\RomanBarabash\\PycharmProjects\\oop_apps\\tickets_booking_app\\cinema.db"
cinema_db = create_engine(f'sqlite:///{cinema_db_path}', echo=True)
cinema_db_metadata = MetaData()
seat_table = Table('Seat', cinema_db_metadata, autoload=True, autoload_with=cinema_db)


class User:
    """Represents a user that can buy a cinema Seat"""

    def __init__(self, name):
        self.name = name

    def buy(self, seat, card):
        """Buys the ticket if the card is valid"""
        if seat.is_free():
            if card.validate(price=seat.get_price()):
                seat.occupy()
                ticket = Ticket(user=self, price=seat.get_price(), seat_number=seat.seat_id)
                ticket.to_pdf()
                return "Purchase successful!"
            else:
                return "There was a problem with your card!"
        else:
            return "Seat is taken!"


class Seat:
    """Represents a cinema seat that can be taken from a User"""

    def __init__(self, seat_id):
        self.seat_id = seat_id

    def get_price(self):
        """Get the price of a certain seat"""
        with cinema_db.connect() as conn:
            seat_row = conn.execute(seat_table
                                    .select()
                                    .where(seat_table.c.seat_id == self.seat_id))

            price = [int(item._data[2]) for item in seat_row][0]

        return price

    def is_free(self):
        """Check in the database if a Seat is taken or not"""
        with cinema_db.connect() as conn:
            seat_row = conn.execute(seat_table
                                    .select()
                                    .where(seat_table.c.seat_id == self.seat_id))

            is_taken = [int(item._data[1]) for item in seat_row][0]

        if is_taken == 0:
            return True
        else:
            return False

    def occupy(self):
        """Change value of taken in the database from 0 to 1 if Seat is free"""
        with cinema_db.connect() as conn:
            update_query = seat_table \
                .update() \
                .where(seat_table.c.seat_id == self.seat_id) \
                .values(taken=1)
            conn.execute(update_query)


class Card:
    """ Represents a bank card needed to finalize a Seat purchase"""

    database = "banking.db"

    def __init__(self, type, number, cvc, holder):
        self.holder = holder
        self.cvc = cvc
        self.number = number
        self.type = type

    def validate(self, price):
        """Checks if Card is valid and has balance. Subtracts price from balance.
        """

        with banking_db.connect() as conn:
            card_row = conn.execute(card_table
                                    .select()
                                    .where(card_table.c.number == self.number))

            balance = [int(item._data[4]) for item in card_row][0]

            if balance >= price:
                update_query = card_table \
                    .update() \
                    .where(card_table.c.number == self.number) \
                    .values(balance=balance - price)
                conn.execute(update_query)
                return True


class Ticket:
    """Represents a cinema Ticket purchased by a User"""

    def __init__(self, user, price, seat_number):
        self.user = user
        self.price = price
        self.id = "".join([random.choice(string.ascii_letters) for i in range(8)])
        self.seat_number = seat_number

    def to_pdf(self):
        """Creates a PDF ticket"""
        pdf = FPDF(orientation='P', unit='pt', format='A4')
        pdf.add_page()

        pdf.set_font(family="Times", style="B", size=24)
        pdf.cell(w=0, h=80, txt="Your Digital Ticket", border=1, ln=1, align="C")

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Name: ", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.user.name, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Ticket ID", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=self.id, border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Price", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=str(self.price), border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.set_font(family="Times", style="B", size=14)
        pdf.cell(w=100, h=25, txt="Seat Number", border=1)
        pdf.set_font(family="Times", style="", size=12)
        pdf.cell(w=0, h=25, txt=str(self.seat_number), border=1, ln=1)
        pdf.cell(w=0, h=5, txt="", border=0, ln=1)

        pdf.output("sample.pdf", 'F')


if __name__ == "__main__":
    # name = input("Your full name: ")
    # seat_id = input("Preferred seat number: ")
    # card_type = input("Your card type: ")
    # card_number = input("Your card number: ")
    # card_cvc = input("Your card cvc: ")
    # card_holder = input("Card holder name: ")

    name = 'roman'
    seat_id = 'B5'
    card_type = 'Visa'
    card_number = 12345678
    card_cvc = 123
    card_holder = 'John Smith'

    user = User(name=name)
    seat = Seat(seat_id=seat_id)
    card = Card(type=card_type, number=card_number, cvc=card_cvc, holder=card_holder)

    print(user.buy(seat=seat, card=card))
