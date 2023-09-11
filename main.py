from requests import get
from typing import Optional

BASE_QUERY = 'c<=g t=creature usd<1'
NUM_CREATURES = 40
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

    def add_next_valid(self) -> None:
        query = f"{BASE_QUERY} {' '.join([f'-t={t}' for t in self.types])}"
        params = {'q': query, 'order': 'edhrec'}
        r = get(SCRYFALL_URL, params=params)
        if r.status_code != 200:
            print(f"Received unexpected status code {r.status_code}")
        data = r.json()
        if 'data' in data and len(data['data']) > 0:
            name = data['data'][0]['name']
            type_line = data['data'][0]['type_line']
            types = get_subtypes(type_line)
            print(types)
            print(type_line)
            card = Card(name=name, types=types)
            if self.is_valid_card(card):
                self.add(card)
            else:
                print('eyo that card wasn\'t valid')


def get_subtypes(type_line: str) -> Optional[list[str]]:
    parts = type_line.split("—")
    if len(parts) > 1:
        subtypes = parts[1]
        types = subtypes.strip().split(" ")
        return types
    else:
        return None


def test_rest_api() -> None:
    query = BASE_QUERY
    params = {'q': query, 'order': 'edhrec'}
    r = get(SCRYFALL_URL, params=params)
    print(r.url)
    print(r.json())


if __name__ == '__main__':
    commander = Card(name='Radagast, the Brown', types=['Wizard', 'Avatar'])
    deck = Deck(cards=[commander])
    for _ in range(NUM_CREATURES):
        deck.add_next_valid()
    for card in deck.cards:
        print(card.name)
