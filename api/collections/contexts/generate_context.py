import concurrent.futures
import os

import google.generativeai as genai
from api.models import Context, Word
from decouple import config

def prettify_context(word, context) -> Context:
    return Context(
        word=word,
        og=context[0],
        tr=context[1],
    )

def generate_context(word: Word) -> Context:
    genai.configure(api_key=config("GENAI_API_KEY"))
    model = genai.GenerativeModel(config("GENAI_MODEL"))
    query = f"{word.og};{word.tr}"
    response = model.generate_content(query)
    first_response = response.candidates[0].content.parts[0].text
    context = first_response.split(";")
    return prettify_context(word, context)


def generate_every_example(words):
    examples = []
    words_set = words.all()
    unfinished_words = {word: False for word in words_set}

    while not all(item for item in unfinished_words.values()):
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
           future_to_word = {executor.submit(generate_context, word): word for word, success in unfinished_words.items() if success == False}
           for future in concurrent.futures.as_completed(future_to_word):
               try:
                   word = future_to_word[future]
                   examples.append(future.result())
                   unfinished_words[word] = True
               except Exception as exc:
                   continue
    return examples