from datetime import datetime, timedelta
from todo_app.data.trello_items import Item
from todo_app.view_model import ViewModel

yesterday = datetime.now() - timedelta(1)
yesterday = yesterday.strftime("%Y-%m-%dT%H:%M:%S.%fZ")
today = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def test_return_to_do_items():
    items = [
        Item(1, 'To Do Item', today, '', "2022-02-08T17:36:12.1345Z", 'To Do'),
        Item(2, 'To Do Item', today, '', "2022-02-08T17:36:12.1345Z", 'To Do')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 2
    assert view_model.to_do_items == [
        Item(1, 'To Do Item', today, '', "2022-02-08T17:36:12.1345Z", 'To Do'),
        Item(2, 'To Do Item', today, '', "2022-02-08T17:36:12.1345Z", 'To Do')
    ]


def test_return_in_progress_items():
    items = [
        Item(1, 'In Progress Item', today, '', "2022-02-08T17:36:12.1345Z", 'In Progress'),
        Item(2, 'In Progress Item', today, '', "2022-02-08T17:36:12.1345Z", 'In Progress'),
        Item(3, 'In Progress Item', today, '', "2022-02-08T17:36:12.1345Z", 'In Progress')
    ]

    view_model = ViewModel(items)

    assert len(view_model.in_progress_items) == 3
    assert view_model.in_progress_items == [
        Item(1, 'In Progress Item', today, '', "2022-02-08T17:36:12.1345Z", 'In Progress'),
        Item(2, 'In Progress Item', today, '', "2022-02-08T17:36:12.1345Z", 'In Progress'),
        Item(3, 'In Progress Item', today, '', "2022-02-08T17:36:12.1345Z", 'In Progress')
    ]


def test_return_done_items():
    items = [
        Item(1, 'Done Item', today, '', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(2, 'Done Item', today, '', "2022-02-08T17:36:12.1345Z", 'Done')
    ]

    view_model = ViewModel(items)

    assert len(view_model.done_items) == 2
    assert view_model.done_items == [
        Item(1, 'Done Item', today, '', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(2, 'Done Item', today, '', "2022-02-08T17:36:12.1345Z", 'Done')
    ]


def test_lists_are_empty_if_undefined_list_is_used():
    items = [
        Item(1, 'Task 1', today, 'Description', "2022-02-08T17:36:12.1345Z", 'Other Status')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 0
    assert len(view_model.in_progress_items) == 0
    assert len(view_model.done_items) == 0


def test_items_are_split_into_categories():
    items = [
        Item(1, 'Task 1', today, '', "2022-02-08T17:36:12.1345Z", 'Something'),
        Item(2, 'Task 2', today, '', "2022-02-08T17:36:12.1345Z", 'To Do'),
        Item(3, 'Task 3', today, '', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(4, 'Task 4', today, '', "2022-02-08T17:36:12.1345Z", 'To Do'),
        Item(5, 'Task 5', today, '', "2022-02-08T17:36:12.1345Z", 'In Progress')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 2
    assert len(view_model.in_progress_items) == 1
    assert len(view_model.done_items) == 1


def test_completed_only_items_last_modified_today():
    items = [
        Item(1, 'Done Today', today, 'Description', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(2, 'To Do', today, 'Description', "2022-02-08T17:36:12.1345Z", 'To Do')
    ]

    view_model = ViewModel(items)

    assert view_model.recent_done_items == [
        Item(1, 'Done Today', today, 'Description', "2022-02-08T17:36:12.1345Z", 'Done')
    ]


def test_completed_only_items_last_modified_before_today():
    items = [
        Item(1, 'Done Yesterday', yesterday, 'Description', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(2, 'Done Today', today, 'Description', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(3, 'Started Yesterday', yesterday, 'Description', "2022-02-08T17:36:12.1345Z", 'In Progress')
    ]

    view_model = ViewModel(items)

    assert view_model.older_done_items == [
        Item(1, 'Done Yesterday', yesterday, 'Description', "2022-02-08T17:36:12.1345Z", 'Done')
    ]