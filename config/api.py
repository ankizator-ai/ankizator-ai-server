from ninja import NinjaAPI
from .generate_context import WordsSchema, generate_example_contexts, add_words_to_examples

api = NinjaAPI()

@api.post('/contexts')
def generate_context(request, payload: WordsSchema):
    contexts_without_words = generate_example_contexts(payload)
    contexts_with_words = add_words_to_examples(payload, contexts_without_words)
    return contexts_with_words