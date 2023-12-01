import hashlib

from ecdsa import SigningKey
import utils
import json
from ecdsa import VerifyingKey, BadSignatureError
from rich.console import Console
from rich.table import Table
import hashlib
from twowheel import TwoWheel

class Company:
    def __init__(self, data):
        if 'name' in data:
            self.name = data['name']
        else: self.name = None
        if 'description' in data:
            self.description = data['description']
        else: self.description = None
        self.creation_date = utils.get_time()
        self.pk_list = data['pk_list']

    @property
    def get_name(self):
        return self.name

    @property
    def get_pk_list(self):
        return self.pk_list

    @property
    def get_data(self):
        d = {
            'name': self.name,
            'creation_date': self.creation_date,
            'description:': self.description
        }
        return d
    
    def __lt__(self, other):
        """
        Compare two transactions. The comparison is based on the hash of the transaction if it is defined else, the date.
        :param other: a transaction
        :return: True or False
        """
        return utils.str_to_time(self.creation_date) < utils.str_to_time(other.creation_date)

    @staticmethod
    def log(companies):
        """
        Print a nice log of set of the transactions
        :param transactions:
        :return:
        """
        table = Table(title=f"List of companies")
        table.add_column("Name", justify="left", style="cyan")
        table.add_column("Description", justify="left", style="cyan")
        table.add_column("Creation date", justify="left", style="cyan")
        table.add_column("Public Keys", justify="left", style="cyan")

        for t in sorted(companies):
            S = t.pk_list[0].to_pem().hex()[:7] + "..." + t.pk_list[0].to_pem().hex()[-7:]
            for i in range(1, len(t.pk_list)):
                S += '\n' + t.pk_list[i].to_pem().hex()[:7] + "..." + t.pk_list[i].to_pem().hex()[-7:]
            table.add_row(
                None if t.name is None else t.name,
                None if t.description is None else t.description,
                t.creation_date[:10],
                S
            )

        console = Console()
        console.print(table)


def test_companies():
    from ecdsa import SigningKey, NIST384p
    sk = SigningKey.generate(curve=NIST384p)
    sk2 = SigningKey.generate(curve=NIST384p)
    pk = sk.get_verifying_key()
    pk2 = sk2.get_verifying_key()
    data_decathlon = {
        'name': 'Decathlon',
        'description': 'à fond la forme !',
        'pk_list': [pk, pk2]
    }
    Decathlon = Company(data_decathlon)

    data_intersport = {
        'name': 'Intersport',
        'description': 'Le sport commence ici',
        'pk_list': [pk, pk2]
    }
    Intersport = Company(data_intersport)

    Company.log([Decathlon, Intersport])

if __name__ == '__main__':
    test_companies()
