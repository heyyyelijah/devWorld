from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Profile, Skill, Message


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }
    
    # OVERRIDES INIT METHOD TO ADD CLASSES TO FIELDS
    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        # LOOP THROUGH EACH FIELD AND GIVE EACH ONE A CLASS NAMED "INPUT"
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})

        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add Title'})
        # self.fields['description'].widget.attrs.update({'class':'input'})


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'email', 'username', 'location', 
        'short_intro', 'bio', 'profile_image', 'social_github',
        'social_twitter','social_linkedin','social_youtube',
        'social_website',
        ]

    # OVERRIDES INIT METHOD TO ADD CLASSES TO FIELDS
    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)

        # LOOP THROUGH EACH FIELD AND GIVE EACH ONE A CLASS NAMED "INPUT"
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})

        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add Title'})
        # self.fields['description'].widget.attrs.update({'class':'input'})


class SkillsForm(ModelForm):
    class Meta:
        model = Skill
        fields = ['name', 'description']

    # OVERRIDES INIT METHOD TO ADD CLASSES TO FIELDS
    def __init__(self, *args, **kwargs):
        super(SkillsForm, self).__init__(*args, **kwargs)

        # LOOP THROUGH EACH FIELD AND GIVE EACH ONE A CLASS NAMED "INPUT"
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'name', 'email', 'body']
        labels = {
            'subject':'Message Subject:',
            'name': 'Your Name:',
            'email': 'Your Email:',
            'body': 'Your Message:',
        }

    # OVERRIDES INIT METHOD TO ADD CLASSES TO FIELDS
    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        # LOOP THROUGH EACH FIELD AND GIVE EACH ONE A CLASS NAMED "INPUT"
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input input--text'})