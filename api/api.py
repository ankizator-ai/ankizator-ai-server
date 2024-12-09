import os
from django.http import JsonResponse
from ninja import NinjaAPI

from api.extration import extract_tablepress_content, SourceSchema
from api.models import Source
from api.generate_context import WordsSchema, generate_example_contexts, add_words_to_examples

api = NinjaAPI()

@api.post('/contexts')
def generate_context(request, payload: WordsSchema):
    contexts_without_words = generate_example_contexts(payload)
    contexts_with_words = add_words_to_examples(payload, contexts_without_words)
    return contexts_with_words

@api.get('/sources')
def get_sources(request):
    sources = list(Source.objects.values())
    return JsonResponse(sources, safe=False)

@api.post('/words')
def get_merula(request, payload: SourceSchema):
    return JsonResponse(extract_tablepress_content(payload.dict()['source']), safe=False, json_dumps_params={'ensure_ascii': False})
