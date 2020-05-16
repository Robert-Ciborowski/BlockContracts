"""
Represents a singular block in the blockchain. The block stores
pdf data.
"""

from hashlib import sha256
import json
from typing import List


class Block:
    index: int
    data: List
    timestamp: int
    previous_hash: int
    nonce: int

    def __init__(self, index, data, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = data
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce

    def compute_hash(self):
        """
        Returns a hash based on the data of this block.
        """
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
