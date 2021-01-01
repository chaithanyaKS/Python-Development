import pytest
import os
import pathlib
from LocalStorage.localStore import LocalSore
import jsonlines

KEY_DESCRIPTOR = '&^@#'


def test_store_creation():
    """Test for checking store is created at the default location
    """
    store = LocalSore()
    file_path = store.file_path
    file = file_path.name
    parent_path = file_path.parent
    files = os.listdir(parent_path)

    assert file in files, 'Store Not Created'
    assert 'keys.json' in files, 'Keys file not created'

    store.delete_store()


def test_store_creation_user_path():
    """Test to checking store is created at the user location
    """
    store1 = LocalSore('store.json')
    file_path = store1.file_path
    file = file_path.name
    parent_path = file_path.parent
    files = os.listdir(parent_path)
    print(file_path)

    assert file in files, 'Store Not Created'
    assert 'keys.json' in files, 'Keys file not created'

    store1.delete_store()


def test_write_to_store__key_error():
    """Test for checking if the write method raises KeyError Exception if same key is entered
    """
    store = LocalSore()
    with pytest.raises(KeyError) as exec_info:
        store.write("key1", 'adasdfadsf')
        store.write("key1", 'adasdfadsf')
        print(exec_info)
    store.delete_store()


def test_write_to_store__type_error():
    """Test for checking if write method raises if the type of key is not string
    """
    store = LocalSore()
    with pytest.raises(TypeError) as exec_info:
        print(exec_info)
        store.write(1, 'adasdfadsf')
    store.delete_store()


def test_write_to_file():
    """Test for checking if the record is written properly to the file
    """
    store = LocalSore()
    store.write("key1", 'adasdfadsf')

    with jsonlines.open(store.file_path) as fp:
        for line in fp.iter():
            assert line == {f'key1{KEY_DESCRIPTOR}': {'data': 'adasdfadsf'}
                            }, 'Record is not same'
    store.delete_store()


def test_write_to_store_multiple_records():
    """Test for checking if multiple items are written properly to the file
    """
    store = LocalSore()
    store.write('key1', 'asdfadfasdf')
    store.write('key2', 'asdfadfasdf')
    entries = [
        {f'key1{KEY_DESCRIPTOR}': {'data': 'asdfadfasdf'}},
        {f'key2{KEY_DESCRIPTOR}': {'data': 'asdfadfasdf'}},
    ]

    with jsonlines.open(store.file_path) as fp:
        for line, test in zip(fp.iter(), entries):
            assert line == test, 'records not same'
        store.delete_store()


def test_read_from_file__type_error():
    """Test for checking if read method raises if the type of key is not string
    """
    store = LocalSore()
    with pytest.raises(TypeError) as exec_info:
        store.read(1)
    store.delete_store()


def test_read_from_file__key_error():
    """Test for checking if the read method raises KeyError Exception if same key is entered
    """
    store = LocalSore()
    store.write('key1', "asdasdad")
    with pytest.raises(KeyError) as exec_info:
        store.read('key2')
    store.delete_store()


def test_read_from_store():
    """Test for checking if the data is read properly
    """
    store = LocalSore()
    store.write('key1', 'asdasd')
    data = store.read('key1')
    assert data == {'data': 'asdasd'}, 'data is not same'
    store.delete_store()


def test_delete_from_store__type_error():
    """Test for checking if delete method raises if the type of key is not string
    """
    store = LocalSore()
    with pytest.raises(TypeError) as exec_info:
        store.delete(1)
    store.delete_store()


def test_delete_from_store__key_error():
    """Test for checking if the delete method raises KeyError Exception if same key is entered
    """
    store = LocalSore()
    store.write('key1', 'asdfadsfadsf')
    with pytest.raises(KeyError) as exec_info:
        store.delete('key2')
    store.delete_store()


def test_delete_from_store():
    """Test for Checking if the record is deleted properly
    """
    store = LocalSore()
    store.write('key1', 'asdfadsfadsf')
    store.write('key2', 'asdfadsfadsf')
    store.delete('key1')

    with jsonlines.open(store.file_path) as fp:
        for line in fp.iter():
            assert line == {f'key2{KEY_DESCRIPTOR}': {
                'data': 'asdfadsfadsf'}}, 'Record deleted is different'

    store.delete_store()
