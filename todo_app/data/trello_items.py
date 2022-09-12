import requests
from flask import current_app as app
from datetime import date
import datetime

import pymongo
from bson.objectid import ObjectId

def __get_endpoint():
    endpoint = pymongo.MongoClient(app.config['ENDPOINT'])
    return endpoint

def __get_database():
    database = __get_endpoint()
    database = database[app.config['DATABASE']]
    return database

def __get_card_collection():
    database = __get_database()
    cards = database.cards
    return cards

class Item:

    def __init__(self, id, name, last_modified, description = '', due = '', status = 'To Do'):
        self.id = id
        self.name = name
        self.last_modified = last_modified.strftime("%Y-%m-%d")
        self.description = description
        self.due = due
        self.status = status

    def __eq__(self, other):
        return self.id == other.id and self.name == other.name

    @classmethod
    def from_card(cls, card):
        return cls(card['_id'], card['name'], card['dateLastActivity'], card['desc'], card['due'], card['list'])

    def modified_today(self):
        today = date.today()
        return self.last_modified == today.strftime("%Y-%m-%d")

def get_cards():
    """
    Fetches all cards.
    Returns:
        list: The list of cards.
    """

    cards = __get_card_collection()

    allCards = []
    for card in cards.find():
        allCards.append(Item.from_card(card))

    return allCards


def get_card(cardId):
    """
    Checks the card using the ID.
    Args:
        id (str): The ID of the card.
    """
    cards = __get_card_collection()

    return cards.find({"_id": ObjectId(cardId)})


def add_card(cardName, cardDesc, cardDue):
    """
    Adds a new card with the specified name.

    Args:
        name: The name of the card.
    """

    cards = __get_card_collection()

    card = {
        "name": cardName,
        "dateLastActivity": datetime.datetime.utcnow(),
        "desc": cardDesc,
        "due": cardDue,
        "list": "To Do"
    }

    cards.insert_one(card)

    return Item.from_card(card)


def start_card(cardId):
    """
    Moves the card with the specified ID to the "In Progress" list.
    Args:
        id (str): The ID of the card.
    Returns:
        card: The saved card, or None if no cards match the specified ID.
    """
    card = update_card_list(cardId, 'In Progress')

    return card


def complete_card(cardId):
    """
    Updates an existing card in the session. If no existing card matches the ID of the specified card, nothing is saved.

    Args:
        card: The card to save.
    """
    card = update_card_list(cardId, 'Done')

    return card


def undo_card(cardId):
    """
    Moves the item with the specified ID to the "To-Do" list.
    Args:
        id (str): The ID of the card.
    Returns:
        card: The saved card, or None if no cards match the specified ID.
    """
    card = update_card_list(cardId, 'To Do')

    return card


def delete_card(cardId):
    """
    Updates an existing card in the session. If no existing card matches the ID of the specified card, nothing is archived.

    Args:
        card: The card to archive.
    """
    card = delete_card(cardId)

    return card


def update_card_list(cardId, list):
    """
    Runs a put request to update the card list
    Args:
        cardId: The ID of the card to be updated
        list: The list object to use for the new list
    Returns: 
        card: The updated card, in the new specified list
    """

    cards = __get_card_collection()

    response = cards.update_one({'_id': ObjectId(cardId)}, {'$set': {'list': list, 'dateLastActivity': datetime.datetime.utcnow()}})

    return response


def delete_card(cardId):
    """
    Runs a put request to delete (close) a card
    Args:
        cardId: The ID of the card to be updated
        list: The list object to use for the new list
    Returns:
        card: The updated card with closed = true
    """

    cards = __get_card_collection()

    response = cards.delete_one({'_id': ObjectId(cardId)})
    
    return response