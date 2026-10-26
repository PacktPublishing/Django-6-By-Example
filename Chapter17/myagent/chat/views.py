"""Pages for listing conversations and chatting with the assistant.

Every view works as a plain form post; when htmx sends the request,
it gets back only the HTML fragment to swap instead of a redirect.
"""

import logging

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.text import Truncator
from django.views.decorators.http import require_POST
from google.genai import errors

from .assistant import generate_reply
from .forms import MessageForm
from .models import Conversation, Message

logger = logging.getLogger(__name__)

DETAIL_TEMPLATE = "chat/conversation_detail.html"


def get_own_conversation(request, pk):
    """Return the conversation if it belongs to the current user, else raise 404."""
    return get_object_or_404(Conversation, pk=pk, user=request.user)


def render_detail(request, conversation, form):
    """Render the full conversation page."""
    context = {"conversation": conversation, "chat_messages": conversation.messages.all(), "form": form}
    return render(request, DETAIL_TEMPLATE, context)


@login_required
def conversation_list(request):
    """Show the user's conversations, most recently active first."""
    conversations = request.user.conversations.all()
    return render(request, "chat/conversation_list.html", {"conversations": conversations})


@login_required
@require_POST
def conversation_create(request):
    """Start an empty conversation and open it."""
    conversation = Conversation.objects.create(user=request.user)
    return redirect(conversation)


@login_required
def conversation_detail(request, pk):
    """Show a conversation with the form to send the next message."""
    conversation = get_own_conversation(request, pk)
    return render_detail(request, conversation, MessageForm())


@login_required
@require_POST
def message_create(request, pk):
    """Save the user's message, ask the assistant, and save its answer."""
    conversation = get_own_conversation(request, pk)
    form = MessageForm(request.POST)
    if not form.is_valid():
        if request.htmx:
            return render(request, f"{DETAIL_TEMPLATE}#composer", {"conversation": conversation, "form": form})
        return render_detail(request, conversation, form)

    text = form.cleaned_data["text"]
    if not conversation.messages.exists():
        conversation.title = Truncator(text).chars(60)
    user_message = conversation.messages.create(role=Message.Role.USER, text=text)

    try:
        reply_text = generate_reply(conversation.messages.all())
    except errors.APIError:
        logger.exception("The assistant failed to answer in conversation %s", conversation.pk)
        reply = None
    else:
        reply = conversation.messages.create(role=Message.Role.MODEL, text=reply_text)
    conversation.save(update_fields=["title", "updated_at"])

    if not request.htmx:
        return redirect(conversation)
    context = {
        "conversation": conversation,
        "user_message": user_message,
        "reply": reply,
        "form": MessageForm(),
    }
    # Appended to #messages by htmx; the composer and title are swapped out-of-band.
    return render(request, f"{DETAIL_TEMPLATE}#exchange", context)

