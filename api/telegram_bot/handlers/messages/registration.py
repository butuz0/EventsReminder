MESSAGES = {
    'start': 'Вітаємо у Telegram-боті від KPI Notify! Ви зможете отримувати нагадування про свої події тут.',
    'no_username': 'У вас немає Telegram username',
    'ask_phone': 'Надішліть свій номер телефону, щоб ми могли вас знайти',
    'verification_successful': 'Ваші дані були успішно верифіковані! Оберіть метод нагадування Telegram, щоб отримувати нагадування про свої події у цьому чаті.',
}

def user_not_found(username=None, phone=None):
    if username:
        return f'Користувача {username} не знайдено. Спробуйте надіслати номер телефону.'
    if phone:
        return f'Не вдалося знайти користувача з номером {phone}.'
    return 'Користувача не знайдено. Спробуйте інший спосіб ідентифікації.'
