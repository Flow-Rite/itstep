from django import forms
from .models import Publication
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = ['title', 'author', 'annotation', 'publication_year', 'page_count', 'publication_type', 'cover_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'author': forms.TextInput(attrs={'class': 'form-control'}),
            'annotation': forms.Textarea(attrs={'class': 'form-control'}),
            'publication_year': forms.NumberInput(attrs={'class': 'form-control'}),
            'page_count': forms.NumberInput(attrs={'class': 'form-control'}),
            'publication_type': forms.Select(attrs={'class': 'form-select'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name in self.errors:
                field.widget.attrs['class'] += ' is-invalid'
            else:
                field.widget.attrs['class'] += ' form-control'

    def clean_publication_year(self):
        year = self.cleaned_data.get('publication_year')
        if year and (year < 1000 or year > 2024):
            raise forms.ValidationError("Рік має бути в межах від 1000 до 2024.")
        return year


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'password1', 'password2')
