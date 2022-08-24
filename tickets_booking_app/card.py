from sqlalchemy import create_engine, MetaData, Table

banking_db_path = "C:\\Users\\RomanBarabash\\PycharmProjects\\oop_apps\\tickets_booking_app\\banking.db"
banking_db = create_engine(f'sqlite:///{banking_db_path}', echo=True)
banking_db_metadata = MetaData()
card_table = Table('Card', banking_db_metadata, autoload=True, autoload_with=banking_db)


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
