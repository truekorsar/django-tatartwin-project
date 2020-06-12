
from rest_framework import serializers
from apps.core.models import Tatar, Translations
from django.core.validators import RegexValidator


class WordErrorCheckSerializer(serializers.Serializer):
    _word_validator = RegexValidator(regex='^[А-Яа-яЁёӘәҖҗӨөһҺҢңҮү\s]+$',
                                    message="Допустимы только буквы татарского алфавита и пробел!")
    error = serializers.CharField(max_length=50, validators=[_word_validator],
                                 error_messages={'max_length': 'Максимум 50 символов'})


class TranslationSerializer(serializers.ModelSerializer):
    examples = serializers.StringRelatedField(many=True)

    class Meta:
        model = Translations
        fields = ('translation','examples')


class TatarFullSerializer(serializers.ModelSerializer):
    translations = TranslationSerializer(many=True, read_only=True)

    class Meta:
        model = Tatar
        fields = ('word', 'hit', 'translations')


class TatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tatar
        fields = ('word', 'hit')


