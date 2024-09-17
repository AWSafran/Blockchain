import hashlib
import requests
import json
import sys
from time import time

# TODO: Implement functionality to search for a proof 

def valid_proof(block_string, proof):
    """
    Validates the Proof:  Does hash(block_string, proof) contain 6
    leading zeroes?
    """
    guess = f'{block_string}{proof}'.encode()
    guess_hash = hashlib.sha256(guess).hexdigest()
    return guess_hash[:6] == "000000"


if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    coins_mined = 0
    print("Testing print statements")
    loops = 0
    # Run forever until interrupted
    while True:
        print("Getting proof")
        get_block = requests.get(url='http://localhost:5000/last_block')
        last_block = get_block.json()
        print(last_block)
        # TODO: Get the last proof from the server and look for a new one

        block_string = json.dumps(last_block, sort_keys=True).encode()
        proof = 0
        while not valid_proof(block_string, proof):
            print(f"Failure: {proof}")
            proof += 1

        # TODO: When found, POST it to the server {"proof": new_proof}

        proof_object = {
            "proof": proof
        }
        # TODO: We're going to have to research how to do a POST in Python
        # HINT: Research `requests` and remember we're sending our data as JSON

        response = requests.post(url='http://localhost:5000/mine', data=proof_object)
        # TODO: If the server responds with 'New Block Forged'
        # add 1 to the number of coins mined and print it.  Otherwise,
        # print the message from the server.

        if response.status_code == 200:
            coins_mined += 1
            print("You mined another coin!")

        if coins_mined > 10:
            break

