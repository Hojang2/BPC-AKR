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


# Bitcoin momentalne obsahuje 17 nul


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


class Wallet:
    def __init__(self, name):
        self.name = name
        self.UTXOs = []

    def __str__(self):
        return self.to_json()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def send_funds(self, recipient, value):
        bill = value
        neededUTXOs = []
        for utxo in self.UTXOs:
            if bill > 0:
                bill -= utxo.UTXO
                neededUTXOs.append(utxo)
        transaction = Transaction(self.name, recipient.name, value, neededUTXOs)
        for UTXO in neededUTXOs:
            self.UTXOs.remove(UTXO)
        self.UTXOs.append(TransactionInput(transaction.outputs[0]))
        recipient.UTXOs.append(TransactionInput(transaction.outputs[1]))
        return transaction


class Transaction:
    def __init__(self, sender, recipient, value, inputs):
        self.sender = sender
        self.recipient = recipient
        self.value = value
        self.id = self.calculate_hash()
        self.inputs = inputs
        self.outputs = self.processTransaction()

    def calculate_hash(self):
        text = f"{self.sender}{self.recipient}{self.value}"
        return hashlib.sha256(text.encode('utf-8')).hexdigest()

    def __str__(self):
        return self.to_json()

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def processTransaction(self):
        coinsInInputs = 0
        for input in self.inputs:
            coinsInInputs += input.UTXO
        if coinsInInputs < self.value:
            raise ValueError("Nedostatek mincí pro provedení transakce!")
        cashback = coinsInInputs - self.value
        return [TransactionOutput(self.sender, cashback, self.id),
                TransactionOutput(self.recipient, self.value, self.id)]


class TransactionInput:
    def __init__(self, transactionOutput):
        self.UTXO = transactionOutput.value
        self.transactionOutputId = transactionOutput.id

    def __str__(self):  # formátování do JSON
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)


class TransactionOutput:
    def __init__(self, recipient, value, parent_transaction_id):
        self.recipient = recipient
        self.value = value
        self.parentTransactionId = parent_transaction_id
        self.id = self.calculate_hash()

    def __str__(self): #formátování do JSON
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def calculate_hash(self):
        text = f"{self.recipient}{self.value}{self.parentTransactionId}"
        return hashlib.sha256(text.encode('utf-8')).hexdigest()


w1 = Wallet("Jukemi")
w2 = Wallet("Waldo")

t1 = Transaction("Satoshi Nakamoto", "Jukemi", 100, [TransactionInput(TransactionOutput("0", 100, "0"))])

w1.UTXOs = [TransactionInput(t1.outputs[1])]

difficulty = 4
blockchain = [Block(t1, "0")]
time1 = time.time()
blockchain[0].mine_block(difficulty)
print("Block vytezen po:", time.time() - time1)
print("Is chain valid: ", is_chain_valid(blockchain))

t2 = w1.send_funds(w2, 80)

blockchain.append(Block(t2, blockchain[-1].hash))
time1 = time.time()
blockchain[-1].mine_block(difficulty)
print("Block vytezen po:", time.time() - time1)
print("Is chain valid: ", is_chain_valid(blockchain))

t3 = w2.send_funds(w1, 30)

blockchain.append(Block(t3, blockchain[-1].hash))
time1 = time.time()
blockchain[-1].mine_block(difficulty)
print("Block vytezen po:", time.time() - time1)
print("Is chain valid: ", is_chain_valid(blockchain))

#for block in blockchain:
#    print(block.to_json())
print(w1)
print(w2)

# pouziti neexistujicich penez vyvola vyjimku
"""
t4 = w2.send_funds(w1, 100)
blockchain.append(Block(t4, blockchain[-1].hash))
time1 = time.time()
blockchain[-1].mine_block(difficulty)
print("Block vytezen po:", time.time() - time1)
print(blockchain[0].to_json())
print("Is chain valid: ", is_chain_valid(blockchain))
"""