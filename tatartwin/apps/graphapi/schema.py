import graphene
from graphene_django import DjangoObjectType
from apps.core.models import Tatar, Translation, Example
from apps.core.validators import WordFieldValidator, ValidationError


class ExampleType(DjangoObjectType):
    class Meta:
        model = Example
        fields = ("example",)


class TranslationType(DjangoObjectType):
    examples = graphene.List(ExampleType)

    def resolve_examples(self, info):
        return self.examples.all()

    class Meta:
        model = Translation
        fields = ("translation", "examples")


class TatarType(DjangoObjectType):
    translations = graphene.List(TranslationType)

    def resolve_translations(self, info):
        # print(type(self.translations), dir(self.translations), self.translations.all())
        return self.translations.all()

    class Meta:
        model = Tatar
        fields = ("word", "hit", "translations")


class Query(graphene.ObjectType):
    twin = graphene.Field(TatarType, word=graphene.String(required=True))
    top = graphene.List(TatarType, N=graphene.Int(required=True))

    def resolve_twin(self, info, word):
        try:
            WordFieldValidator(is_authenticated=False)(word)
            return Tatar.objects.find_twin(word)
        except ValidationError:
            return Tatar.objects.none()

    def resolve_top(self, info, N):
        return Tatar.objects.top(N)


schema = graphene.Schema(query=Query)
