import pytest
import os
import pathlib
from LocalStorage.localStore import LocalSore
import jsonlines


def test_store_creation():
    # default path
    store = LocalSore()
    file_path = store.file_path
    file = file_path.name
    parent_path = file_path.parent
    files = os.listdir(parent_path)

    assert file in files, 'Store Not Created'
    assert 'keys.json' in files, 'Keys file not created'

    store.delete_store()


def test_store_creation_user_path():
    store1 = LocalSore('store.json')
    file_path = store1.file_path
    file = file_path.name
    parent_path = file_path.parent
    files = os.listdir(parent_path)
    print(file_path)

    assert file in files, 'Store Not Created'
    assert 'keys.json' in files, 'Keys file not created'

    store1.delete_store()


def test_write_to_file():
    store = LocalSore()
    store.write("key1", 'adasdfadsf')

    with jsonlines.open(store.file_path) as fp:
        for line in fp.iter():
            assert line == {'key1&^@#':{'data': 'adasdfadsf'}}, 'Record is not same'

    store.delete_store()