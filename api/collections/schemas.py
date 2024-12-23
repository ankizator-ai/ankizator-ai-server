from ninja import ModelSchema, Schema
from ..models import Collection, Word

class CollectionSchema(ModelSchema):
    class Meta:
        model = Collection
        fields = ['id', 'name']

class WordSchema(ModelSchema):
    class Meta:
        model = Word
        fields = ['id', 'og', 'tr']

class PlainWordSchema(ModelSchema):
    class Meta:
        model = Word
        fields = ['og', 'tr']

class ExampleSchema(Schema):
    class Word:
        og: str
        tr: str
    class Context:
        og: str
        tr: str