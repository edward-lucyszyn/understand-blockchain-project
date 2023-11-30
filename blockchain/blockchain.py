"""
This module contains the class Blockchain. A blockchain is a list of blocks and a mempool.
"""
import json
import random
import config
from block import Block, InvalidBlock
from transaction import Transaction
import utils


class Blockchain(object):
    def __init__(self):
        self.chain = [Block(None)]
        self.mempool = []
        pass

    @property
    def last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        """
        Add a new transaction to the mempool. Return True if the transaction is valid and not already in the mempool.
        :param transaction:
        :return: True or False
        """
        if utils.str_to_time(transaction.date) > utils.str_to_time(utils.get_time()):
            return False
        if transaction in self.mempool:
            return False
        if transaction.verify():
            self.mempool.append(transaction)
            return True
        else:
            return False

    def new_block(self, block=None):
        """
        Create a new block from transactions choosen in the mempool.
        :param block: The previous block. If None, the last block of the chain is used.
        :return: The new block
        """
        if block is None:
            block = self.last_block

        data = {
            'index': self.__len__(),
            'timestamp': utils.get_time(),
            'transactions': self.mempool[0: config.blocksize],
            'proof': 0,
            'previous_hash': block.hash()
        }
        self.mempool = self.mempool[config.blocksize:]
        return Block(data)

    def extend_chain(self, block):
        """
        Add a new block to the chain if it is valid (index, previous_hash, proof).
        :param block: A block
        :raise InvalidBlock if the block is invalid
        """
        if block.index != self.__len__() or block.previous_hash != self.last_block.hash() or not block.valid_proof():
            raise InvalidBlock
        else:
            self.chain.append(block)

    def __str__(self):
        """
        String representation of the blockchain
        :return: str
        """
        d = {
            "chain": [block.data for block in self.chain],
        }   
        return str(json.dumps(d, sort_keys=True))

    def validity(self):
        """
        Check the validity of the chain.
        - The first block must be the genesis block
        - Each block must be valid
        - Each block must point to the previous one
        - A transaction can only be in one block
        :return: True if the chain is valid, False otherwise
        """
        if not(self.chain[0].index == 0 and self.chain[0].timestamp == "2023-11-24 00:00:00.000000" and self.chain[0].transactions == [] and self.chain[0].proof == 0 and self.chain[0].previous_hash == "0" * 64):
            return False
        
        for block in self.chain:
            if not block.validity():
                return False
            
        for i in range(len(self.chain) - 1):
            if self.chain[i+1].previous_hash != self.chain[i].hash():
                return False
            
        all_transactions = []
        for i in range(len(self.chain) - 1):
            for j in range(len(self.chain[i].transactions)):
                if self.chain[i].transactions[j] in all_transactions:
                    return False
                else:
                    all_transactions.append(self.chain[i].transactions[j])

        return True

    def __len__(self):
        """
        Return the length of the chain
        :return:
        """
        return len(self.chain)

    def merge(self, other):
        """
        Modify the blockchain if other is longer and valid.
        :param other:
        :return:
        """
        if self.__len__() >= other.__len__():
            return self
        else:
            self.chain = other.chain[:]
            #self.mempool = other.mempool[:]
        return self

    def log(self):
        print(self)
        Transaction.log(self.mempool)

        for b in self.chain:
            b.log()


def merge_test():
    from ecdsa import SigningKey
    blockchain = Blockchain()
    sk = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk)
        blockchain.add_transaction(t)

    blockchain2 = Blockchain()
    sk2 = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk2)
        blockchain2.add_transaction(t)

    for i in range(3):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    for i in range(2):
        b = blockchain2.new_block()
        b.mine()
        blockchain2.extend_chain(b)

    blockchain.merge(blockchain2)
    blockchain2.merge(blockchain)

    for i in range(2):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    for i in range(4):
        b = blockchain2.new_block()
        b.mine()
        blockchain2.extend_chain(b)

    blockchain.merge(blockchain2)
    blockchain2.merge(blockchain)

    blockchain.log()


def simple_test():
    from ecdsa import SigningKey
    blockchain = Blockchain()
    sk = SigningKey.generate()
    for i in range(100):
        t = Transaction(f"Message {i}")
        t.sign(sk)
        blockchain.add_transaction(t)

    print(blockchain)
    for i in range(3):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    print(blockchain)
    print(b.validity())
    print(len(blockchain))


def test_bike():
    from ecdsa import SigningKey, NIST384p
    from transaction import Transaction
    sk = SigningKey.generate(curve=NIST384p)
    t1 = Transaction("Test for transaction with bike")

    blockchain = Blockchain()

    transactions = [Transaction(f"Transaction for bike {i}") for i in range(10)]
    for t in transactions:
        t.sign(sk)
        blockchain.add_transaction(t)
    Transaction.log(transactions)

    print(blockchain)
    for _ in range(4):
        b = blockchain.new_block()
        b.mine()
        blockchain.extend_chain(b)

    print("Test for blockchain validity :", b.validity())

    blockchain.log()

if __name__ == '__main__':
    print("Blockchain test")
    # simple_test()
    # merge_test()
    test_bike()
