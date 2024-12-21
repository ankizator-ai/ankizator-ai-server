import json
import google.generativeai as genai
import typing_extensions
from dotenv import dotenv_values
from api.collections.schemas import WordSchema

class Example(typing_extensions.TypedDict):
    og: str
    tr: str

def generate_example_contexts(words):
    config = dotenv_values(".env")
    genai.configure(api_key=config["GENAI_API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-flash")
    string_words = [f"{word['og']},{word['tr']}" for word in words]
    query_format = "This is array of pairs of words separated by ';'. First is in pl, and second in en_GB: {words}. Provide one grammatically correct example sentence per pair. First word need sentence in og and second in tr. Used word bold in markdown."
    processed_query = query_format.format(words=';'.join(string_words))
    config = genai.GenerationConfig(
        response_mime_type="application/json",
        response_schema=list[Example]
    )
    response = model.generate_content(processed_query, generation_config=config)

    first_response = response.candidates[0].content.parts[0].text
    return json.loads(first_response)
