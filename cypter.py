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

    def __init__(self, file):
        """
        :param file:
        Takes in the file path that needs to be encrypted.
        Does not do anything if the file does not exist.
        """
        self.file_path = file
        if not os.path.isfile(file):
            print("File Does Not Exist")
        else:
            f = open(file, 'rb')
            data = f.read()
            self.data = data
            self.key = None

    def scramble(self):
        self.key = Fernet.generate_key()
        new_crypter = Fernet(self.key)
        encrypted = new_crypter.encrypt(self.data)
        self.data = encrypted
        self.save_to(self.file_path)
        self.show_key()

    def save_to(self, file_path):
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

    def __init__(self, file):
        self.file = file
        if not os.path.isfile(file):
            print("File Does Not Exist")
        else:
            f = open(file, 'rb')
            data = f.read()
            self.data = data

    def unscramble(self, key, file_path=''):
        """
        Takes in a file path to where the decrypted messages goes
        and a key. Default path is the original file
        :param file_path:
        :param key:
        :return:
        """

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


if __name__ == '__main__':
    # test1 = Encrypt('scrambledEggs')
    # test1.scramble()
    test2 = Decrypt('scrambledEggs')
    test2.unscramble('jOZElgYMezB2_S7LlKSrM850Q21eHxT15gqUGq9sZMs=')
