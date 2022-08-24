from tickets_booking_app.card import Card
from tickets_booking_app.seat import Seat
from tickets_booking_app.user import User

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
