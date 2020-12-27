import pathlib
import json
import os


class LocalSore:

    def __init__(self, store_file_path='./store/store.json', store_index_path='./store/index.txt'):
        self.store_file_path = store_file_path
        self.store_index_path = store_index_path
        self.keys = self.get_keys()

    def get_keys(self):
        with open(self.store_index_path) as fp:
            return fp.readline().split(',')

    def check_key(self, key):
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

            self.keys.append(key)
            with open(self.store_index_path, 'a') as fp:
                fp.write(f',{key}')

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
            store = self.get_store()
            store[key] = data
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


store = LocalSore()
store.print_store()
