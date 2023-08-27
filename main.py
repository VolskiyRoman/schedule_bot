import telebot
import webbrowser
from telebot import types


class Schedule:
    def __init__(self, first_week, second_week):
        self.first_week = first_week
        self.second_week = second_week
        self.current_week = first_week

    def get_schedule(self, week):
        schedule_text = ''
        if self.current_week == self.first_week:
            schedule_text += f"Розклад першого тижня:\n"
        elif self.current_week == self.second_week:
            schedule_text += f"Розклад другого тижня:\n"
        for day, subjects in week.items():
            schedule_text += f"{day}:\n"
            for order, subject in subjects.items():
                schedule_text += f"{order}: {subject}\n"
            schedule_text += '\n'
        return schedule_text


class Bot:
    def __init__(self, token, schedule):
        self.bot = telebot.TeleBot(token)
        self.schedule = schedule

    def create_menu_markup(self):
        markup = types.InlineKeyboardMarkup(row_width=1)
        website_button = types.InlineKeyboardButton('Перейти на сайт', callback_data='website')
        schedule_button = types.InlineKeyboardButton('Мій розклад', callback_data='schedule')
        change_week = types.InlineKeyboardButton('Змінити тиждень', callback_data='change_schedule')
        emails_button = types.InlineKeyboardButton('Список електронних адрес', callback_data='email')
        lesson_links = types.InlineKeyboardButton('Список посилань на пари', callback_data='lesson_links')
        markup.add(website_button, schedule_button, change_week, emails_button, lesson_links)
        return markup

    def global_init(self):
        @self.bot.message_handler(commands=['start'])
        def start(message):
            markup = self.create_menu_markup()
            self.bot.send_message(message.chat.id, f'Привіт, {message.from_user.first_name}!', reply_markup=markup)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'website')
        def handle_website_callback(call):
            self.handle_website_button(call.message)
            self.main_menu(call.message)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'schedule')
        def handle_schedule_callback(call):
            self.handle_schedule_button(call.message)
            self.main_menu(call.message)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'change_schedule')
        def handle_change_schedule_callback(call):
            self.handle_change_week(call.message)
            self.main_menu(call.message)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'email')
        def handle_email_callback(call):
            self.handle_email_week(call.message)
            self.main_menu(call.message)

        @self.bot.callback_query_handler(func=lambda call: call.data == 'lesson_links')
        def handle_lesson_links_callback(call):
            self.handle_lesson_links(call.message)
            self.main_menu(call.message)

        self.bot.polling(none_stop=True)

    def handle_website_button(self, message):
        webbrowser.open('http://roz.kpi.ua/')

    def handle_schedule_button(self, message):
        schedule_text = self.schedule.get_schedule(self.schedule.current_week)
        self.bot.send_message(message.chat.id, schedule_text)

    def handle_change_week(self, message):
        if self.schedule.current_week == self.schedule.first_week:
            self.schedule.current_week = self.schedule.second_week
        else:
            self.schedule.current_week = self.schedule.first_week
        self.bot.send_message(message.chat.id, "Тиждень змінено!")

    def handle_email_week(self, message):
        emails_str = ""
        for name, email in emails.items():
            emails_str += f"{name}: {email}\n"
        self.bot.send_message(message.chat.id, f"Список email адрес:\n{emails_str}")

    def handle_lesson_links(self, message):
        lesson_str = ""
        for name, link in lesson_links.items():
            lesson_str += f"{name}: {link}\n"
        self.bot.send_message(message.chat.id, f"Список посилань на пари:\n{lesson_str}")

    def main_menu(self, message):
        markup = self.create_menu_markup()
        text = "Ось ваше головне меню:"
        self.bot.send_message(message.chat.id, text, reply_markup=markup)


if __name__ == "__main__":
    my_schedule_first_week = {
        'Понеділок': {},
        'Вівторок': {'8:30': 'Правознавство', '10:25': 'Паралельне програмування',
                     '12:20': '''Архітектура комп'ютерів''', '16:10': 'Front-end'},
        'Середа': {'8:30': 'AGILE', '10:25': 'Штучний інтелект', '12:20': 'Data science'},
        'Четвер': {'21:35': 'Англійська', '14:15': '''Архітектура комп'ютерів''', '16:10': 'Англійська'},
        "П'ятниця": {},
        'Субота': {},
        'Неділя': {}
    }

    my_schedule_second_week = {
        'Понеділок': {},
        'Вівторок': {'10:25': 'Паралельне програмування', '12:20': '''Архітектура комп'ютерів''', '16:10': 'Front-end'},
        'Середа': {'8:30': 'AGILE', '10:25': 'Штучний інтелект', '12:20': 'Data science'},
        'Четвер': {'10:25': 'Англійська', '12:20': 'Правознавство', '14:15': 'Паралельне програмування',
                   '16:10': 'Англійська'},
        "П'ятниця": {},
        'Субота': {},
        'Неділя': {}
    }

    emails = {
        "Вася": "vasyapupkin32@gmail.com",
        "Петя": "petyapetrov@gmail.com",
        "Катя": "katyasmith@gmail.com",
        "Оля": "olyaivanova@gmail.com",
        "Іван": "ivanov.ivan@gmail.com",
        "Марія": "mariyapetrova@gmail.com"
    }

    lesson_links = {
        "Урок 1": "https://example.com/lesson1",
        "Урок 2": "https://example.com/lesson2",
        "Урок 3": "https://example.com/lesson3",
        "Урок 4": "https://example.com/lesson4",
        "Урок 5": "https://example.com/lesson5"
    }

    schedule = Schedule(my_schedule_first_week, my_schedule_second_week)
    bot = Bot('6345985846:AAG1uhFPwX9vDkqqrP3Xab4sEOj95qxfP2w', schedule)
    bot.global_init()


