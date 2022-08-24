from tickets_booking_app.app.db_manager import DbManager

db = DbManager(file_name='../db/banking.db')
banking_db = db.get_db()
card_table = db.get_table(table_name='Card')


class Card:
    """ Represents a bank card needed to finalize a Seat purchase"""

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
