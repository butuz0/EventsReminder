from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from config.settings.local import SITE_NAME, DEFAULT_FROM_EMAIL, DOMAIN
from apps.events.models import Event


def send_event_notification_email(user, event: Event) -> None:
    subject = f'Notification for {event}'
    from_email = DEFAULT_FROM_EMAIL
    recipient_list = [user.email]

    context = {
        'user': user,
        'event': event,
        'domain': DOMAIN,
        'site_name': SITE_NAME
    }

    html_email = render_to_string('notifications/notification_email.html', context)
    text_email = render_to_string('notifications/notification_email.txt', context)

    email = EmailMultiAlternatives(subject, text_email, from_email, recipient_list)
    email.attach_alternative(html_email, 'text/html')
    email.send()
