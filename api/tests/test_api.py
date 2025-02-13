from django.test import TestCase, Client
from api.models import Word, Context, Collection

class GenerateContextTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.collection = Collection.objects.create(id=1, name="Test Collection")
        self.word1 = Word.objects.create(id=1, collection=self.collection, og="przyklad1", tr="example1")
        self.word2 = Word.objects.create(id=2, collection=self.collection, og="przyklad2", tr="example2")
        self.valid_payload = [1, 2]
        self.invalid_payload = [999]

    def test_generate_context_success(self):
        response = self.client.get("/api/collection/1/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Context.objects.exists())
