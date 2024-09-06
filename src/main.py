# Импортируем пакеты
from datetime import datetime
import locale
locale.setlocale (
  category = locale.LC_ALL,
  locale = "Russian"
)
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils import executor
from aiogram_datepicker import Datepicker, DatepickerSettings

# Устанавливаем токен бота
API_TOKEN = "7501903523:AAFE9MIpzZ7sRY655iNrFoHZ27CXASCqya4"

# Создаем объекты бота и диспетчера
bot = Bot(token = API_TOKEN)
dp = Dispatcher(bot, run_tasks_by_default = True)

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


# Создание разметки клавиатуры
kb = InlineKeyboardMarkup(row_width=5)

# Создание кнопок с цифрами от 1 до 6
# number_buttons = [InlineKeyboardButton(text = str(i), callback_data = f'num_{i}') for i in range(1, 7)]

# Создание кнопок
time_buttons = [
  InlineKeyboardButton(text = "Пара / Время", callback_data = "time_0"),
  InlineKeyboardButton(text = "1. 08:00-09:40", callback_data = "time_1"),
  InlineKeyboardButton(text = "2. 08:00-09:40", callback_data = "time_2"),
  InlineKeyboardButton(text = "3. 08:00-09:40", callback_data = "time_3"),
  InlineKeyboardButton(text = "4. 08:00-09:40", callback_data = "time_4"),
  InlineKeyboardButton(text = "5. 08:00-09:40", callback_data = "time_5"),
  InlineKeyboardButton(text = "6. 08:00-09:40", callback_data = "time_6"),
]

# Создание кнопок
discipline_buttons = [
  InlineKeyboardButton(text = "Дисциплина", callback_data = "discipline_0"),
  InlineKeyboardButton(text = "Компьютерные сети", callback_data = "discipline_1"),
  InlineKeyboardButton(text = "Английский", callback_data = "discipline_2"),
  InlineKeyboardButton(text = " ", callback_data = "discipline_3"),
  InlineKeyboardButton(text = "Биология", callback_data = "discipline_4"),
  InlineKeyboardButton(text = "География", callback_data = "discipline_5"),
  InlineKeyboardButton(text = " ", callback_data = "discipline_6"),
]

# Создание кнопок
teacher_buttons = [
  InlineKeyboardButton(text = "Преподаватель", callback_data = "teacher_0"),
  InlineKeyboardButton(text = "Фамилия И.О.", callback_data = "teacher_1"),
  InlineKeyboardButton(text = "Фамилия И.О.", callback_data = "teacher_2"),
  InlineKeyboardButton(text = " ", callback_data = "teacher_3"),
  InlineKeyboardButton(text = "Фамилия И.О.", callback_data = "teacher_4"),
  InlineKeyboardButton(text = "Фамилия И.О.", callback_data = "teacher_5"),
  InlineKeyboardButton(text = " ", callback_data = "teacher_6"),
]

# Создание кнопок
cabinet_buttons = [
  InlineKeyboardButton(text = "Аудитория", callback_data = "cabinet_0"),
  InlineKeyboardButton(text = "303", callback_data = "cabinet_1"),
  InlineKeyboardButton(text = "311/203", callback_data = "cabinet_2"),
  InlineKeyboardButton(text = " ", callback_data = "cabinet_3"),
  InlineKeyboardButton(text = "дис.", callback_data = "cabinet_4"),
  InlineKeyboardButton(text = "дис.", callback_data = "cabinet_5"),
  InlineKeyboardButton(text = " ", callback_data = "cabinet_6"),
]

# Объединение кнопок в разметку
for i in range(7):
  kb.add(time_buttons[i], discipline_buttons[i], teacher_buttons[i], cabinet_buttons[i])


# Запуск бота (/start)
@dp.message_handler(commands = ["start"])
async def send_welcome(message: Message):
  await message.answer("Укажите группу для просмотра расписания пар:")


# Обработка колбеков
@dp.callback_query_handler(lambda call: call.data.startswith("teacher_"))
async def handle_teacher_button(call: types.CallbackQuery):
  teacher_number = call.data.split('_')[1]
  response_text = ""
  if teacher_number == '1' and True:
    response_text = "Фамилия Имя Отчество"
  elif teacher_number == '2' and True:
    response_text = "Фамилия Имя Отчество"
  elif teacher_number == '3' and False:
    response_text = ""
  elif teacher_number == '4' and True:
    response_text = "Фамилия Имя Отчество"
  elif teacher_number == '5' and True:
    response_text = "Фамилия Имя Отчество"
  elif teacher_number == '6' and False:
    response_text = ""
  await call.answer(response_text)
  await call.message.answer(response_text)


# Обработка колбеков
@dp.callback_query_handler(lambda call: call.data.startswith("discipline_"))
async def handle_discipline_button(call: types.CallbackQuery):
  discipline_number = call.data.split('_')[1]
  response_text = ""
  if discipline_number == '1' and True:
    response_text = "ОП.11 Компьютерные сети"
  elif discipline_number == '2' and True:
    response_text = "ОУД.13 Английский"
  elif discipline_number == '3' and False:
    response_text = ""
  elif discipline_number == '4' and True:
    response_text = "ОУД.08 Биология"
  elif discipline_number == '5' and True:
    response_text = "ОУД.09 География"
  elif discipline_number == '6' and False:
    response_text = ""
  await call.answer(response_text)
  await call.message.answer(response_text)


@dp.callback_query_handler(Datepicker.datepicker_callback.filter())
async def _process_datepicker(callback_query: CallbackQuery, callback_data: dict):
  global group_name
  datepicker = Datepicker(_get_datepicker_settings())
  _date = await datepicker.process(callback_query, callback_data)
  if _date:
    if group_name != None:
      await callback_query.message.answer(f'Расписание для группы {group_name} на {_date.strftime("%d.%m.%Y")}:', reply_markup=kb)
  await callback_query.answer()


@dp.message_handler()
async def echo(message: Message):
  global group_name
  datepicker = Datepicker(_get_datepicker_settings())
  markup = datepicker.start_calendar()
  if False:
    await message.answer(f'Группа {message.text} не найдена (если в наименовании группы присутствуют буквы - используйте кириллицу, без пробелов)')
  else:
    group_name = message.text
    await message.answer("Выберете дату: ", reply_markup=markup)


if __name__ == "__main__":
  executor.start_polling(dp, skip_updates = True)