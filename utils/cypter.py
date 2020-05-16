from cryptography.fernet import Fernet
import os.path


# create the key and save it to a file
# key = Fernet.generate_key()
#
# crypter = Fernet(key)
# pw = crypter.encrypt(b'mypassword')
# print(key)
# print('Encrypted password: ' + str(pw, 'utf8'))
#
# solve = crypter.decrypt(pw)
#
# print(str(solve, 'utf8'))
# file = open('keys.key', 'rb')
# message = file.read()
# print(message)


class Encrypt:
    """
    Takes in the file path that you want to read because feeding in a big string
    is a big no no

    """

    def __init__(self, file=None):
        """
        :param file:
        Takes in the file path that needs to be encrypted.
        Does not do anything if the file does not exist.
        """
        self.file_path = file
        if file is None:
            self.data = None
        elif not os.path.isfile(file):
            self.data = None
            print("File Does Not Exist. Moving On")
        else:
            f = open(file, 'rb')
            data = f.read()
            self.data = data
            self.key = None

    def scramble(self, data=None):
        """
        Encrypt Can take both string or file, however file takes priority
        """
        if data is None and self.data is None:
            print("No Data to Encrypt")
            return None
        elif self.file_path is not None:
            self.key = Fernet.generate_key()
            new_crypter = Fernet(self.key)
            encrypted = new_crypter.encrypt(self.data)
            self.data = encrypted
            self._save_to(self.file_path)
            self.show_key()
        else:
            self.key = Fernet.generate_key()
            new_crypter = Fernet(self.key)
            encrypted = new_crypter.encrypt(bytes(data, 'utf8'))
            self.data = encrypted
            self.show_key()
            print('encrypted: ' + str(self.data, 'utf8'))
            return self.data

    def _save_to(self, file_path):
        try:
            folder = open(file_path, "wb")
            folder.write(self.data)
            folder.close()

            folder = open('keys.key', 'wb')
            folder.write(self.key)
            folder.close()
        except:
            print('Failed to save data')

    def show_key(self):
        """
        Shut up robert
        :return:
        """
        print(self.key)
        return self.key


class Decrypt:
    """
    Decryptes files
    """

    def __init__(self, file=None):
        self.file = file
        if file is None:
            self.data = None
        elif not os.path.isfile(file):
            self.data = None
            print("File Does Not Exist. Moving On")
        else:
            f = open(file, 'rb')
            data = f.read()
            self.data = data

    def unscramble(self, key, data=None, file_path=''):
        """
        Takes in a file path to where the decrypted messages goes
        and a key. Default path is the original file
        :param file_path:
        :param key:
        :return:
        """
        if self.data is None and data is None:
            print("NO DATA TO DECRYPT")
            return None
        elif self.data is not None:

            try:
                crypter = Fernet(key)
                message = crypter.decrypt(self.data)
                try:

                    if file_path == '':
                        path = self.file
                    else:
                        path = file_path
                    folder = open(path, "wb")
                    folder.write(message)
                    folder.close()
                except:
                    print('Failed to decrypt data')
            except:
                print("Invalid Key")
        else:

            try:
                crypter = Fernet(key)
                message = crypter.decrypt(bytes(data, 'utf8'))
                try:

                    print('msg: ' + str(message, 'utf8'))
                    return message
                except:
                    print('Failed to decrypt data')
            except:
                print("Invalid Key")


if __name__ == '__main__':
    # test1 = Encrypt()
    # test1.scramble('hello')
    test2 = Decrypt()
    test2.unscramble('8zDJ96latqvuZQNvUJmpMax2WNx2QkW5B4-32Qillf4=', 'gAAAAABewFVDvOMcp5EG4WfK7X6m_4V3iyxGjc_YfItmelfgwLtEqhfgmrXA4xEDDuiZhqcwYmamHvTUSWhXIUYdGodbOJq6fw==')

