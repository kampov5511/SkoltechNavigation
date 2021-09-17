import os
from io import BytesIO

from PIL import Image
from telebot import types

from db_config import session
from find_route import find_route
from generate_map import generate_map
from db_config import User
from pyzbar_modified import pyzbar
import requests
import telebot

from math import atan2, pi


def get_angle(qrcode):
    poly = qrcode.polygon
    angle = atan2(poly[1].y - poly[0].y, poly[1].x - poly[0].x)
    return angle - pi/2


bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_KEY'), parse_mode=None)


def send_destination_choices(chat_id):
    markup = types.ReplyKeyboardMarkup(row_width=3)
    markup.add(*[types.KeyboardButton(str(i)) for i in range(1, 13)])
    bot.send_message(chat_id=chat_id, text="Choose destination:", reply_markup=markup)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    chat_id = message.chat.id
    if session.query(User.id).filter_by(id=message.from_user.id).first() is not None:
        session.query(User).filter_by(id=message.from_user.id).update({'state': None})
    else:
        user = User(id=message.from_user.id, chat_id=chat_id, state=None)
        session.add(user)
    session.commit()
    send_destination_choices(chat_id)


@bot.message_handler(func=lambda msg: msg.text.isdigit())
def handle_destination(msg):
    location = int(msg.text)
    if 0 > location >= 12:
        bot.send_message(chat_id=msg.chat.id, text='Location is not supported yet!')
        return
    session.query(User).filter_by(chat_id=msg.chat.id).update({'destination': location})
    session.commit()
    bot.send_message(chat_id=msg.chat.id, text='Scan your current location')


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    bot.send_message(chat_id=message.chat.id, text='I am sorry, I do not support this yet...')


@bot.message_handler(func=lambda m: True, content_types=['photo'])
def handle_images(msg):
    url = bot.get_file_url(msg.json['photo'][-1]['file_id'])
    get_qr(url, msg.chat.id, msg.from_user.id)


def get_qr(img_url, user_id, chat_id):
    response = requests.get(img_url)
    img = Image.open(BytesIO(response.content))

    # find and decode QR code
    decoded_codes = pyzbar.decode(img)
    rotation = 0
    if not decoded_codes:
        new_img = img.rotate(45)
        rotation = 45

        decoded_codes = pyzbar.decode(new_img)
        if not decoded_codes:
            bot.send_message(chat_id=chat_id, text='No QR code was found. Please try another image.')
            return

    decoded_qr_code = max(decoded_codes, key=lambda x: x.polygon[0].y)

    if not decoded_qr_code.data.isdigit():
        bot.send_message(chat_id=chat_id, text='Wrong QR code supplied. '
                                                       'Please make sure the code is in the image.')
        return

    orientation_degrees = get_angle(decoded_qr_code) * 180 / pi + rotation

    destination = session.query(User.destination).filter_by(id=user_id, chat_id=chat_id).first()[0]
    source = int(decoded_qr_code.data)
    route = find_route(source, destination)
    generated_map = generate_map(route, -1 * orientation_degrees)

    # todo pass the number of new current location to user
    new_location_state = 3  # todo pass the correct value
    session.query(User).filter_by(id=user_id, chat_id=chat_id).update({'state': new_location_state})
    session.commit()

    bot.send_photo(chat_id=chat_id, photo=generated_map,
                   caption=f'')


bot.polling()
