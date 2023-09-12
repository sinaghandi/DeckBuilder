from requests import get
from typing import Optional

BASE_QUERY = 'c<=g t=creature game=paper'
NUM_CREATURES = 40  # num creatures not including commander to be in deck
SCRYFALL_URL = "https://api.scryfall.com/cards/search"


class Card:
    def __init__(self, name: str, types: list[str], usage: int = 0) -> None:
        self.name = name
        self.usage = usage
        self.types = set(types)


class Deck:
    cards = set()
    types = set()

    def __init__(self, cards: list[cards]) -> None:
        self.cards = set(cards)
        for card in cards:
            for subtype in card.types:
                self.types.add(subtype)

    def add(self, card: Card) -> None:
        self.cards.add(card)
        for subtype in card.types:
            self.types.add(subtype)

    def is_valid_card(self, card: Card) -> bool:
        for subtype in card.types:
            if subtype in self.types:
                return False
        return True

    # adds valid card with highest EDHREC rank to Deck
    def add_next_valid(self) -> None:
        # removes every type in self.types from query
        query = f"{BASE_QUERY} {' '.join([f'-t={t}' for t in self.types])}"
        params = {'q': query, 'order': 'edhrec'}
        r = get(SCRYFALL_URL, params=params)
        if r.status_code != 200:
            print(f"Received unexpected status code {r.status_code}")
        request = r.json()
        # TODO add error handling
        if 'data' in request and len(request['data']) > 0:
            name = request['data'][0]['name']
            type_line = request['data'][0]['type_line']
            types = get_subtypes(type_line)
            # TODO use logging instead?
            print(types)
            print(type_line)
            # TODO add error handling if types is None
            card = Card(name=name, types=types)
            # if query param is created corrected, this is unnecessary, as it would
            # never return an invalid card
            if self.is_valid_card(card):
                self.add(card)
            else:
                print(f'eyo {card.name} wasn\'t valid')


def get_subtypes(type_line: str) -> Optional[list[str]]:
    parts = type_line.split("—")
    if len(parts) > 1:
        subtypes = parts[1]
        types = subtypes.strip().split(" ")
        return types
    else:
        return None


# adds the next NUM_CREATURE cards using greedy algorithm
def main() -> None:
    commander = Card(name='Radagast, the Brown', types=['Wizard', 'Avatar'])
    deck = Deck(cards=[commander])
    for _ in range(NUM_CREATURES):
        deck.add_next_valid()
    for card in deck.cards:
        print(card.name)


if __name__ == '__main__':
    main()
