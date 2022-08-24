from tickets_booking_app.app.dbmanager import DbManager

db = DbManager(file_name='../db/cinema.db')
cinema_db = db.get_db()
seat_table = db.get_table(table_name='Seat')


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
