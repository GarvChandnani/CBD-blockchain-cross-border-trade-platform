import hashlib
import json
import time

class Block:
    def __init__(self, index, transactions, previous_hash, timestamp=None, nonce=0):
        self.index = index
        self.timestamp = timestamp or time.time()
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps({
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t if isinstance(t, dict) else t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    def mine_block(self, difficulty):
        target = "0" * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        print(f"Block Mined! Hash: {self.hash}")

    def to_dict(self):
        return {
            "index": self.index,
            "timestamp": self.timestamp,
            "transactions": [t if isinstance(t, dict) else t.to_dict() for t in self.transactions],
            "previous_hash": self.previous_hash,
            "nonce": self.nonce,
            "hash": self.hash
        }
