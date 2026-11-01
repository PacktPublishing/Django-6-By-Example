from django import forms


class MessageForm(forms.Form):
    """The text a user sends to the assistant."""

    text = forms.CharField(
        label="Message",
        max_length=4000,
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "Ask about our teas and accessories…"}),
    )
