import pathlib
import json
import os
import jsonlines
import fileinput


class EmptyStoreException(Exception):
    def __init__(self, msg):
        self.msg = msg


class LocalSore:
    """Class to create a Key Value based Storage System

    """
    __BASE_FILE_PATH = pathlib.Path.cwd()
    __STORE_FILE_PATH = __BASE_FILE_PATH / 'store' / 'store.ndjson'
    __KEY_DESCRIPTOR = '&^@#'

    def __init__(self, store_file_path=__STORE_FILE_PATH):
        """Constructor to initialize the Local Storage

        Args:
            store_file_path (str, optional): Path to the local storage. Defaults to __STORE_FILE_PATH.
        """
        self.store_file_path = pathlib.Path(store_file_path)
        self.__BASE_PATH = self.store_file_path.parent
        self.store_keys_path = self.__BASE_PATH / 'keys.json'
        self.__check_or_create_files()
        self.keys = self.__get_keys()

    @property
    def file_path(self):
        return self.store_file_path

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
            with open(self.store_keys_path, 'w') as fp:
                json.dump([], fp)

    def __get_keys(self):
        """Function to retrieve the keys from the keys.txt
            if the keys.txt file is empty list is returned        

        Returns:
            keys : keys of the local storage
        """
        with open(self.store_keys_path) as fp:
            keys = json.load(fp)
            return keys

    def __check_key(self, key):
        """Function to check if the key is already in use

        Args:
            key (str): the key to be checked

        Returns:
            bool: True if key is present else False
        """
        return True if key in self.keys else False

    def __generate_store_key(self, key):
        return f'{key}{self.__KEY_DESCRIPTOR}'

    def __get_store(self):
        """Function to retrieve the local storage

        Raises:
            EmptyStore: When the store is empty

        Returns:
            store: returns the contents of the store
        """
        if not self.keys:
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
        else:
            if self.__check_key(key):
                raise Exception('Key already exists')
            self.keys.append(key)

        with open(self.store_keys_path, 'w') as fp:
            json.dump(self.keys, fp)

    def __update_store(self, key=None, data=None, op='add'):
        """Function to update the store entries

        Args:
            key (str): key of the record
            data (dict(str,str)): new record
            op (Enum('add', 'del')): operation to update the store

        Raises:
            KeyErrorException: If the key is None during delete operation
        """
        if op == 'add':
            with jsonlines.open(self.store_file_path, mode='a') as fp:
                fp.write(data)
        elif op == 'del':
            if key is None:
                raise KeyError('Key not provided')
            with fileinput.FileInput(self.store_file_path, inplace=True, backup='.bak', mode='r') as fp:
                for line in fp:
                    if key in line:
                        print('', end='')
                    else:
                        print(line, end='')

    def print_store(self):
        """Function to print the contents of the store.
        """
        spacer = ' ' * 18
        print('=' * 50)
        print(f'  key{spacer}data')
        print('=' * 50)
        print()

        with jsonlines.open(self.store_file_path) as fp:
            for line in fp.iter():
                key, data = list(line.items()).pop()
                record_key = key.replace(self.__KEY_DESCRIPTOR, '')
                print(f'{record_key}    :    {data}', end='\n\n')

        print('=' * 50, end='\r')

    def write(self, key, data):
        """Function to write the contents to the store

        Args:
            key (str): key of the new entry
            data (str): data to be stored

        Raises:
            KeyError: Key already exists
        """
        if not self.__check_file_size():
            raise Exception('Store Size exceeded')

        # if type(key) != '':
        #     raise TypeError("Key is not a string")
        new_key = self.__generate_store_key(key)
        if self.__check_key(new_key):
            raise KeyError('Key Already Exists')
        new_data = {new_key: {"data": data}}
        self.__update_store(data=new_data)
        self.__update_keys(new_key)
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
        key = self.__generate_store_key(key)
        if not self.__check_key(key):
            raise KeyError('Key Not Found')
        for line in fileinput.input(self.store_file_path):
            if key in line:
                val = json.loads(line)
                return val[key]

    def delete(self, key):
        """Function to delete an entry based on a key

        Args:
            key (str): key of the entry to be deleted

        Raises:
            KeyError: If key is not present
        """
        record_key = self.__generate_store_key(key)
        if not self.__check_key(record_key):
            raise KeyError('Key Not Found')
        self.__update_store(key=record_key, op='del')
        self.__update_keys(record_key, op='del')

    def delete_store(self):
        os.remove(self.store_file_path)
        os.remove(self.store_keys_path)
        if not os.path.samefile(pathlib.Path.cwd(), self.store_file_path.parent.absolute()):
            os.removedirs(self.store_file_path.parent.absolute())
        print('Store Deleted Successfully')

    def __check_file_size(self):
        return True if os.stat(self.store_file_path).st_size < 2 ** 30 else False


if __name__ == "__main__":
    store = LocalSore()
    # print(store.file_path)
    # store.write("key3", 'dadasda3')
    # store.write("key2", 'dadasda3')
    # store.write("key1", 'dadasda3')
    # print(store.read('key3'))
    # store.delete('key3')
    store.print_store()
