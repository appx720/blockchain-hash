import random
import hashlib
import datetime
import json
import time

class BlockChain:
    def __init__(self):
        self.chain = []
        self.create_block(nonce = 1, merkle = '', previous_hash = '', transaction = {}) # Genesis block

    def create_block(self, nonce, merkle, previous_hash, transaction : dict):
        time = str(datetime.datetime.now())[:19]

        header = {
            'version': '0.0.1',
            #'index': len(self.chain) + 1,
            'timestamp': time,
            'merkle_root': merkle,
            'nonce': nonce,
            'previous_node': previous_hash
        }

        body = transaction

        self.chain.append({'header': header, 'body': body})
        return [header, body]

    def get_previous_block(self):
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False

        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()

            if hash_operation.startswith("0" * difficulty):
                check_proof = True

            else:
                new_proof += 1

        return new_proof

    def get_merkle(self, transaction):
        if len(transaction) == 1:
            return self.hash(transaction[0])

        newtransaction = []

        for i in range(0, len(transaction) - 1, 2):
            newtransaction.append(self.hash(self.hash(transaction[i]) + self.hash(transaction[i + 1])))

        if len(transaction) % 2 == 1:
            newtransaction.append(self.hash(self.hash(transaction[-1]) + self.hash(transaction[-1])))

        return self.get_merkle(newtransaction)


    def hash(self, proof):
        encoded_block = json.dumps(proof, sort_keys = True).encode()
        return hashlib.md5(encoded_block).hexdigest()

    def create_transaction(self):
        transaction = []

        for i in range(random.randint(1, 5)):
            while True:
                sender = chr(random.randint(65, 90))
                receiver = chr(random.randint(65, 90))

                if sender != receiver:
                    break


            amount = random.randint(1, 10000) / 100
            transaction.append({'sender': sender, 'receiver': receiver, 'amount': amount})

        return transaction



difficulty = 4 # 채굴 난이도

blockchain = BlockChain()

while len(blockchain.chain) < 10:
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['header']['nonce']

    transaction = blockchain.create_transaction()
    merkle = blockchain.get_merkle(transaction)
    nonce = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(nonce, merkle, previous_hash, transaction)


with open('chain.json', 'w') as f :
	json.dump(blockchain.chain, f, indent = 4)

# blockchain2 = BlockChain()
# previous_block = blockchain.get_previous_block()
# previous_proof = previous_block['header']['nonce']

# transaction = [{'sender': 'A', 'receiver': 'B', 'amount': 1}]
# merkle = blockchain2.get_merkle(transaction)
# nonce = blockchain2.proof_of_work(previous_proof)
# previous_hash = blockchain2.hash(previous_block)
# block = blockchain2.create_block(nonce, merkle, previous_hash, transaction)

# time.sleep(1)

# transaction2 = [{'sender': 'A', 'receiver': 'B', 'amount': 1}]
# merkle = blockchain2.get_merkle(transaction2)
# block2 = blockchain2.create_block(nonce, merkle, previous_hash, transaction2)

# with open('chain2.json', 'w') as f :
# 	json.dump(blockchain2.chain, f, indent = 4)