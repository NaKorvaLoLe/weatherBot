import telebot
from pyowm import OWM
from pyowm.utils.config import get_default_config
import random
import settings

config_dict = get_default_config()
config_dict['language'] = 'ru'

owm = OWM(settings.API_KEY_WEATHER, config_dict)
mgr = owm.weather_manager()
bot = telebot.TeleBot(settings.API_KEY_BOT, parse_mode=None)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.from_user.id, "В каком городе хотите узнать погоду?")

@bot.message_handler(content_types=['text'])
def send_echo(message):
    try:
        observation = mgr.weather_at_place(message.text)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        status = w.detailed_status
        degree = ''
        if temp < 0:
            degree = 'градусов меньше нуля'
        elif temp > 0:
            degree = 'градусов больше нуля'
        else:
            degree = 'градусов'

        advice = ''
        if temp < 0:
            advice = 'Ваще дубак 🥶. Оденься, как танк!'
        elif temp < 10:
            advice = 'Сейчас холодно. Оденься по теплее!'
        elif temp < 20:
            advice = 'Прохладненько. Оденься!'
        elif temp < 25:
            advice = 'Сегодня тепло. Одевайся полегче👕.'
        elif temp > 25:
            advice = 'Ну и жаришка!🥵Возьми водичку!'



        answer = (f"В городе {message.text} сейчас {status}, {temp} {degree}. \n{advice}")
        bot.send_message(message.chat.id, answer)
    except:
        answer = [
            "Что это такое😠. \n Я не знаю такого города!",
            "Дружочек-пирожочек, введи пожалуйста верно свой город😇",
            "Пу-пу-пум, что то пошло не так😬",
            "Вы ввели неверное значение,попытайтесь снова. Я уверен , вы справитесь с этой задачей 💪 ",

        ]
        random_answer = random.randint(0, len(answer) - 1)
        bot.send_message(message.chat.id, answer[random_answer])
bot.polling(none_stop = True)
