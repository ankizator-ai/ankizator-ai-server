import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")


from django.http import JsonResponse
from ninja import NinjaAPI

from api.extration import extract_tablepress_content
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

@api.get('/sources')
def get_merula(request):
    return JsonResponse(extract_tablepress_content(request), safe=False)

# TERMINAL:
# python api.py https://merula.pl/jezyk-angielski/focus-3-rozdzial-1-wyglad-tabela-slowek/
