from apps.events.models import Event
from telegram_bot.utils.format_date import format_datetime


def generate_event_reminder_text(event: Event) -> str:
    reminder_text = ['Нагадуємо про подію:']

    reminder_text.append(f'<b>{event.title}</b>')

    formatted_datetime = format_datetime(event.start_datetime)
    reminder_text.append(f'Початок: <i>{formatted_datetime}</i>')

    if event.description:
        reminder_text.append(f'{event.description}')

    if event.location:
        reminder_text.append(f'Місце: {event.location}')

    if event.link:
        reminder_text.append(f'<a href="{event.link}">Деталі</a>')

    if event.priority:
        reminder_text.append(f'Пріоритет: {event.get_priority_display()}')

    tags = event.tags.names()
    if tags:
        reminder_text.append(f'Теги: {", ".join(f"#{tag}" for tag in tags)}')

    return '\n'.join(reminder_text)
