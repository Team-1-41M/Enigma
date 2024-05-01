from typing import Any

import pytest
from server.projects.content import (
    _is_default,
    _remove_defaults,
    create,
    delete,
    put,
    update,
)


def test_create():
    content_list = []

    element_data = {
        "id": 1,
        "name": "test",
    }

    create(content_list, element_data)

    assert element_data in content_list


def test_create_duplicates_id():
    element_data = {
        "id": 1,
        "name": "test",
    }

    content_list = [
        element_data,
    ]

    duplicates_list = [
        element_data,
        element_data,
    ]

    create(content_list, element_data)

    assert content_list != duplicates_list


@pytest.mark.parametrize(
    "value, result",
    [
        (0, True),
        (0.0, True),
        ("", True),
        (None, False),
        (1, False),
        (1.0, False),
        ("test", False),
    ]
)
def test_is_default(value: Any, result: bool):
    assert _is_default(value) == result
