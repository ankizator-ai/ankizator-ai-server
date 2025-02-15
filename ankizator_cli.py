import argparse
import os
import pathlib

import django
from decouple import config
from django.test import Client
import json

client = Client()


def get_collections():
    response = client.get('/api/collections/')
    return response.json()

def get_extract_collection(collection_id):
    response = client.get(f'/api/collections/{collection_id}/extract')
    return response.json()

def get_words(collection_id):
    all_words = False
    query_params = {"all_words": all_words}
    response = client.get(f'/api/collections/{collection_id}/words', query_params)
    return response.json()

def post_words(collection_id, payload):
    response = client.post(
        f'/api/collections/{collection_id}/words',
        data=json.dumps(payload),
        content_type="application/json",
    )
    return response.json()

def get_contexts(collection_id):
    response = client.get(f'/api/collections/{collection_id}/contexts')
    return response.json()

def post_contexts(collection_id, words):
    response = client.post(
        f'/api/collections/{collection_id}/contexts',
        data=json.dumps(words),
        content_type="application/json",
    )
    return response.json()

def delete_contexts(collection_id, contexts):
    response = client.delete(
        f'/api/collections/{collection_id}/contexts',
        data=json.dumps(contexts),
        content_type = "application/json"
    )
    return response

def extract_words_ids(elems):
    ids = [elem["id"] for elem in elems]
    return ids

def extract_contexts_ids(contexts):
    ids = [elem['context']["id"] for elem in contexts]
    return ids

def scrap(collection_id):
    words = get_extract_collection(collection_id)
    post_words(collection_id, words)

def chunked_list(lst, chunk_size):
    for i in range(0, len(lst), chunk_size):
        yield lst[i:i + chunk_size]

def generate_contexts(collection_id):
    words = get_words(collection_id)
    extracted_words = extract_words_ids(words)
    chunked_words = chunked_list(extracted_words, 5)
    for chunk in chunked_words:
        post_contexts(collection_id, chunk)

def truncate_contexts(collection_id):
    contexts = get_contexts(collection_id)
    extracted_contexts = extract_contexts_ids(contexts)
    delete_contexts(collection_id, extracted_contexts)

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

def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', config("DJANGO_SETTINGS_MODULE"))
    django.setup()

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--collection", help="Select collection", type=int, default=1)
    parser.add_argument("-e", "--extract", help="Scrape from website", action="store_true")
    parser.add_argument("-g", "--generate-contexts", help="Generate contexts", action="store_true")
    parser.add_argument("-d", "--download", help="Download anki deck", action="store_true")
    parser.add_argument("-p", "--print", help="Print possible collections", action="store_true")
    parser.add_argument("-t", "--truncate", help="Truncate collection's contexts", action="store_true")

    args = parser.parse_args()

    collections_list = get_collections()
    collections_dict = {collection['id']: collection for collection in collections_list}
    if args.print:
        for coll_id, collection in collections_dict.items():
            print(f"{coll_id} - {collection['name']}")
        return


    if args.collection in collections_dict.keys():
        coll_id = args.collection
    else:
        print("Collection not found!")
        return

    print(f"Selected collection: {coll_id} - {collections_dict[coll_id]['name']}")

    if args.truncate:
        truncate_contexts(coll_id)
        print("Truncated collection's contexts")

    if args.extract:
        scrap(coll_id)
        print("Done scraping!")

    if args.generate_contexts:
        generate_contexts(coll_id)
        print("Done generating contexts!")

    if args.download:
        download_deck(coll_id)
        print("Done downloading!")


if __name__ == "__main__":
    main()