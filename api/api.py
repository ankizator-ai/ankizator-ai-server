from django.http import JsonResponse
from ninja import NinjaAPI, Schema
from ninja.pagination import paginate, PageNumberPagination

from api.collections.schemas import CollectionSchema, WordSchema, PlainWordSchema
from api.extration import extract_tablepress_content
from api.generate_anki_deck import generate_anki_deck
from api.models import Collection, Word, Context
from api.collections.contexts.generate_context import generate_example_contexts

api = NinjaAPI()

def collection_404():
    return 404, {"message": "Collection not found"}

class Success(Schema):
    message: str

class Error(Schema):
    message: str

@api.get('/collections', response=list[CollectionSchema])
def get_collections(request):
    return Collection.objects.values()

@api.get('/collections/{collection_id}/extract', response={200: list[PlainWordSchema], 404: Error})
def get_collections_extract(request, collection_id: int):
    try:
        collection = Collection.objects.get(id=collection_id)
    except Collection.DoesNotExist:
        return collection_404()

    words = extract_tablepress_content(collection)

    return 200, words

@api.get('/collections/{collection_id}/words', response=list[WordSchema])
@paginate(PageNumberPagination, page_size=30)
def get_collections_words(request, collection_id: int, all_words: bool = False):
    collection = Collection.objects.get(id=collection_id)
    if all_words:
        return Word.objects.filter(collection=collection).values()
    else:
        return Word.objects.filter(collection=collection, context__isnull=True).values()

@api.post('/collections/{collection_id}/words', response={201: Success, 400: Error, 404: Error})
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

@api.post('/collections/{collection_id}/contexts')
def generate_context(request, payload: list[int], collection_id: int):
    words = Word.objects.filter(id__in=payload, collection_id=collection_id)
    if not words.exists():
        return JsonResponse({'error': 'No words found for the given IDs and collection.'}, status=404)
    contexts_data = generate_example_contexts(words.values())
    context_objects = [
        Context(
            word=words[key],
            og=context['og'],
            tr=context['tr']
    )
        for key, context in enumerate(contexts_data)
    ]

    Context.objects.bulk_create(context_objects)

@api.get('/collections/{collection_id}/anki')
def get_anki_deck(request, collection_id: int):
    return generate_anki_deck(collection_id)
