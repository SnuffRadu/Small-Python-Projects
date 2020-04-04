import requests                                                                         #1. Ar merge o automatizare ca programul sa se execute automat la un anumit interval de timp
from bs4 import BeautifulSoup                                                           #2. Ar merge si criptare cu SMTP.starttls
import smtplib

URL = "https://www.amazon.de/dp/B07L5LZ9L2/ref=dp_cerb_2"       #link for the amazon product

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}         #local user agent

def check_price():                                  #price check function

    page = requests.get(URL, headers=headers)           #parsing data from the website
    soup = BeautifulSoup(page.content, "html.parser")

    title = soup.find(id = "productTitle").get_text()             #identifying the title of the product we want to parse

    price = soup.find(id = "priceblock_ourprice").get_text()          #identifying the price of the product we want to parse
    converted_price = int(price[0:3])                           #setting the limits of the len of price

    if converted_price > 150:              #if the price is under the set limit, program will send an email
        send_mail()                     #calling the send mail function

        print(converted_price)
        print(title.strip())


def send_mail():

    gmail_user = ' '                       #credentials of test gmail account
    gmail_password = ''                     #password

    sent_from = gmail_user
    to = ['nuffydevtest@gmail.com']                                 #body of the email
    subject = 'Price dropped check email!'
    body = 'check the amazon link: https://www.amazon.de/dp/B07L5LZ9L2/ref=dp_cerb_2\n\n'

    email_text = """\
    From: %s
    To: %s
    Subject: %s

    %s
    """ % (sent_from, ", ".join(to), subject, body)                 #string joining

    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)                #setting up the gmail smtp server
        server.ehlo()
        server.login(gmail_user, gmail_password)                #login with credentials
        server.sendmail(sent_from, to, email_text)              #sending the mail
        server.close()                  #closing the server

        print('Email sent!')
    except:
        print('Price did not drop')

check_price()
send_mail()

