"""
A class which represents a corporate contract.
"""

import csv
from typing import List

from utils.cypter import Encrypt


class Contract:
    data: str
    encrypted_data: str
    encryption_key: str
    block_of_chain: int
    digital_signatures: List
    digital_signature_keys: List

    def __init__(self):
        self.data = ""
        self.encrypted_data = ""
        self.encryption_key = ""
        self.block_of_chain = 0
        self.digital_signatures = []
        self.digital_signature_keys = []

    def add_digital_signature(self, signature: str):
        self.digital_signatures.append(signature)

    def encrypt_data(self):
        encrypt = Encrypt()
        self.encrypted_data = encrypt.scramble(self.data)
        return self.encrypted_data, encrypt.show_key()

    def export_to_files(self, path: str, whichSignature: int):
        if whichSignature < 0 or whichSignature >= len(self.digital_signatures):
            raise Exception(str(whichSignature + " does not exist!"))

        print("ooooof")
        f = open(path, "w+")
        print("ooooof2")
        f.write("key,block_id,signature\n")
        f.write(self.encryption_key + "," + str(self.block_of_chain) + "," +
                self.digital_signatures[whichSignature])
        f.close()

    def import_from_file(self, path: str):
        try:
            with open(path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)

                for row in reader:
                    self.encryption_key = row["key"]
                    self.block_of_chain = int(row["block_id"])
                    self.digital_signatures = [row["signature"]]

        except IOError as e:
            print("Could not read " + path + "!")
