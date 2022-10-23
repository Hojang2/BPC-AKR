import json
import time
import hashlib


class Block(object):
    def __init__(self, data, previous_hash):
        self.data = data
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.nonce = 0
        self.hash = ""

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def create_hash(self):
        text = f"{self.data}{self.previous_hash}{self.timestamp}{self.nonce}"
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.hash

    def change_data(self, data):
        self.data = data

    def mine_block(self, difficulty):
        hash = ""
        while hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            hash = self.create_hash()
        self.hash = hash


difficulty = 4
blocks = [Block("Hello, I'm first block", "0")]
t1 = time.time()
blocks[0].mine_block(difficulty)
print("Block vytezen po:", time.time() - t1)

print(blocks[0].to_json())
for i in range(10):
    block = Block("Hello, I'm first block", blocks[-1].hash)
    t1 = time.time()
    block.mine_block(difficulty)
    print("Block vytezen po:", time.time() - t1)
    blocks.append(block)

difficulty = 6
blocks = [Block("Hello, I'm first block", "0")]
t1 = time.time()
blocks[0].mine_block(difficulty)
print("Block vytezen po:", time.time() - t1)

for i in range(10):
    block = Block("Hello, I'm first block", blocks[-1].hash)
    t1 = time.time()
    block.mine_block(difficulty)
    print("Block vytezen po:", time.time() - t1)
    blocks.append(block)


# Bitcoin momentalne obsahuje 17 nul

for block in blocks:
    print(block.to_json())


def is_chain_valid(blockchain) -> bool:

    for block in blockchain:
        hash = block.create_hash()
        if hash != block.hash:
            return False

    b = blockchain[0].previous_hash
    for block in blockchain:
        if block.previous_hash != b:
            print(blockchain.index(block))
            return False
        b = block.hash

    return True


print("Is chain valid: ", is_chain_valid(blocks))

blocks[1].data = "New data"
print(blocks[1].to_json())

print("Is chain valid: ", is_chain_valid(blocks))


