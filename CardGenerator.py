import genanki


class CardGenerator:
    def __init__(self, deckName):
        self.model = genanki.Model(1878474794,
                                   'Code Trivia',
                                   fields=[
                                       {'name': 'Question'},
                                       {'name': 'Answer'},
                                   ],
                                   templates=[
                                       {
                                           'name': 'Card 1',
                                           'qfmt': '<p style="font-size:20px">{{Question}}</p>',
                                           'afmt': '{{FrontSide}}<hr id="answer"><p style="font-size:20px">{{Answer}}</p>',
                                       },
                                   ])
        self.deck = genanki.Deck(
            1465567413,
            deckName
        )

    def add_card(self, question, answer):
        note = genanki.Note(
            model=self.model,
            fields=[question, answer]
        )
        self.deck.add_note(note)

    def output_deck(self, path):
        self.deck.write_to_file(path)
