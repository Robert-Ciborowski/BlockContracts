"""
This is a server, which represents a single node in
our blockchain network. Each client runs such a
server.
"""

import json
import time

from flask import Flask, request
import requests

from blockchain.Block import Block
from blockchain.Blockchain import Blockchain

app = Flask(__name__)

# This node's copy of the chain.
blockchain = Blockchain()
blockchain.create_genesis_block()

# This stores the address of other participating members of the network.
peers = set()


@app.route('/new_transaction', methods=['POST'])
def new_transaction():
    """
    This submits a new transaction request.
    :return: a success/error string, HTTP error code
    """
    tx_data = request.get_json()
    required_fields = ["content"]

    for field in required_fields:
        if not tx_data.get(field):
            return "Invalid transaction data", 404

    tx_data["timestamp"] = time.time()
    blockchain.add_transaction(tx_data)
    return "Success", 201


@app.route('/chain', methods=['GET'])
def get_chain():
    """
    This returns the node's copy of the chain.
    :return: json data with chain length, the chain itself,
             and a list of peers
    """
    chain_data = []

    for block in blockchain.chain:
        chain_data.append(block.__dict__)

    return json.dumps({"length": len(chain_data),
                       "chain": chain_data,
                       "peers": list(peers)})


@app.route('/mine', methods=['GET'])
def mine_unconfirmed_transactions():
    """
    This requests the node to mine the unconfirmed data (if any).
    :return: success/error string
    """
    result = blockchain.mine()

    if not result:
        return "-1"
    else:
        # Making sure we have the longest chain before announcing to the network
        chain_length = len(blockchain.chain)
        consensus()

        if chain_length == len(blockchain.chain):
            # announce the recently mined block to the network
            announce_new_block(blockchain.get_last_block)

        return "{}".format(blockchain.get_last_block.index)


@app.route('/register_node', methods=['POST'])
def register_new_peers():
    """
    This adds new peers to the network.
    :return: a success/error string, HTTP error code
    """
    node_address = request.get_json()["node_address"]

    if not node_address:
        return "Invalid data", 400

    # Add the node to the peer list
    peers.add(node_address)

    # Return the consensus blockchain to the newly registered node
    # so that he can sync
    return get_chain()


@app.route('/register_with', methods=['POST'])
def register_with_existing_node():
    """
    Internally calls the `register_node` endpoint to
    register current node with the node specified in the
    request, and sync the blockchain as well as peer data.
    :return: a success/error string, HTTP error code
    """
    node_address = request.get_json()["node_address"]

    if not node_address:
        return "Invalid data", 400

    data = {"node_address": request.host_url}
    headers = {'Content-Type': "application/json"}

    # Make a request to register with remote node and obtain information
    response = requests.post(node_address + "/register_node",
                             data=json.dumps(data), headers=headers)

    if response.status_code == 200:
        global blockchain
        global peers
        # update chain and the peers
        chain_dump = response.json()['chain']
        blockchain = create_chain_from_dump(chain_dump)
        peers.update(response.json()['peers'])
        return "Registration successful", 200
    else:
        # if something goes wrong, pass it on to the API response
        return response.content, response.status_code


def create_chain_from_dump(chain_dump):
    """
    Creates a blockchain from given data.
    :param chain_dump: the data
    :return: the generated blockchain
    """
    generated_blockchain = Blockchain()
    generated_blockchain.create_genesis_block()

    for idx, block_data in enumerate(chain_dump):
        if idx == 0:
            # We don't care about the genesis block.
            continue

        block = Block(block_data["index"],
                      block_data["transactions"],
                      block_data["timestamp"],
                      block_data["previous_hash"],
                      block_data["nonce"])
        proof = block_data['hash']
        added = generated_blockchain.add_block(block, proof)

        if not added:
            raise Exception("The chain dump is tampered!!")

    return generated_blockchain


# endpoint to add a block mined by someone else to
# the node's chain. The block is first verified by the node
# and then added to the chain.
@app.route('/add_block', methods=['POST'])
def verify_and_add_block():
    """
    Adds a block mined by someone else to the node's chain.
    The block is first verified by the node and then added to
    the chain.
    :return: a success/error string, HTTP error code
    """
    block_data = request.get_json()
    block = Block(block_data["index"],
                  block_data["transactions"],
                  block_data["timestamp"],
                  block_data["previous_hash"],
                  block_data["nonce"])
    proof = block_data['hash']
    added = blockchain.add_block(block, proof)

    if not added:
        return "The block was discarded by the node", 400

    return "Block added to the chain", 201


@app.route('/pending_tx')
def get_pending_tx():
    """
    Queries any unconfirmed transactions.
    :return: JSON data of the unconfirmed transactions.
    """
    return json.dumps(blockchain.unconfirmed_transactions)


def consensus():
    """
    A *very* naive consensus algorithm. If a longer valid chain is
    found, our chain is replaced with it.
    :return: success (boolean)
    """
    global blockchain

    longest_chain = None
    current_len = len(blockchain.chain)

    for node in peers:
        response = requests.get('{}chain'.format(node))
        length = response.json()['length']
        chain = response.json()['chain']

        if length > current_len and blockchain.check_chain_validity(chain):
            current_len = length
            longest_chain = chain

    if longest_chain:
        blockchain = longest_chain
        return True

    return False


def announce_new_block(block):
    """
    This will send an announcement to the entire network once a block has
    been mined. Other blocks can simply verify the proof of work and add it
    to their respective chains.
    """
    for peer in peers:
        url = "{}add_block".format(peer)
        headers = {'Content-Type': "application/json"}
        requests.post(url,
                      data=json.dumps(block.__dict__, sort_keys=True),
                      headers=headers)

# Uncomment this line if you want to specify the port number in the code
#app.run(debug=True, port=8000)
