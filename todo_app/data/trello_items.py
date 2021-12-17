import requests
from flask import current_app as app

def get_auth_params():
    return { 'key': app.config['API_KEY'], 'token': app.config['API_TOKEN'] }

def build_url(endpoint):
    return app.config['BASE_URL'] + endpoint

def build_params(params = {}):
    full_params = get_auth_params()
    full_params.update(params)
    return full_params

class Item:

    def __init__(self, id, name, status = 'To Do'):
        self.id = id
        self.name = name
        self.status = status

    @classmethod
    def from_trello_card(cls, card, list):
        return cls(card['id'], card['name'], list['name'])
        

def get_lists():
    """
    Fetch all lists for board
    Returns:
        list: The list of board lists (To Do, In Progress, Done, etc)
    """
    params = build_params({ 'cards': 'open' })
    url = build_url('/boards/%s/lists' % app.config['BOARD_ID'])

    allLists = requests.get(url, params = params).json()

    return allLists


def get_list(listName):
    """
    Fetches the list with the specified name.

    Args:
        name: The name of the list.
    """
    lists = get_lists()
    return next((list for list in lists if list['name'] == listName), None)


def get_cards():
    """
    Fetches all cards.
    Returns:
        list: The list of cards.
    """
    lists = get_lists()

    cards = []
    for card_list in lists:
        for card in card_list['cards']:
            cards.append(Item.from_trello_card(card, card_list))

    return cards


def get_card(cardId):
    """
    Checks the card using the ID.
    Args:
        id (str): The ID of the card.
    """
    singleCard = []
    cards = get_cards()

    for card in cards:
        if card.id == cardId:
            singleCard.append(card)

    return singleCard


def add_card(cardName):
    """
    Adds a new card with the specified name.

    Args:
        name: The name of the card.
    """
    todo_list = get_list('To Do')

    params = build_params({ 'name': cardName, 'idList': todo_list['id'] })
    url = build_url('/cards')

    response = requests.post(url, params = params)
    card = response.json()

    return Item.from_trello_card(card, todo_list)


def start_card(cardId):
    """
    Moves the card with the specified ID to the "In Progress" list.
    Args:
        id (str): The ID of the card.
    Returns:
        card: The saved card, or None if no cards match the specified ID.
    """
    in_progress_list = get_list('In Progress')
    card = update_card_list(cardId, in_progress_list)

    return Item.from_trello_card(card, in_progress_list)



def complete_card(cardId):
    """
    Updates an existing card in the session. If no existing card matches the ID of the specified card, nothing is saved.

    Args:
        card: The card to save.
    """
    completed_list = get_list('Done')
    card = update_card_list(cardId, completed_list)

    return Item.from_trello_card(card, completed_list)


def undo_card(cardId):
    """
    Moves the item with the specified ID to the "To-Do" list.
    Args:
        id (str): The ID of the card.
    Returns:
        card: The saved card, or None if no cards match the specified ID.
    """
    todo_list = get_list('To Do')
    card = update_card_list(cardId, todo_list)

    return Item.from_trello_card(card, todo_list)


def update_card_list(cardId, list):
    """
    Runs a put request to update the card list
    Args:
        cardId: The ID of the card to be updated
        list: The list object to use for the new list
    Returns: 
        card: The updated card, in the new specified list
    """
    params = build_params({ 'idList': list['id'] })
    url = build_url('/cards/%s' % cardId)

    response = requests.put(url, params = params)
    card = response.json()

    return card