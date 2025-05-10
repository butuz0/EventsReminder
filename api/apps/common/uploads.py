import os
import uuid


def upload_event_image(instance, filename):
    extension = os.path.splitext(filename)[1]
    return os.path.join('event_images/', f'{uuid.uuid4()}{extension}')


def upload_avatar(instance, filename):
    extension = os.path.splitext(filename)[1]
    return os.path.join('avatars/', f'{uuid.uuid4()}{extension}')
