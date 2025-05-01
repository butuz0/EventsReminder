from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from apps.common.models import TimeStampedModel

User = get_user_model()


class Team(TimeStampedModel):
    name = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_teams', verbose_name=_('Created By'))
    members = models.ManyToManyField(User, related_name='teams', blank=True, verbose_name=_('Members'))
    description = models.TextField(blank=True, null=True, verbose_name=_('Description'))

    def __str__(self):
        return f'{self.name} - {self.created_by}'

    class Meta:
        verbose_name = 'Team'
        verbose_name_plural = 'Teams'
        indexes = [
            models.Index(fields=['created_by']),
        ]


class Invitation(TimeStampedModel):
    class Status(models.TextChoices):
        PENDING = 'p', 'Pending'
        ACCEPTED = 'a', 'Accepted'
        REJECTED = 'r', 'Rejected'
    
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_invitations', verbose_name=_('Created By'))
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='invitations', verbose_name=_('Team'))
    sent_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_invitations', verbose_name=_('Sent To'))
    status = models.CharField(max_length=5, choices=Status.choices, default=Status.PENDING, blank=True, verbose_name=_('Status'))
    
    def __str__(self):
        return f'{self.sent_to} - {self.team}'

    class Meta:
        verbose_name = 'Invitation'
        verbose_name_plural = 'Invitations'
