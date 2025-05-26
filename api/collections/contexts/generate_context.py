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
    try:
        genai.configure(api_key=config("GENAI_API_KEY"))
        generation_config = genai.GenerationConfig(temperature=1.0)
        model = genai.GenerativeModel(config("GENAI_MODEL"), safety_settings=safety_settings, generation_config=generation_config)
        query = f"Generate a usage example for the word '{word.og}' in Polish and its translation '{word.tr}' in English. Respond only with one sentence in Polish and its translation in English, separated by a semicolon without empty space in front of it."
        print(f"Sending to Gemini: {query}")
        response = model.generate_content(query)
        candidate = response.candidates[0]
        first_response = candidate.content.parts[0].text
        context = first_response.split(";")
        print(f"Parsed context: {context}")
        return prettify_context(word, context)

    except Exception as e:
        print(f"Exception in generate_context for word '{word.og}': {e}")
        raise

def generate_every_example(words):
    examples = []
    words_set = list(words)
    finished_words = {word: {"finished": False, "retries": 0} for word in words_set}
    max_retries = config("GENAI_MAX_RETRIES", cast=int)

    while not all(word['finished'] or word['retries'] >= max_retries for word in finished_words.values()):
        with concurrent.futures.ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
            future_to_word = {
                executor.submit(generate_context, word): word
                for word, state in finished_words.items() if not state['finished'] and state['retries'] < max_retries
            }
            for future in concurrent.futures.as_completed(future_to_word):
                try:
                    word = future_to_word[future]
                    examples.append(future.result())
                    finished_words[word]['finished'] = True
                except Exception as exc:
                    print(f"Error processing word {exc}")
                    finished_words[word]['retries'] += 1

    print("GENERATED EXAMPLES:", examples)
    return examples
