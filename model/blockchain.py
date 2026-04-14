from .block import Block
import time

class Blockchain:
    def __init__(self):
        self.chain = []
        self.pending_transactions = []
        self.difficulty = 2
        # Create genesis block
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], "0")
        genesis_block.mine_block(self.difficulty)
        self.chain.append(genesis_block)

    def get_latest_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        self.pending_transactions.append(transaction)
        # For simplicity in this demo, we auto-mine after every transaction
        self.mine_pending_transactions()

    def mine_pending_transactions(self):
        if not self.pending_transactions:
            return False
        
        new_block = Block(
            index=len(self.chain),
            transactions=self.pending_transactions,
            previous_hash=self.get_latest_block().hash
        )
        new_block.mine_block(self.difficulty)
        self.chain.append(new_block)
        self.pending_transactions = []
        return True

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]

            if current_block.hash != current_block.calculate_hash():
                return False
            
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

    def get_shipment_history(self, shipment_id):
        history = []
        for block in self.chain:
            for tx in block.transactions:
                # transactions might be dicts or Transaction objects
                tx_id = tx['shipment_id'] if isinstance(tx, dict) else tx.shipment_id
                if tx_id == shipment_id:
                    history.append(tx)
        return history

    def get_latest_shipment_state(self, shipment_id):
        history = self.get_shipment_history(shipment_id)
        if not history:
            return None
        # Return the most recent update
        return history[-1]
