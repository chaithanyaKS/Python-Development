import pathlib
import json
import os


class EmptyStoreException(Exception):
    def __init__(self, msg):
        self.msg = msg


class LocalSore:
    """Class to careate a Key Value based Storage System

    """
    __BASE_FILE_PATH = pathlib.Path.cwd()
    __STORE_FILE_PATH = __BASE_FILE_PATH / 'store' / 'store.json'

    def __init__(self, store_file_path=__STORE_FILE_PATH):
        """Constructor to initialize the Local Storage

        Args:
            store_file_path (str, optional): Path to the local storage. Defaults to __STORE_FILE_PATH.
        """
        self.store_file_path = pathlib.Path(store_file_path)
        self.__BASE_PATH = self.store_file_path.parent
        self.store_keys_path = self.__BASE_PATH / 'keys.txt'
        self.__check_or_create_files()
        self.keys = self.__get_keys()

    def __check_or_create_files(self):
        """Function to check if the store is created or not
        """
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
        """Function to retrive the keys from the keys.txt
            if the keys.txt file is empty list is returned        

        Returns:
            keys : keys of the local storage
        """
        with open(self.store_keys_path) as fp:
            keys = fp.readline().split(',')
            return keys if keys[0] != '' else []

    def __check_key(self, key):
        """Function to check if the key is already in use

        Args:
            key (str): the key to be checked

        Returns:
            bool: True if key is present else False
        """
        return True if key in self.keys else False

    def __get_store(self):
        """Function to retrive the local storage

        Raises:
            EmptyStore: When the store is empty

        Returns:
            store: returns the contents of the store
        """
        if self.keys == []:
            raise EmptyStoreException('No Data is present in Store')
        with open(self.store_file_path, 'r') as fp:
            return json.load(fp)

    def __update_keys(self, key, op='add'):
        """Function to update the key entries

        Args:
            key (str): new key
            op (str, optional): Type of operation to be performed. Defaults to 'add'.

        Raises:
            Exception: [description]
        """

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
        """Function to update the store entries

        Args:
            store (dict(str,str)): new store
        """
        with open(self.store_file_path, 'w') as fp:
            json.dump(store, fp)

    def print_store(self):
        """Function to print the contents of the store.
        """
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
        """Function to write the contents to the store

        Args:
            key (str): key of the new entry
            data (str): data to be stored

        Raises:
            KeyError: Key already exists
        """
        if self.__check_key(key):
            raise KeyError('Key Already Exists')
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
        """Function to read the contents of the store based on a given key

        Args:
            key (str): entry to be read

        Raises:
            KeyError: Key not Found

        Returns:
            entry: contents stored with the key
        """
        if not self.__check_key(key):
            raise KeyError('Key Not Found')
        try:
            store = self.__get_store()
            return store[key]
        except Exception as e:
            print(e)

    def delete(self, key):
        """Function to delete an entry based on a key

        Args:
            key (str): key of the entry to be deleted

        Raises:
            KeyError: If key is not present
        """
        if not self.__check_key(key):
            raise KeyError('Key Not Found')
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
