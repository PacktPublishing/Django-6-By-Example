from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User, Conversation, Message

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    pass


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ["created_at"]


@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ["title", "user", "updated_at"]
    list_select_related = ["user"]
    search_fields = ["title", "user__username"]
    inlines = [MessageInline]
