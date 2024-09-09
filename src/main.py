# Импортируем пакеты
from datetime import datetime
import locale
locale.setlocale (
  category = locale.LC_ALL,
  locale = "Russian"
)
from aiogram import Bot, Dispatcher
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram_datepicker import Datepicker, DatepickerSettings
import sqlite3

# Устанавливаем токен бота
API_TOKEN = "7501903523:AAFE9MIpzZ7sRY655iNrFoHZ27CXASCqya4"

# Создаем объекты бота и диспетчера
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot, run_tasks_by_default = True)

# Подключаемся к бд
connection = sqlite3.connect('db/database.db')
cursor = connection.cursor()

# Конфиг для календаря
def _get_datepicker_settings():
  return DatepickerSettings(
    initial_view = "day",
    initial_date = datetime.now().date(),
    views = {
      "day": {
        "show_weekdays": True,
        "weekdays_labels": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
        "header": ["days-title"],
        "footer": ["prev-month", "next-month"],
      },
      "month": {
        "months_labels": ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"],
        "header": ["year"],
        "footer": []
      },
      "year": {
        "header": [],
        "footer": ["prev-years", "next-years"]
      }
    },
    labels = {
      "prev-years": "⬅",
      "next-years": "➡",
      "prev-month": "⬅",
      "next-month": "➡",
      "days-title": "📆 {month} {year}",
      "selected-day": "{day}",
      "selected-month": "{month}",
      "present-day": "{day}",
    },
    custom_actions = []
  )


# Имя группы
group_name = None

# Дата расписания
schedule_date = None

# Создание разметки клавиатуры
kb = InlineKeyboardMarkup(row_width=5)


# Запуск бота (/start)
@dp.message_handler(commands = ["start"])
async def send_welcome(message: Message):
  await message.answer("Укажите группу для просмотра расписания пар:")


# Получить кнопки времени
def get_time_buttons():
  global group_name
  global schedule_date
  time_buttons = [InlineKeyboardButton(text = "Пара / Время", callback_data = "time_0")]
  for i in range(1, 7):
    cursor.execute(f'SELECT Время_начала FROM Пары WHERE id = (SELECT Пара_{i}_id FROM Расписание WHERE id = (SELECT Даты.Расписание_id FROM Даты JOIN Группы ON Даты.id = Группы.Дата_id AND Группы.Группа = \'{group_name}\' AND Даты.Дата = \'{schedule_date}\'))')
    start_time = cursor.fetchone()[0]
    cursor.execute(f'SELECT Время_окончания FROM Пары WHERE id = (SELECT Пара_{i}_id FROM Расписание WHERE id = (SELECT Даты.Расписание_id FROM Даты JOIN Группы ON Даты.id = Группы.Дата_id AND Группы.Группа = \'{group_name}\' AND Даты.Дата = \'{schedule_date}\'))')
    end_time = cursor.fetchone()[0]
    time_buttons.append(InlineKeyboardButton(text = f'{i}. {start_time}-{end_time}', callback_data = f'time_{i}'))
  return time_buttons


# Получить кнопки дисциплины
def get_discipline_buttons():
  global group_name
  global schedule_date
  discipline_buttons = [InlineKeyboardButton(text = "Дисциплина", callback_data = "discipline_0")]
  for i in range(1, 7):
    cursor.execute(f'SELECT Дисциплина FROM Дисциплины WHERE id = (SELECT Дисциплина_id FROM Пары WHERE id = (SELECT Пара_{i}_id FROM Расписание WHERE id = (SELECT Даты.Расписание_id FROM Даты JOIN Группы ON Даты.id = Группы.Дата_id AND Группы.Группа = \'{group_name}\' AND Даты.Дата = \'{schedule_date}\')))')
    discipline = cursor.fetchone()
    if discipline == None:
      discipline_buttons.append(InlineKeyboardButton(text = " ", callback_data = f'discipline_0'))
    else:
      discipline_buttons.append(InlineKeyboardButton(text = discipline[0], callback_data = f'discipline_{i}'))
  return discipline_buttons


# Получить кнопки преподавателей
def get_teacher_buttons():
  global group_name
  global schedule_date
  teacher_buttons = [InlineKeyboardButton(text = "Преподаватели", callback_data = "teacher_0")]
  for i in range(1, 7):
    cursor.execute(f'SELECT Фамилия FROM Преподаватели WHERE id = (SELECT Преподаватель_id FROM Пары WHERE id = (SELECT Пара_{i}_id FROM Расписание WHERE id = (SELECT Даты.Расписание_id FROM Даты JOIN Группы ON Даты.id = Группы.Дата_id AND Группы.Группа = \'{group_name}\' AND Даты.Дата = \'{schedule_date}\')))')
    teacher_surname = cursor.fetchone()
    cursor.execute(f'SELECT Имя FROM Преподаватели WHERE id = (SELECT Преподаватель_id FROM Пары WHERE id = (SELECT Пара_{i}_id FROM Расписание WHERE id = (SELECT Даты.Расписание_id FROM Даты JOIN Группы ON Даты.id = Группы.Дата_id AND Группы.Группа = \'{group_name}\' AND Даты.Дата = \'{schedule_date}\')))')
    teacher_name = cursor.fetchone()
    cursor.execute(f'SELECT Отчество FROM Преподаватели WHERE id = (SELECT Преподаватель_id FROM Пары WHERE id = (SELECT Пара_{i}_id FROM Расписание WHERE id = (SELECT Даты.Расписание_id FROM Даты JOIN Группы ON Даты.id = Группы.Дата_id AND Группы.Группа = \'{group_name}\' AND Даты.Дата = \'{schedule_date}\')))')
    teacher_lastname = cursor.fetchone()
    if teacher_surname == None or teacher_name == None or teacher_lastname == None:
      teacher_buttons.append(InlineKeyboardButton(text = " ", callback_data = f'teacher_0'))
    else:
      teacher_buttons.append(InlineKeyboardButton(text = f'{teacher_surname[0]} {teacher_name[0][0]}. {teacher_lastname[0][0]}.', callback_data = f'teacher_{i}'))
  return teacher_buttons


# Получить кнопки кабинетов
def get_cabinet_buttons():
  global group_name
  global schedule_date
  cabinet_buttons = [InlineKeyboardButton(text = "Аудитория", callback_data = "cabinet_0")]
  for i in range(1, 7):
    cursor.execute(f'SELECT Аудитория FROM Пары WHERE id = (SELECT Пара_{i}_id FROM Расписание WHERE id = (SELECT Даты.Расписание_id FROM Даты JOIN Группы ON Даты.id = Группы.Дата_id AND Группы.Группа = \'{group_name}\' AND Даты.Дата = \'{schedule_date}\'))')
    cabinet = cursor.fetchone()[0]
    if cabinet == None:
      cabinet_buttons.append(InlineKeyboardButton(text = " ", callback_data = f'cabinet_0'))
    else:
      cabinet_buttons.append(InlineKeyboardButton(text = cabinet, callback_data = f'cabinet_{i}'))
  return cabinet_buttons


# Создание и объединение кнопок в разметку (расписание)
def create_schedule():
  global group_name
  global schedule_date

  # Создание разметки клавиатуры
  kb = InlineKeyboardMarkup(row_width=5)

  # Создание кнопок

  # Время начала и окончания пар
  time_buttons = get_time_buttons()

  # Дисциплина
  discipline_buttons = get_discipline_buttons()

  # Преподаватели
  teacher_buttons = get_teacher_buttons()

  # Кабинеты
  cabinet_buttons = get_cabinet_buttons()

  # # Объединение кнопок в разметку
  for i in range(7):
    kb.add(time_buttons[i], discipline_buttons[i], teacher_buttons[i], cabinet_buttons[i])

  return kb


# Выбор даты
@dp.callback_query_handler(Datepicker.datepicker_callback.filter())
async def _process_datepicker(callback_query: CallbackQuery, callback_data: dict):
  global group_name
  global schedule_date
  datepicker = Datepicker(_get_datepicker_settings())
  _date = await datepicker.process(callback_query, callback_data)
  if _date:
    if group_name != None:
      schedule_date = _date.strftime("%Y-%m-%d")
      cursor.execute(f'SELECT Даты.id FROM Даты JOIN Группы ON Даты.id = Группы.Дата_id AND Группы.Группа = \'{group_name}\' AND Даты.Дата = \'{schedule_date}\'')
      schedule = cursor.fetchall()
      if len(schedule) == 0:
        await callback_query.message.answer(f'Расписание для группы {group_name} на {schedule_date} не найдено')
      else:
        await callback_query.message.answer(f'Расписание для группы {group_name} на {schedule_date}:', reply_markup = create_schedule())
  await callback_query.answer()


# Запуск дата-пикера
@dp.message_handler()
async def echo(message: Message):
  global group_name
  datepicker = Datepicker(_get_datepicker_settings())
  markup = datepicker.start_calendar()

  # Поиск группы в бд
  cursor.execute(f'SELECT * FROM Группы WHERE Группа = \'{message.text}\'')
  groups = cursor.fetchall()
  if len(groups) == 0:
    await message.answer(f'Группа {message.text} не найдена (если в наименовании группы присутствуют буквы - используйте кириллицу, без пробелов)')
  else:
    group_name = message.text
    await message.answer("Выберете дату: ", reply_markup=markup)


if __name__ == "__main__":
  executor.start_polling(dp, skip_updates = True)


# Закрываем соединение с бд
connection.close()