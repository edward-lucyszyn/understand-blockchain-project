"""
This module contains the class Blockchain. A blockchain is a list of blocks and a mempool.
"""
import json
import random
import config
from block import Block, InvalidBlock
from transaction import Transaction


class Blockchain(object):
    def __init__(self):
        pass

    @property
    def last_block(self):
        pass

    def add_transaction(self, transaction):
        """
        Add a new transaction to the mempool. Return True if the transaction is valid and not already in the mempool.
        :param transaction:
        :return: True or False
        """
        pass

    def new_block(self, block=None):
        """
        Create a new block from transactions choosen in the mempool.
        :param block: The previous block. If None, the last block of the chain is used.
        :return: The new block
        """
        pass

    def extend_chain(self, block):
        """
        Add a new block to the chain if it is valid (index, previous_hash, proof).
        :param block: A block
        :raise InvalidBlock if the block is invalid
        """
        pass

    def __str__(self):
        """
        String representation of the blockchain
        :return: str
        """
        pass

    def validity(self):
        """
        Check the validity of the chain.
        - The first block must be the genesis block
        - Each block must be valid
        - Each block must point to the previous one
        - A transaction can only be in one block
        :return: True if the chain is valid, False otherwise
        """
        pass

    def __len__(self):
        """
        Return the length of the chain
        :return:
        """
        pass

    def merge(self, other):
        """
        Modify the blockchain if other is longer and valid.
        :param other:
        :return:
        """
        pass

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


if __name__ == '__main__':
    print("Blockchain test")
    #simple_test()
    #merge_test()
