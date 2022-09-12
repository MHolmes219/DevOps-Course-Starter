from datetime import datetime, timedelta
from datetime import date
from todo_app.data.trello_items import Item
from todo_app.view_model import ViewModel
from pytest_freezegun import pytest

@pytest.fixture
def current_date():
    return date.today()

@pytest.mark.freeze_time('2022-02-08')
def test_return_to_do_items(current_date):
    items = [
        Item(1, 'To Do Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'To Do'),
        Item(2, 'To Do Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'To Do')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 2
    assert view_model.to_do_items == [
        Item(1, 'To Do Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'To Do'),
        Item(2, 'To Do Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'To Do')
    ]

@pytest.mark.freeze_time('2022-02-08')
def test_return_in_progress_items(current_date):
    items = [
        Item(1, 'In Progress Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'In Progress'),
        Item(2, 'In Progress Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'In Progress'),
        Item(3, 'In Progress Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'In Progress')
    ]

    view_model = ViewModel(items)

    assert len(view_model.in_progress_items) == 3
    assert view_model.in_progress_items == [
        Item(1, 'In Progress Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'In Progress'),
        Item(2, 'In Progress Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'In Progress'),
        Item(3, 'In Progress Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'In Progress')
    ]


@pytest.mark.freeze_time('2022-02-08')
def test_return_done_items(current_date):
    items = [
        Item(1, 'Done Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(2, 'Done Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'Done')
    ]

    view_model = ViewModel(items)

    assert len(view_model.done_items) == 2
    assert view_model.done_items == [
        Item(1, 'Done Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(2, 'Done Item', current_date, '', "2022-02-08T17:36:12.1345Z", 'Done')
    ]


@pytest.mark.freeze_time('2022-02-08')
def test_lists_are_empty_if_undefined_list_is_used(current_date):
    items = [
        Item(1, 'Task 1', current_date, 'Description', "2022-02-08T17:36:12.1345Z", 'Other Status')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 0
    assert len(view_model.in_progress_items) == 0
    assert len(view_model.done_items) == 0


@pytest.mark.freeze_time('2022-02-08')
def test_items_are_split_into_categories(current_date):
    items = [
        Item(1, 'Task 1', current_date, '', "2022-02-08T17:36:12.1345Z", 'Something'),
        Item(2, 'Task 2', current_date, '', "2022-02-08T17:36:12.1345Z", 'To Do'),
        Item(3, 'Task 3', current_date, '', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(4, 'Task 4', current_date, '', "2022-02-08T17:36:12.1345Z", 'To Do'),
        Item(5, 'Task 5', current_date, '', "2022-02-08T17:36:12.1345Z", 'In Progress')
    ]

    view_model = ViewModel(items)

    assert len(view_model.to_do_items) == 2
    assert len(view_model.in_progress_items) == 1
    assert len(view_model.done_items) == 1


@pytest.mark.freeze_time('2022-02-08')
def test_completed_only_items_last_modified_today(current_date):
    items = [
        Item(1, 'Done Today', current_date, 'Description', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(2, 'To Do', current_date, 'Description', "2022-02-08T17:36:12.1345Z", 'To Do')
    ]

    view_model = ViewModel(items)

    assert view_model.recent_done_items == [
        Item(1, 'Done Today', current_date, 'Description', "2022-02-08T17:36:12.1345Z", 'Done')
    ]


@pytest.mark.freeze_time('2022-02-08')
def test_completed_only_items_last_modified_before_today(current_date):

    yesterday = date(2022, 2, 7)

    items = [
        Item(1, 'Done Yesterday', yesterday, 'Description', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(2, 'Done Today', current_date, 'Description', "2022-02-08T17:36:12.1345Z", 'Done'),
        Item(3, 'Started Yesterday', yesterday, 'Description', "2022-02-08T17:36:12.1345Z", 'In Progress')
    ]

    view_model = ViewModel(items)

    assert view_model.older_done_items == [
        Item(1, 'Done Yesterday', yesterday, 'Description', "2022-02-08T17:36:12.1345Z", 'Done')
    ]