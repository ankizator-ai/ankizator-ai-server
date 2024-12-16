import os
from django.http import JsonResponse, HttpResponse
from ninja import NinjaAPI

from api.extration import extract_tablepress_content, SourceSchema
from api.generate_anki_deck import generate_anki_deck
from api.models import Collection
from api.generate_context import WordsSchema, generate_example_contexts, add_words_to_examples, WordsWithContextSchema, \
    split_words_payload

api = NinjaAPI()

# TODO: remove it
def return_json(response):
    return JsonResponse({'data': response}, json_dumps_params={'ensure_ascii': False}, safe=False)

@api.get('/collections')
def get_sources(request):
    sources = list(Collection.objects.values())
    return return_json(sources)

@api.post('/contexts')
def generate_context(request, payload: WordsSchema):
    split_words = split_words_payload(payload)
    final_contexts_with_words = []
    for words in split_words:
        contexts_without_words = generate_example_contexts(words)
        contexts_with_words = add_words_to_examples(words, contexts_without_words)
        final_contexts_with_words.extend(contexts_with_words)
    return final_contexts_with_words

@api.post('/words')
def get_merula(request, payload: SourceSchema):
    source = payload.dict()['source']
    words = extract_tablepress_content(source)
    return return_json(words)

@api.post('/anki')
def post_anki_deck(request, payload: WordsWithContextSchema):
    return generate_anki_deck(payload)
