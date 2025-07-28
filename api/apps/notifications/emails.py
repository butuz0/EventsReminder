from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from apps.registration_cards.models import RegistrationCard
from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL, DOMAIN
from apps.events.models import Event


def send_event_notification_email(user, event: Event) -> None:
    subject = f'Нагадування про подію: {event.title}'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    context = {
        'user': user,
        'event': event,
        'domain': DOMAIN,
        'site_name': SITE_NAME
    }

    html_email = render_to_string('notifications/event_notification_email.html', context)
    text_email = render_to_string('notifications/event_notification_email.txt', context)

    email = EmailMultiAlternatives(subject, text_email, from_email, recipient_list)
    email.attach_alternative(html_email, 'text/html')
    email.send()


def send_reg_card_notification_email(user, reg_card: RegistrationCard) -> None:
    subject = f'Нагадування про сертифікат електронного підпису: {reg_card.full_name}'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    context = {
        'user': user,
        'reg_card': reg_card,
        'domain': DOMAIN,
        'site_name': SITE_NAME
    }

    html_email = render_to_string('notifications/reg_card_notification_email.html', context)
    text_email = render_to_string('notifications/reg_card_notification_email.txt', context)

    email = EmailMultiAlternatives(subject, text_email, from_email, recipient_list)
    email.attach_alternative(html_email, 'text/html')
    email.send()
