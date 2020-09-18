from rest_framework import serializers
from apps.core.models import Tatar, Translation, Example
from apps.core.validators import WordFieldValidator

class ExampleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Example
        fields = ('example',)
        validators = []


class TranslationSerializer(serializers.ModelSerializer):
    examples = ExampleSerializer(many=True, allow_null=True)

    class Meta:
        model = Translation
        fields = ('translation', 'examples')


class TatarSerializer(serializers.ModelSerializer):
    def __init__(self, *args, is_authenticated=False, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['word'] = serializers.CharField(validators=[WordFieldValidator(is_authenticated)])

    class Meta:
        model = Tatar
        fields = ('word', 'hit')


class TatarFullSerializer(TatarSerializer):
    translations = TranslationSerializer(many=True, allow_null=True, required=False)

    class Meta:
        model = Tatar
        fields = ('word', 'hit', 'translations')

    def create(self, validated_data):
        tatar = Tatar.objects.create(word=validated_data['word'])
        for translation_dict in validated_data.get('translations', []):
            translation = Translation.objects.create(translation=translation_dict.get('translation', ''), tatar=tatar)
            for example_dict in translation_dict.get('examples', []):
                Example.objects.create(example=example_dict.get('example', ''), translation=translation)
        return tatar

