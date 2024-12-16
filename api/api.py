from django.http import JsonResponse
from ninja import NinjaAPI

from api.collections.schemas import CollectionOut
from api.extration import extract_tablepress_content, SourceSchema
from api.generate_anki_deck import generate_anki_deck
from api.generate_context import WordsSchema, split_words_payload, generate_example_contexts, add_words_to_examples, \
    WordsWithContextSchema
from api.models import Collection, Word

api = NinjaAPI()

# TODO: remove it
def return_json(response):
    return JsonResponse({'data': response}, json_dumps_params={'ensure_ascii': False}, safe=False)

@api.get('/collections', response=list[CollectionOut])
def get_sources(request):
    return Collection.objects.values()

@api.post('/collections/{collection_id}/words')
def post_contexts_words(request, collection_id: int):
    collection = Collection.objects.get(id=collection_id)
    Word.objects.filter(collection=collection).delete()
    words = extract_tablepress_content(collection)
    Word.objects.bulk_create(words)

@api.post('/contexts')
def generate_context(request, payload: WordsSchema):
    split_words = split_words_payload(payload)
    final_contexts_with_words = []
    for words in split_words:
        contexts_without_words = generate_example_contexts(words)
        contexts_with_words = add_words_to_examples(words, contexts_without_words)
        final_contexts_with_words.extend(contexts_with_words)
    return final_contexts_with_words

@api.post('/anki')
def post_anki_deck(request, payload: WordsWithContextSchema):
    return generate_anki_deck(payload)
