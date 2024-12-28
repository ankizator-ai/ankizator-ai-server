import math
import os
import pathlib

import django
from decouple import config
from django.test import Client
import json

client = Client()


def get_collections():
    response = client.get('/api/collections')
    return response.json()

def extract_collection(collection_id):
    response = client.get(f'/api/collections/{collection_id}/extract')
    return response.json()

def get_collections_words(collection_id, page, all_words=False):
    query_params = {"all_words": all_words, "page": page}
    response = client.get(f'/api/collections/{collection_id}/words', query_params)
    return response.json()

def post_words(collection_id, payload):
    response = client.post(
        f'/api/collections/{collection_id}/words',
        data=json.dumps(payload),
        content_type="application/json",
    )
    return response.json()


def post_contexts(collection_id, words_with_pagination):
    words = words_with_pagination['items']
    ids = [word["id"] for word in words]
    response = client.post(
        f'/api/collections/{collection_id}/contexts',
        data=json.dumps(ids),
        content_type="application/json",
    )
    return response.json()

def download_deck(collection_id):
    response = client.get(f'/api/collections/{collection_id}/anki')
    if response.status_code == 200:
        content_disposition = response.headers.get("Content-Disposition")
        if content_disposition and "filename=" in content_disposition:
            filename = content_disposition.split("filename=")[-1].strip('"')
        else:
            filename = "generated_anki_deck.apkg"

        build_path = pathlib.Path("build")
        build_path.mkdir(exist_ok=True)
        build_filename = os.path.join(build_path, filename)
        with open(build_filename, "wb") as file:
            file.write(b"".join(response.streaming_content))

def confirmation_prompt(task_description):
    while True:
        answer = input(f"{task_description} [y/N]: ").strip().lower()

        if answer in ['y', 'yes']:
            return True
        elif answer in ['n', 'no', '']:
            return False
        else:
            print("Invalid input. Please enter 'y' for yes or 'n' for no.")

def collection_prompt(collections):
    while True:
        print("Available collections:")
        for collection in collections:
            print(f"{collection['id']} - {collection['name']}")
        default_answer = collections[0]['id']
        answer = input(f"Select id [{default_answer}]: ").strip().lower()

        if answer in [default_answer, '']:
            return int(default_answer)
        elif answer in [str(collection['id']) for collection in collections]:
            return int(answer)
        else:
            print("Invalid input. Please proper id.")

def scrap(collection_id):
    words = extract_collection(collection_id)
    post_words(collection_id, words)

def generate_contexts(collection_id):
    starting_page = 1
    items_per_page = 30

    first_words = get_collections_words(collection_id, starting_page)
    float_pages = first_words['count'] / items_per_page
    pages = math.ceil(float_pages)
    post_contexts(collection_id, first_words)
    for page in range(starting_page + 1, pages + 1):
        words = get_collections_words(collection_id, page)
        post_contexts(collection_id, words)

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', config("DJANGO_SETTINGS_MODULE"))
    django.setup()
    collections = get_collections()
    coll_id = collection_prompt(collections)

    if confirmation_prompt("Scrap collection?"):
        scrap(coll_id)
        print("Done scraping!")

    if confirmation_prompt("Generate contexts for words that don't have so?"):
        generate_contexts(coll_id)
        print("Done generating contexts!")

    download_deck(coll_id)
    print("Done downloading!")


if __name__ == "__main__":
    main()