import html
import io
import markdown
import genanki
from django.http import HttpResponse, FileResponse

from api.generate_context import WordsWithContextSchema


def generate_anki_deck(to_gen: WordsWithContextSchema):
    print(to_gen)
    my_model = genanki.Model(
        1607392319,
        'AnkizatorAI',
        fields=[
            {'name': 'pl_word'},
            {'name': 'en_word'},
            {'name': 'pl_context'},
            {'name': 'en_context'},
        ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '{{pl_word}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{en_word}}',
            },
        ])

    my_deck = genanki.Deck(  2059400110,'AnkizatorAI::Chapter 1')

    for words_with_context in to_gen.wordsWithContext:
        raw_pl_context = markdown.markdown(words_with_context.context.pl)
        raw_en_context = markdown.markdown(words_with_context.context.en)
        pl_context = html.escape(raw_pl_context)
        en_context = html.escape(raw_en_context)
        my_note = genanki.Note(
            model=my_model,
            fields=[words_with_context.wordsPair.pl, words_with_context.wordsPair.en, pl_context, en_context],)
        my_deck.add_note(my_note)
    filename = "anki_deck.apkg"
    genanki.Package(my_deck).write_to_file(filename)

    response = FileResponse(open(filename, 'rb'), content_type="application/octet-stream")
    response['Content-Disposition'] = 'attachment; filename="generated_anki_deck.apkg"'

    return response
