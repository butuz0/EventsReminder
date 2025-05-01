from django.urls import path
from .views import (
    TeamListAPIView,
    TeamCreateAPIView,
    TeamUpdateAPIView,
    TeamDetailAPIView,
    TeamDeleteAPIView,
    TeamLeaveAPIView,
    InvitationListCreateAPIView,
    InvitationDetailAPIView,
    InvitationRespondAPIView,
    InvitationDeleteAPIView
)

urlpatterns = [
    path('', TeamListAPIView.as_view(), name='team-list'),
    path('create/', TeamCreateAPIView.as_view(), name='team-create'),
    path('<uuid:id>/', TeamDetailAPIView.as_view(), name='team-detail'),
    path('<uuid:id>/update/', TeamUpdateAPIView.as_view(), name='team-update'),
    path('<uuid:id>/delete/', TeamDeleteAPIView.as_view(), name='team-delete'),
    path('<uuid:id>/leave/', TeamLeaveAPIView.as_view(), name='team-leave'),
    path('invitations/', InvitationListCreateAPIView.as_view(), name='invitation-list'),
    path('invitations/create/', InvitationListCreateAPIView.as_view(), name='invitation-create'),
    path('invitations/<uuid:id>/', InvitationDetailAPIView.as_view(), name='invitation-detail'),
    path('invitations/<uuid:id>/respond/', InvitationRespondAPIView.as_view(), name='invitation-respond'),
    path('invitations/<uuid:id>/delete/', InvitationDeleteAPIView.as_view(), name='invitation-delete'),
]
