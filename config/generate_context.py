import os
from ninja import Schema
from typing import List
import json

import google.generativeai as genai
from dotenv import dotenv_values
import typing_extensions as typing

class ContextSchema(Schema):
    pl: str
    en: str

class WordsPairSchema(Schema):
    pl: str
    en: str

class WordsSchema(Schema):
    words: List[WordsPairSchema]

class WordsPairWithContextSchema(Schema):
    wordsPair: WordsPairSchema
    context: ContextSchema

class WordsWithContextSchema(Schema):
    wordsWithContext: List[WordsPairWithContextSchema]

class ExampleContext(typing.TypedDict):
    pl: str
    en: str

def generate_example_contexts(words: WordsSchema):
    config = dotenv_values(".env")
    genai.configure(api_key=config["GENAI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    dumped_words = json.dumps(words.dict()['words'])
    query_format = "This is array of pairs of words (pl, en_GB): {json_arr}. Provide one grammatically correct example usage per pair. Used word bold in markdown."
    print(query_format.format(json_arr=dumped_words))
    response = model.generate_content(query_format.format(json_arr=dumped_words),
                                      generation_config=genai.GenerationConfig(
                                          response_mime_type="application/json", response_schema=list[ExampleContext]
                                      ),
                                      )

    first_text_in_response = response.candidates[0].content.parts[0].text
    return json.loads(first_text_in_response)

def add_words_to_examples(words: WordsSchema, context):
    contexts_with_words = []
    words = words.dict()["words"]
    for i, context_without_words in enumerate(context):
        words_pair = words[i]
        context_with_words = WordsPairWithContextSchema(wordsPair=words_pair, context=context_without_words)
        contexts_with_words.append(context_with_words)
    return contexts_with_words
