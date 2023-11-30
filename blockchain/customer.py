import hashlib

from ecdsa import SigningKey
import utils
import json
from ecdsa import VerifyingKey, BadSignatureError
from rich.console import Console
from rich.table import Table
import hashlib
from twowheel import TwoWheel

class Customer:
    def __init__(self, pk, name=None, description=None):
        self.name = name
        self.pk = pk
        self.description = description
        self.creation_date = utils.get_time()

    @property
    def get_name(self):
        return self.name

    @property
    def get_pk(self):
        return self.pk

    @property
    def get_data(self):
        d = {
            'name': self.name,
            'creation_date': self.creation_date
        }
        return d

    @staticmethod
    def log(customers):
        """
        Print a nice log of set of the transactions
        :param transactions:
        :return:
        """
        table = Table(title=f"List of customers")
        table.add_column("Name", justify="left", style="cyan")
        table.add_column("Description", justify="left", style="cyan")
        table.add_column("Creation date", justify="left", style="cyan")
        table.add_column("Public Key", justify="left", style="cyan")

        for t in sorted(customers):
            table.add_row(
                None if t.name is None else t.name,
                None if t.description is None else t.description,
                t.creation_date[:10],
                t.pk.to_pem().hex()[:7] + "..." + t.pk.to_pem().hex()[-7:]
            )

        console = Console()
        console.print(table)


def test_customer():
    from ecdsa import SigningKey, NIST384p
    sk = SigningKey.generate(curve=NIST384p)
    pk = sk.get_verifying_key()
    Maria = Customer(pk, 'Maria')
    print(Maria.get_name)
    print(Maria.get_pk.to_pem().hex())
    print(Maria.get_data)
    Customer.log([Maria])

def create_message_str(serialNo, hashPublicKeyBuyer):
    d = {
        "serialNo": serialNo,
        "hashPublicKeyBuyer": hashPublicKeyBuyer
    }
    return str(d)

def test_transaction():
    from ecdsa import SigningKey, NIST384p
    from blockchain import Blockchain
    from transaction import Transaction
    Blockchain = Blockchain()

    sk_comp = SigningKey.generate(curve=NIST384p)
    pk_comp = sk_comp.get_verifying_key()
    Company = Customer(pk_comp, 'Company')
    Customer.log([Company])

    sk_paul = SigningKey.generate(curve=NIST384p)
    pk_paul = sk_paul.get_verifying_key()
    Paul = Customer(pk_paul, 'Paul')
    Customer.log([Paul])

    bike = TwoWheel('12313593452')
    t1 = Transaction(create_message_str(bike.get_has_serial_number(), hashlib.sha256(Paul.get_pk.to_pem()).hexdigest()))
    t1.sign(sk_comp)
    Blockchain.add_transaction(t1)
    Blockchain.log()
    b = Blockchain.new_block()
    b.mine()
    Blockchain.extend_chain(b)
    Blockchain.log()
    print(Blockchain.search_owner(hashlib.sha256(Paul.get_pk.to_pem()).hexdigest(), bike.get_has_serial_number()))
    t2 = Transaction(create_message_str(bike.get_has_serial_number(), hashlib.sha256(Paul.get_pk.to_pem()).hexdigest()))
    t2.sign(sk_comp)
    print(Blockchain.add_transaction(t2))


    sk = SigningKey.generate(curve=NIST384p)
    pk = sk.get_verifying_key()
    Tom = Customer(pk, 'Tom')
    bike = TwoWheel('123135934523')

if __name__ == '__main__':
    #test_customer()
    test_transaction()
