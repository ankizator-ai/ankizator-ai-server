import json

from django.test import TestCase, Client
from api.models import Word, Context, Collection

def delete_ids(list_to_process):
    for piece in list_to_process:
        del piece['id']


class GenerateContextTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.collection = Collection.objects.create(id=1, name="Test Collection")
        self.word1 = Word.objects.create(collection=self.collection, og="jedzenie", tr="food")
        self.word2 = Word.objects.create(collection=self.collection, og="mieszkanie", tr="flat")
        self.context = Context.objects.create(word = self.word1, og="Jedzenie jest niebywale ważne dla człowieka.", tr="Food is exceedingly important for a human.")

        self.words_payload = [
            {"og": "jedzenie","tr": "food"},
            {"og": "mieszkanie","tr": "flat"}
        ]
        self.words_to_add = [
            {"og": "przyklad3", "tr": "example3"},
            {"og": "przyklad4", "tr": "example4"}
        ]
        self.words_after_add = self.words_payload + self.words_to_add
        self.contexts_payload = [
            {
                "word": {
                    "id": self.word1.id,
                    "og": self.word1.og,
                    "tr": self.word1.tr
                },
                "context": {
                    "id": self.context.id,
                    "og": self.context.og,
                    "tr": self.context.tr
                }
            }
        ]
        self.collection_payload = [
            {"id": 1, "name": "Test Collection"}
        ]

    def test_get_collections(self):
        response = self.client.get("/api/collections/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.collection_payload, response.json())

    def test_get_words(self):
        response = self.client.get("/api/collections/1/words?all_words=True")
        self.assertEqual(response.status_code, 200)
        delete_ids(response.json())
        self.assertEqual(self.words_payload, response.json())

    def test_post_words(self):
        response = self.client.post("/api/collections/1/words", data=json.dumps(self.words_to_add), content_type="application/json")
        self.assertEqual(response.status_code, 201)
        response = self.client.get("/api/collections/1/words?all_words=True")
        self.assertEqual(response.status_code, 200)
        delete_ids(response.json())
        self.assertEqual(self.words_after_add, response.json())

    def test_get_contexts(self):
        response = self.client.get("/api/collections/1/contexts")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.contexts_payload, response.json())

    def test_post_contexts(self):
        words = self.client.get("/api/collections/1/words").json()
        contexts_payload = []
        for word in words:
             contexts_payload.append(word["id"])
        response = self.client.post("/api/collections/1/contexts", data=json.dumps(contexts_payload), content_type="application/json")
        self.assertEqual(response.status_code, 201)