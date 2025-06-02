from django.db import models
from celery.result import AsyncResult
from typing import Callable
from datetime import datetime


def reschedule_celery_task(
        instance: models.Model,
        celery_task: Callable,
        task_args: list,
        eta: datetime,
        task_id_field: str = 'celery_task_id',
        save: bool = True
) -> None:
    task_id = getattr(instance, task_id_field, None)

    if task_id:
        result = AsyncResult(task_id)
        if result.status in ['PENDING', 'RECEIVED', 'STARTED', 'RETRY']:
            result.revoke(terminate=True)

    new_task = celery_task.apply_async(args=task_args, eta=eta)
    setattr(instance, task_id_field, new_task.id)

    if save:
        instance.save(update_fields=[task_id_field])
