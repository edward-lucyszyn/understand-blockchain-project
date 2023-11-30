"""
This module contains the class Block. A block is a list of transactions. The first block is called the genesis block.
"""

import hashlib
import json
import config
import utils
from rich.console import Console
from rich.table import Table


class InvalidBlock(Exception):
    pass


class Block(object):
    def __init__(self, data=None):
        """
        If data is None, create a new genesis block. Otherwise, create a block from data (a dictionary).
        Raise InvalidBlock if the data are invalid.
        """
        if data is None:
            self.index = 0
            self.timestamp = "2023-11-24 00:00:00.000000"
            self.transactions = []
            self.proof = 0
            self.previous_hash = "0" * 64
        else:
            try: 
                self.index = data['index']
                self.timestamp = data['timestamp']
                self.transactions = data['transactions']
                self.proof = data['proof']
                self.previous_hash = data['previous_hash']
            except:
                raise InvalidBlock
        pass

    def next(self, transactions):
        """
        Create a block following the current block
        :param transactions: a list of transactions, i.e. a list of messages and their signatures
        :return: a new block
        """
        data = {}
        data['index'] = self.index + 1
        data['timestamp'] = utils.get_time()
        data['transactions'] = transactions
        data['proof'] = 0
        data['previous_hash'] = self.hash()
        new_block = Block(data)
        return new_block
    
    @property
    def data(self):
        d = {
            "index": self.index,
            "timestamp": self.timestamp,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
            "transactions": [transaction.data for transaction in self.transactions]
        }
        return d

    def hash(self):
        """
        Hash the current block (SHA256). The dictionary representing the block is sorted to ensure the same hash for
        two identical block. The transactions are part of the block and are not sorted.
        :return: a string representing the hash of the block
        """
        d = {
            "index": self.index,
            "timestamp": self.timestamp,
            "proof": self.proof,
            "previous_hash": self.previous_hash,
            "transactions": [transaction.data for transaction in self.transactions]
        }
        return hashlib.sha256(str(json.dumps(d, sort_keys=True)).encode()).hexdigest()

    def __str__(self):
        """
        String representation of the block
        :return: str
        """
        d = {
            "index": self.index,
            "hash": self.hash(),
            "timestamp": self.timestamp,
            "transactions_number": len(self.transactions)
        }
        return str(json.dumps(d, sort_keys=True))

    def valid_proof(self, difficulty=config.default_difficulty):
        """
        Check if the proof of work is valid. The proof of work is valid if the hash of the block starts with a number
        of 0 equal to difficulty.

        If index is 0, the proof of work is valid.
        :param difficulty: the number of 0 the hash must start with
        :return: True or False
        """
        hash = self.hash()
        if hash[:difficulty] == "0"*difficulty:
            return True
        else:
            return False

    def mine(self, difficulty=config.default_difficulty):
        """
        Mine the current block. The block is valid if the hash of the block starts with a number of 0 equal to
        config.default_difficulty.
        :return: the proof of work
        """
        i = self.proof
        while not self.valid_proof(difficulty):
            i += 1
            self.proof = i
        return i

    def validity(self):
        """
        Check if the block is valid. A block is valid if it is a genesis block or if:
        - the proof of work is valid
        - the transactions are valid
        - the number of transactions is in [0, config.blocksize]
        :return: True or False
        """
        if self.index == 0 and self.timestamp == "2023-11-24 00:00:00.000000" and self.transactions == [] and self.proof == 0 and self.previous_hash == "0" * 64:
            return True
        
        if len(self.transactions) < 0 or len(self.transactions) > config.blocksize:
            return False
        
        for transaction in self.transactions:
            if not transaction.verify():
                return False
        
        if self.valid_proof():
            return True
        else:
            return False


    def log(self):
        """
        A nice log of the block
        :return: None
        """
        table = Table(
            title=f"Block #{self.index} -- {self.hash()[:7]}...{self.hash()[-7:]} -> {self.previous_hash[:7]}...{self.previous_hash[-7:]}")
        table.add_column("Author", justify="right", style="cyan")
        table.add_column("Message", style="magenta", min_width=30)
        table.add_column("Date", justify="center", style="green")

        for t in self.transactions:
            table.add_row(t.author[:7] + "..." + t.author[-7:], t.message, t.date[:-7])

        console = Console()
        console.print(table)


def test():
    from ecdsa import SigningKey
    from transaction import Transaction
    sk = SigningKey.generate()
    transactions = [Transaction(f"Message {i}") for i in range(10)]
    for t in transactions:
        t.sign(sk)

    Transaction.log(transactions)

    blocks = [Block()]
    for i in range(5):
        blocks.append(blocks[-1].next(transactions[i * 2:(i + 1) * 2]))
        blocks[-1].mine()

    for b in blocks:
        b.log()

def test_bike():
    from ecdsa import SigningKey, NIST384p
    from transaction import Transaction
    sk = SigningKey.generate(curve=NIST384p)
    t1 = Transaction("Test for transaction with bike")
    transactions = [Transaction(f"Transaction for bike {i}") for i in range(10)]
    for t in transactions:
        t.sign(sk)
    Transaction.log(transactions)
    blocks = [Block()]
    blocks.append(blocks[0].next(transactions))

    for b in blocks:
        b.log()

    print("Test for validity :", blocks[1].validity())
    blocks[1].mine()

    for b in blocks:
        b.log()
    
    
if __name__ == '__main__':
    print("Test Block")
    # test()
    test_bike()
