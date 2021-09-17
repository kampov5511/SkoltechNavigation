import os
from io import BytesIO

from PIL import Image

from image_direction_generator import MAP_LOCATION_DICT, generate_direction
from find_route import find_route
from pyzbar_modified import pyzbar
import requests
import telebot

from math import atan2, pi


def get_angle(qrcode):
    poly = qrcode.polygon
    angle = atan2(poly[1].y - poly[0].y, poly[1].x - poly[0].x)
    return angle - pi/2


bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_KEY'), parse_mode=None)


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    return
    """ Welcoming message
    bot.send_sticker(chat_id=message.chat.id,
                     data='CAACAgIAAxkBAAEC4dhhOy88-VPaB1GkzHAhsnsw4GYwzQADAQACsJjjAxT0jjvVJ8VKIAQ')
    """

@bot.message_handler(func=lambda m: True)
def echo_all(message):
    bot.reply_to(message, message.text)
    bot.send_message(chat_id=message.chat.id, text='I am sorry, I do not support this yet...')


@bot.message_handler(func=lambda m: True, content_types=['photo'])
def get_qr_code(message):
    # read image
    url = bot.get_file_url(message.json['photo'][-1]['file_id'])
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # arr = np.asarray(bytearray(response.content), dtype=np.uint8)
    # img = cv2.imdecode(arr, -1)  # 'Load it as it is'

    # find and decode QR code
    decoded_codes = pyzbar.decode(img)
    rotation = 0
    if not decoded_codes:
        new_img = img.rotate(45)
        rotation = 45
        # new_img.show()

        decoded_codes = pyzbar.decode(new_img)
        if not decoded_codes:
            bot.send_message(chat_id=message.chat.id, text='No QR code was found. Please try another image.')
            return

    """ Check that one qr code
    if len(decoded_codes) > 1:
        bot.send_message(chat_id=message.chat.id, text='Several QR codes were found. '
                                                       'Please make sure only one code is in the image.')
        return
    """

    decoded_qr_code = max(decoded_codes, key=lambda x: x.polygon[0].y)

    if not decoded_qr_code.data.isdigit():
        bot.send_message(chat_id=message.chat.id, text='Wrong QR code supplied. '
                                                       'Please make sure the code is in the image.')
        return

    orientation_degrees = get_angle(decoded_qr_code) * 180 / pi + rotation

    destination = 15 # Change it with tg-bot state
    source = int(decoded_qr_code.data)
    route = find_route(source, destination)

    map_location = MAP_LOCATION_DICT[int(decoded_qr_code.data)]
    new_direction = generate_direction(map_location, orientation_degrees)

    bot.send_photo(chat_id=message.chat.id, photo=new_direction,
                   caption=f'QR code angle is {round(orientation_degrees, 1)} degrees. '
                           f'Please proceed according to the map.')


bot.polling()
