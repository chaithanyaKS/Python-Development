import pathlib
import json
import os
from typing import cast
BASE_FILE_PATH = pathlib.Path.cwd()
STORE_FILE_PATH = BASE_FILE_PATH / 'store' / 'store.json'
STORE_INDEX_PATH = BASE_FILE_PATH / 'store' / 'keys.txt'


class LocalSore:

    def __init__(self, store_file_path=STORE_FILE_PATH, store_index_path=STORE_INDEX_PATH):
        self.store_file_path = pathlib.Path(store_file_path)
        self.store_index_path = pathlib.Path(store_index_path)
        self.check_or_create_files()
        self.keys = self.get_keys()

    def check_or_create_files(self):
        if not self.store_file_path.parent.exists():
            os.makedirs(self.store_file_path.parent)

        if not self.store_index_path.parent.exists():
            os.makedirs(self.store_index_path.parent)

        if not self.store_file_path.exists():
            with open(self.store_file_path, 'w'):
                pass
            print(
                f'Created Store at {self.store_file_path.absolute()}')

        if not self.store_index_path.exists():
            with open(self.store_index_path, 'w'):
                pass
            print(
                f'Created Index File at {self.store_index_path.absolute()}')

    def get_keys(self):
        with open(self.store_index_path) as fp:
            keys = fp.readline().split(',')
            return keys if keys[0] != '' else None

    def check_key(self, key):
        if self.keys == None:
            return False
        return True if key in self.keys else False

    def get_store(self):
        with open(self.store_file_path, 'r') as fp:
            return json.load(fp)

    def update_keys(self, key, op='add'):
        if op == 'del':
            self.keys.remove(key)
            with open(self.store_index_path, 'w') as fp:
                fp.write(*self.keys)
        else:
            if self.check_key(key):
                raise Exception('Key already exists')

            separator = ',' if self.keys is not None else ''

            with open(self.store_index_path, 'a') as fp:
                fp.write(f'{separator}{key}')

            if self.keys == None:
                self.keys == [key]
            else:
                self.keys.append(key)

    def update_store(self, store):
        with open(self.store_file_path, 'w') as fp:
            json.dump(store, fp)

    def print_store(self):
        store = self.get_store()

        print('='*50)
        print('key        data')
        print('='*50)
        print()
        for key, data in store.items():
            print(f'{key}    :    {data}', end='\n\n')
        print('='*50)

    def write(self, key,  data):
        if self.check_key(key):
            raise Exception('Key Already Exists')
        else:
            try:
                store = self.get_store()
                store[key] = data
            except:
                store = {key: data}
            self.update_store(store)
            self.update_keys(key)
            print('Data Stored Successfully', end='\n\n')

    def read(self, key):
        if key not in self.keys:
            raise Exception('Key Not Found')
        store = self.get_store()
        return store[key]

    def delete(self, key):
        if key not in self.keys:
            raise Exception('Key Not Found')
        store = self.get_store()
        del store[key]
        self.update_store(store)
        self.update_keys(key, op='del')
        print(self.keys)
        print('Data Deleted Successfully')


store = LocalSore('stores/store.json', 'stores/keys.txt')
store.write("3", 'asdsa')
