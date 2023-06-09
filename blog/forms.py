from django import forms
from django.contrib.auth import get_user_model
from django.core.mail import send_mail


from .models import Post

class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Your Name',
            })
        )
    message = forms.CharField(widget=forms.Textarea(
        attrs={
            'placeholder': "Your Message (Not less than 2 words)",
            'rows': '4',
        }
    ))

    def clean_message(self):
        message = self.cleaned_data.get('message', '')
        num_words = len(message.split())
        if num_words < 2:
            raise forms.ValidationError("Not enough words!")
        return message

    def send_mail(self):
        message = f"From: {self.cleaned_data['name']}\n\nMessage:\n\
            {self.cleaned_data['message']}"

        send_mail(
            subject='Mail from the site',
            message=message,
            from_email='contact@domain.com',
            recipient_list=
            ['customerservices@domain.com',],
            fail_silently=False,
        )


class PostCreateForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('comment_count', 'author', )
