from ninja import ModelSchema
from ..models import Collection

class CollectionOut(ModelSchema):
    class Meta:
        model = Collection
        fields = ['id', 'name']

