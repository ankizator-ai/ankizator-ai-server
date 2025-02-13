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

safety_settings=[
  {
    "category": "HARM_CATEGORY_DANGEROUS",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_NONE",
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_NONE",
  },
]

def generate_context(word: Word) -> Context:
    genai.configure(api_key=config("GENAI_API_KEY"))
    generation_config = genai.GenerationConfig(temperature=1.0)
    model = genai.GenerativeModel(config("GENAI_MODEL"), safety_settings=safety_settings, generation_config=generation_config)
    query = f"{word.og};{word.tr}"
    response = model.generate_content(query)
    first_response = response.candidates[0].content.parts[0].text
    context = first_response.split(";")
    print(context)
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
                   print("Fail:", exc)
                   continue

    print("GENERATED EXAMPLES:", examples)
    return examples