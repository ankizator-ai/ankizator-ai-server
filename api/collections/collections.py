from django.http import JsonResponse
from ninja import Schema, Router

from api.collections.schemas import CollectionSchema, WordSchema, PlainWordSchema, ExampleSchema
from api.extration import extract_tablepress_content
from api.generate_anki_deck import generate_anki_deck
from api.models import Collection, Word, Context
from api.collections.contexts.generate_context import generate_every_example

router = Router()

def collection_404():
    return 404, {"message": "Collection not found"}

class Success(Schema):
    message: str

class Error(Schema):
    message: str

@router.get('/', response=list[CollectionSchema])
def get_collections(request):
    return Collection.objects.values()

@router.get('/{collection_id}/extract', response={200: list[PlainWordSchema], 404: Error})
def get_collections_extract(request, collection_id: int):
    try:
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        return collection_404()

    words = extract_tablepress_content(collection)

    return 200, words

@router.get('/{collection_id}/words', response=list[WordSchema])
def get_collections_words(request, collection_id: int, all_words: bool = False):
    collection = Collection.objects.get(id=collection_id)
    if all_words:
        return Word.objects.filter(collection=collection).values()
    else:
        return Word.objects.filter(collection=collection, context__isnull=True).values()

@router.post('/{collection_id}/words', response={201: Success, 400: Error, 404: Error})
def post_collections_words(request, collection_id: int, payload: list[PlainWordSchema]):
    try:
        collection = Collection.objects.get(id=collection_id)

        og_tr_pairs = [(word_data.og, word_data.tr) for word_data in payload]
        existing_words = Word.objects.filter(
            collection=collection,
            og__in=[og for og, tr in og_tr_pairs]
        ).values_list('og', 'tr')

        new_words = [
            Word(collection=collection, og=og, tr=tr)
            for og, tr in og_tr_pairs
            if (og, tr) not in existing_words
        ]

        if new_words:
            Word.objects.bulk_create(new_words)
    except Collection.DoesNotExist:
        return collection_404()
    except Exception as e:
            return 400, {"message": f"Failed to create words: {str(e)}"}

    return 201, {"message": "Words created successfully"}

@router.get('/{collection_id}/contexts', response=list[ExampleSchema])
def get_collections_contexts(request, collection_id: int):
    words = Word.objects.filter(collection_id=collection_id).prefetch_related('context_set')
    result = [
        {
            "word": word,
            "context": word.context_set.first()

        }
        for word in words if word.context_set.exists()
    ]
    return result

@router.post('/{collection_id}/contexts')
def generate_context(request, payload: list[int], collection_id: int):
    words = Word.objects.filter(id__in=payload, collection_id=collection_id)
    if not words.exists():
        return JsonResponse({'error': 'No words found for the given IDs and collection.'}, status=404)

    context_objects= generate_every_example(words)
    Context.objects.bulk_create(context_objects)

@router.delete('/{collection_id}/contexts')
def generate_context(request, payload: list[int], collection_id: int):
    contexts = Context.objects.filter(id__in=payload, word__collection_id=collection_id).delete()
    if not contexts[0]:
        return JsonResponse({'error': 'No contexts found for the given IDs and collection.'}, status=404)
    return 200, contexts


@router.get('/{collection_id}/anki')
def get_anki_deck(request, collection_id: int):
    return generate_anki_deck(collection_id)