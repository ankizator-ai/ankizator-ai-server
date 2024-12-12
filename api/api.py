import os
from django.http import JsonResponse, HttpResponse
from ninja import NinjaAPI

from api.extration import extract_tablepress_content, SourceSchema
from api.generate_anki_deck import generate_anki_deck
from api.models import Source
from api.generate_context import WordsSchema, generate_example_contexts, add_words_to_examples, WordsWithContextSchema

api = NinjaAPI()

# TODO: remove it
def return_json(response):
    return JsonResponse({'data': response}, json_dumps_params={'ensure_ascii': False}, safe=False)

@api.post('/anki')
def post_anki_deck(request, payload: WordsWithContextSchema):
    return generate_anki_deck(payload)

@api.post('/contexts')
def generate_context(request, payload: WordsSchema):
    contexts_without_words = generate_example_contexts(payload)
    contexts_with_words = add_words_to_examples(payload, contexts_without_words)
    return contexts_with_words

@api.get('/sources')
def get_sources(request):
    sources = list(Source.objects.values())
    return return_json(sources)

@api.post('/words')
def get_merula(request, payload: SourceSchema):
    source = payload.dict()['source']
    words = extract_tablepress_content(source)
    return return_json(words)
