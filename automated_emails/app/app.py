import datetime
from threading import Timer

import pandas
import yagmail

from automated_emails.app.config import USER_EMAIL, PASSWORD
from automated_emails.app.news import NewsFeed


def get_contacts_table():
    return pandas.read_excel('data\contacts.xlsx')


def get_news_feed(row, from_date, to_date):
    return NewsFeed(interest=row['interest'], from_date=from_date, to_date=to_date) \
        .get_email_body()


def get_email(user, password):
    return yagmail.SMTP(user=user, password=password)


def send_emails_to_contacts():
    for index, row in get_contacts_table().iterrows():
        today = datetime.datetime.now().strftime('%Y-%m-%d')
        yesterday = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime('%Y-%m-%d')

        get_email(USER_EMAIL, PASSWORD) \
            .send(to=row['email'],
                  subject=f"Your {row['interest']} news for today!",
                  contents=f"Hi {row['name']}\n\n "
                           f"See what's on about {row['interest']} today.\n\n"
                           f"{get_news_feed(row, yesterday, today)}\nRoman")


x = datetime.datetime.today()
y = x.replace(day=x.day, hour=9, minute=0, second=0, microsecond=0) + datetime.timedelta(days=1)
delta_t = y - x
secs = delta_t.total_seconds()

t = Timer(secs, send_emails_to_contacts)
t.start()
