from django.forms import ModelForm
from django import forms

from users.models import Profile
from .models import Project, Review



class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link']
        widgets = {
            'tags': forms.CheckboxSelectMultiple(),
        }

    # OVERRIDES INIT METHOD TO ADD CLASSES TO FIELDS
    def __init__(self, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)

        # LOOP THROUGH EACH FIELD AND GIVE EACH ONE A CLASS NAMED "INPUT"
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add Title'})
        # self.fields['description'].widget.attrs.update({'class':'input'})


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['value', 'body']
        labels = {
            'value': 'Place your vote',
            'body': 'Add a comment to your vote',
        }

    # OVERRIDES INIT METHOD TO ADD CLASSES TO FIELDS
    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        # LOOP THROUGH EACH FIELD AND GIVE EACH ONE A CLASS NAMED "INPUT"
        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

        # self.fields['title'].widget.attrs.update({'class':'input', 'placeholder':'Add Title'})
        # self.fields['description'].widget.attrs.update({'class':'input'})