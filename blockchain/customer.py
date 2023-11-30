
from ecdsa import SigningKey
import utils
import json
from ecdsa import VerifyingKey, BadSignatureError
from rich.console import Console
from rich.table import Table

class Customer:
    def __init__(self, pk, name=None, age=None, description=None):
        self.name = name
        self.pk = pk
        self.description = description
        self.creation_date = utils.get_time()
        self.age = age

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
            'age': self.age,
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
        table.add_column("Age", justify="left", style="cyan")
        table.add_column("Description", justify="left", style="cyan")
        table.add_column("Creation date", justify="left", style="cyan")
        table.add_column("Public Key", justify="left", style="cyan")

        for t in sorted(customers):
            table.add_row(
                None if t.name is None else t.name,
                None if t.age is None else t.age,
                None if t.description is None else t.description,
                t.creation_date[:10],
                t.pk.to_pem().hex()[:7] + "..." + t.pk.to_pem().hex()[-7:]
            )

        console = Console()
        console.print(table)

def test():
    from ecdsa import SigningKey, NIST384p
    sk = SigningKey.generate(curve=NIST384p)
    pk = sk.get_verifying_key()
    Maria  = Customer(pk, 'Maria', '22')
    print(Maria.get_name)
    print(Maria.get_pk.to_pem().hex())
    print(Maria.get_data)
    Customer.log([Maria])

if __name__ == '__main__':
    test()