"""Form for working with the input on the main page"""

from django import forms
from .validators import WordFieldValidator


class WordForm(forms.Form):
    """The form itself"""

    def __init__(self, *args, is_authenticated=False, **kwargs):
        super().__init__(*args, **kwargs)
        word = forms.CharField(label=False, max_length=50, validators=[WordFieldValidator(is_authenticated)])
        word.widget.attrs.update({'class': 'form-control', 'placeholder': f'Максимум {word.max_length} символов'})
        word.error_messages = {'required': 'Введите хотя бы 1 букву'}
        self.fields['word'] = word

