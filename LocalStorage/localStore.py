import pathlib
import json
import os


BASE_FILE_PATH = pathlib.Path.cwd()
STORE_FILE_PATH = BASE_FILE_PATH / 'store' / 'store.json'


class LocalSore:
    __BASE_FILE_PATH = pathlib.Path.cwd()
    __STORE_FILE_PATH = __BASE_FILE_PATH / 'store' / 'store.json'

    def __init__(self, store_file_path=__STORE_FILE_PATH):
        self.store_file_path = pathlib.Path(store_file_path)
        self.__BASE_PATH = self.store_file_path.parent
        self.store_keys_path = self.__BASE_PATH / 'keys.txt'
        self.__check_or_create_files()
        self.keys = self.__get_keys()

    def __check_or_create_files(self):
        if not self.__BASE_PATH.exists():
            os.makedirs(self.__BASE_PATH)

        if not self.store_file_path.exists():
            with open(self.store_file_path, 'w'):
                pass
            print(
                f'Created Store at {self.store_file_path.absolute()}')

        if not self.store_keys_path.exists():
            with open(self.store_keys_path, 'w'):
                pass
            print(
                f'Created Index File at {self.store_keys_path.absolute()}')

    def __get_keys(self):
        with open(self.store_keys_path) as fp:
            keys = fp.readline().split(',')
            return keys if keys[0] != '' else []

    def __check_key(self, key):
        return True if key in self.keys else False

    def __get_store(self):
        if self.keys == []:
            raise Exception('No Data is present in Store')
        with open(self.store_file_path, 'r') as fp:
            return json.load(fp)

    def __update_keys(self, key, op='add'):
        if op == 'del':
            self.keys.remove(key)
            with open(self.store_keys_path, 'w') as fp:
                fp.write(','.join(self.keys).lstrip(','))
        else:
            if self.__check_key(key):
                raise Exception('Key already exists')

            self.keys.append(key)

            with open(self.store_keys_path, 'w') as fp:
                fp.write(','.join(self.keys))

    def __update_store(self, store):
        with open(self.store_file_path, 'w') as fp:
            json.dump(store, fp)

    def print_store(self):
        store = self.__get_store()
        if self.keys == None:
            print('No data is present in the store')
        else:
            print('='*50)
            print('key        data')
            print('='*50)
            print()
            for key, data in store.items():
                print(f'{key}    :    {data}', end='\n\n')
            print('='*50)

    def write(self, key,  data):
        if self.__check_key(key):
            raise Exception('Key Already Exists')
        else:
            try:
                store = self.__get_store()
                store[key] = data
            except:
                store = {key: data}
            self.__update_store(store)
            self.__update_keys(key)
            print('Data Stored Successfully', end='\n\n')

    def read(self, key):
        if not self.__check_key(key):
            raise Exception('Key Not Found')
        try:
            store = self.__get_store()
            return store[key]
        except Exception as e:
            print(e)

    def delete(self, key):
        if not self.__check_key(key):
            raise Exception('Key Not Found')
        try:
            store = self.__get_store()
            del store[key]
            self.__update_store(store)
            self.__update_keys(key, op='del')
            print(self.keys)
            print('Data Deleted Successfully')

        except Exception as e:
            print(e)


store = LocalSore('stores/store.json')
