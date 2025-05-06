from datetime import datetime

DAYS = {
    0: 'Понеділок',
    1: 'Вівторок',
    2: 'Середа',
    3: 'Четвер',
    4: 'Пʼятниця',
    5: 'Субота',
    6: 'Неділя',
}

MONTHS = {
    1: 'січня',
    2: 'лютого',
    3: 'березня',
    4: 'квітня',
    5: 'травня',
    6: 'червня',
    7: 'липня',
    8: 'серпня',
    9: 'вересня',
    10: 'жовтня',
    11: 'листопада',
    12: 'грудня',
}


def format_datetime(date: datetime) -> str:
    weekday = DAYS[date.weekday()]
    day = date.day
    month = MONTHS[date.month]
    year = date.year
    time = date.strftime('%H:%M')

    return f'{weekday}, {day} {month} {year} року, о {time}'
