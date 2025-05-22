from ninja import ModelSchema, Schema
from ..models import Collection, Word, Context


class CollectionSchema(ModelSchema):
    class Meta:
        model = Collection
        fields = ['id', 'name']

class WordSchema(ModelSchema):
    class Meta:
        model = Word
        fields = ['id', 'og', 'tr']

class ContextSchema(ModelSchema):
    class Meta:
        model = Context
        fields = ['id', 'og', 'tr']

class PlainWordSchema(ModelSchema):
    class Meta:
        model = Word
        fields = ['og', 'tr']

class ExampleSchema(Schema):
    word: WordSchema
    context: ContextSchema