"""
The class which stores blocks in a linkedlist fashion.
This class is meant to be used staticly.
"""

import time
from typing import List

from blockchain.Block import Block


class Blockchain:
    # The difficulty of the proof-of-work algorithm.
    difficulty = 2

    unconfirmed_transactions: List
    chain: List

    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []

    def create_genesis_block(self):
        """
        A function which generates the genesis block and appends it to
        the chain.
        * Such a block has an index of 0
        * Such a block has a previous_hash of 0, and a valid hash.
        """
        genesis_block = Block(0, [], 0, "0")
        genesis_block.hash = genesis_block.compute_hash()
        self.chain.append(genesis_block)

    @staticmethod
    def proof_of_work(block):
        """
        Function that tries different values of nonce to get a hash
        that satisfies our difficulty criteria.
        """
        block.nonce = 0
        computed_hash = block.compute_hash()

        while not computed_hash.startswith('0' * Blockchain.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()

        return computed_hash

    @property
    def get_last_block(self):
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        Adds a block to the chain after the block has been verified.
        """
        previous_hash = self.get_last_block.hash

        if previous_hash != block.previous_hash:
            return False

        if not Blockchain.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def add_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    @classmethod
    def is_valid_proof(cls, block, block_hash):
        """
        Check if block_hash is valid hash of block and satisfies
        the difficulty criteria.

        For a block to be valid...
        - its proof must be valid
        - the previous_hash referred in the block and the hash of latest block
          in the chain must match
        """
        return (block_hash.startswith('0' * Blockchain.difficulty) and
                block_hash == block.compute_hash())

    @classmethod
    def check_chain_validity(cls, chain):
        """
        This verifies that the chain is valid with another chain.
        """
        result = True
        previous_hash = "0"

        for block in chain:
            block_hash = block.hash

            # If you remove hash field, you recompute the hash again using
            # `compute_hash` method.
            delattr(block, "hash")

            if not cls.is_valid_proof(block, block_hash) or \
                    previous_hash != block.previous_hash:
                result = False
                break

            block.hash, previous_hash = block_hash, block_hash

        return result

    def mine(self):
        """
        This function serves as an interface to add the pending
        transactions to the blockchain by adding them to the block
        and figuring out Proof Of Work.
        """
        if not self.unconfirmed_transactions:
            return False

        last_block = self.get_last_block
        new_block = Block(index=last_block.index + 1,
                          data=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)
        proof = self.proof_of_work(new_block)
        self.add_block(new_block, proof)
        self.unconfirmed_transactions = []
        return True
