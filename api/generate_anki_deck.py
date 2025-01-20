import markdown
import genanki
import os
from django.http import FileResponse

from api.models import Collection, Context


def generate_anki_deck(collection_id):
    my_model = genanki.Model(
        1612738572,
    'AnkizatorAI',
        fields=[
            {'name': 'og_word'},
            {'name': 'tr_word'},
            {'name': 'og_context'},
            {'name': 'tr_context'},
        ],
        templates=[
            {
                'name': 'Card 1: (original word+context -> translated word+context)',
                'qfmt': """
                    <div class="front">
                    	<div class="word row">{{tts pl_PL:og_word}}{{og_word}}</div>
                    	<div class="row">
                    		{{tts pl_PL:og_context}}
                    		<span class="context">{{og_context}}</span>
                    	</div>
                    </div>
                """,
                'afmt': """
                    {{FrontSide}}
                    <hr id="answer">
                    <div class="back">
                    		<div class="word row">{{tts en_US:tr_word}}{{tr_word}}</div>
                    		<div class="row">
                    			{{tts en_US:tr_context}}
                    			<span class="context">{{tr_context}}</span>
                    </div>
                    </div> 
                """
            },
        ],
        css="""
        .front, .back {
        	max-width: 40em;
        	margin: auto;
        	padding: 1em;
        }
        
        .word {
        	font-size: 2em;
        	font-weight: 600;
        }
        
        .context {
        	font-style: italic;
        }""")


    collection = Collection.objects.get(id=collection_id)
    collection_name = getattr(collection, 'name')
    my_deck = genanki.Deck(2024749016+collection_id,f'AnkizatorAI::{collection_name}')
    contexts = Context.objects.filter(word__collection=collection).prefetch_related()

    for context in contexts:
        pl_context = markdown.markdown(context.og)
        en_context = markdown.markdown(context.tr)
        my_note = genanki.Note(
            model=my_model,
            fields=[context.word.og, context.word.tr, pl_context, en_context],)
        my_deck.add_note(my_note)
    filename = "anki_deck.apkg"
    cache_dir = "/var/cache/ankizator-ai"
    file_path = os.path.join(cache_dir, filename)
    genanki.Package(my_deck).write_to_file(file_path)

    response = FileResponse(open(file_path, 'rb'), content_type="application/octet-stream")
    response['Content-Disposition'] = f'attachment; filename="{collection_name}.apkg"'

    return response