from django.http import JsonResponse
from ninja import NinjaAPI

from api.collections.schemas import CollectionSchema, WordSchema
from api.extration import extract_tablepress_content
from api.models import Collection, Word, Context
from api.collections.contexts.generate_context import generate_example_contexts

api = NinjaAPI()

@api.get('/collections', response=list[CollectionSchema])
def get_collections(_):
    return Collection.objects.values()

@api.get('/collections/{collection_id}/words', response=list[WordSchema])
def get_collections_words(_, collection_id: int, all_words: bool = False):
    collection = Collection.objects.get(id=collection_id)
    if all_words:
        return Word.objects.filter(collection=collection).values()
    else:
        return Word.objects.filter(collection=collection, context__isnull=True).values()

@api.post('/collections/{collection_id}/words')
def post_collections_words(_, collection_id: int):
    collection = Collection.objects.get(id=collection_id)
    words = extract_tablepress_content(collection)
    Word.objects.bulk_create(words)

@api.post('/collections/{collection_id}/contexts')
def generate_context(_, payload: list[int], collection_id: int):
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

# @api.post('/anki')
# def post_anki_deck(request, payload: WordsWithContextSchema):
#     return generate_anki_deck(payload)
