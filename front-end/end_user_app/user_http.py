"""
A static class used to send and obtain HTTP data.
"""

import datetime
import json
from typing import Dict, List

import requests

posts = []

class UserHTTP:
    guaranteed_node_address: str

    def __init__(self):
        self.guaranteed_node_address = "http://165.22.236.136:3000"

    def fetch_posts(self) -> List:
        """
        Function to fetch the chain from a blockchain node, parse the
        data and store it locally.
        """
        get_chain_address = "{}/chain".format(self.guaranteed_node_address)
        response = requests.get(get_chain_address)

        if response.status_code == 200:
            content = []
            chain = json.loads(response.content)

            for block in chain["chain"]:
                for tx in block["transactions"]:
                    tx["index"] = block["index"]
                    tx["hash"] = block["previous_hash"]
                    content.append(tx)

            return sorted(content, key=lambda k: k['timestamp'],
                           reverse=True)


    def create_new_blockchain_transaction(self, post_object: Dict):
        """
        Creates a new transaction via our application.
        """
        # Submit the transaction!
        new_tx_address = "{}/new_transaction".format(self.guaranteed_node_address)
        requests.post(new_tx_address,
                      json=post_object,
                      headers={'Content-type': 'application/json'})

    def timestamp_to_string(self, epoch_time):
        return datetime.datetime.fromtimestamp(epoch_time).strftime('%H:%M')

    def mine_transaction(self) -> int:
        get_chain_address = "{}/mine".format(self.guaranteed_node_address)
        response = requests.get(get_chain_address)
        return response.status_code, response.text
