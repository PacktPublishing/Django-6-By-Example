from django.urls import path

from . import views

app_name = "chat"

urlpatterns = [
    path("", views.conversation_list, name="conversation_list"),
    path("conversations/new/", views.conversation_create, name="conversation_create"),
    path("conversations/<str:pk>/", views.conversation_detail, name="conversation_detail"),
    path("conversations/<str:pk>/messages/", views.message_create, name="message_create"),
]
