import html
import io
import markdown
import genanki
from django.http import FileResponse

from api.models import Collection, Context


def generate_anki_deck(collection_id):
    my_model = genanki.Model(
        1607392319,
        'AnkizatorAI',
        fields=[
            {'name': 'og_word'},
            {'name': 'tr_word'},
            {'name': 'og_context'},
            {'name': 'tr_context'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{og_word}}{{tts pl_PL:og_word}}<br>{{og_context}}{{tts pl_PL:og_context}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{tr_word}}{{tts en_US:tr_word}}<br>{{tr_context}}{{tts en_US:tr_context}}',
            },
        ])

    my_deck = genanki.Deck(  2059400110,'AnkizatorAI::Chapter 1')

    collection = Collection.objects.get(id=collection_id)
    contexts = Context.objects.filter(word__collection=collection).prefetch_related()

    for context in contexts:
        raw_pl_context = markdown.markdown(context.og)
        raw_en_context = markdown.markdown(context.tr)
        pl_context = html.escape(raw_pl_context)
        en_context = html.escape(raw_en_context)
        my_note = genanki.Note(
            model=my_model,
            fields=[context.word.og, context.word.tr, pl_context, en_context],)
        my_deck.add_note(my_note)
    filename = "anki_deck.apkg"
    genanki.Package(my_deck).write_to_file(filename)

    response = FileResponse(open(filename, 'rb'), content_type="application/octet-stream")
    response['Content-Disposition'] = 'attachment; filename="generated_anki_deck.apkg"'

    return response
