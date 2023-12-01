import tkinter as tk
from tkinter import messagebox, simpledialog
import utils, block, blockchain, customer, twowheel, transaction
from ecdsa import SigningKey, NIST384p
import hashlib
from tkinter import ttk
from PIL import Image, ImageTk
import json
class BlockchainApp:
    """Runs the blockchain"""
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to BikeChain")
        self.root.iconbitmap("logo.ico")
        self.blockchain = blockchain.Blockchain()
        self.tree = ttk.Treeview(root)
        self.tree["columns"] = ("Index", "Previous Hash", "Proof", "Timestamp", "Transactions")
        self.menu_label = tk.Label(root, text="Menu")
        self.menu_label.pack()


        image = Image.open("assets/logo.ico")  # Remplacez "path/vers/votre/logo.png" par le chemin de votre fichier image
        image = image.resize((100, 100))
        logo = ImageTk.PhotoImage(image)

        # Ajouter le logo à la fenêtre
        logo_label = tk.Label(root, image=logo)
        logo_label.image = logo  # Garde une référence à l'image pour éviter la garbage collection
        logo_label.pack()
        self.view_button = ttk.Button(root, text="Show blockchain", command=self.view_chain)
        self.view_button.pack(pady=10)
        self.mine_button = ttk.Button(root, text="Mine new block", command=self.mine_b)
        self.mine_button.pack(pady=10)
        self.sell_button = ttk.Button(root, text="Enter transaction", command=self.sell_bike)
        self.sell_button.pack(pady=10)

        self.exit_button = ttk.Button(root, text="Exit", command=self.root.destroy)
        self.exit_button.pack(pady=10)

    def view_chain(self):
        block=self.blockchain.last_block
        self.tree.insert("", "end", values=(block.index, block.previous_hash, block.proof, block.timestamp, block.transactions))
        for column in self.tree["columns"]:
            self.tree.column(column, anchor="w")
            self.tree.heading(column, text=column)

        self.tree.pack(expand=tk.YES, fill=tk.BOTH)

    def sell_bike(self):
        seller_name = simpledialog.askstring("Sell Bike", "Enter your name:")
        bike_details = simpledialog.askstring("Sell Bike", "Enter bike details:")
        buyer_name = simpledialog.askstring("Sell Bike", "Enter buyer name:")
        sk = SigningKey.generate()
        bike=twowheel.TwoWheel(str(bike_details))
        sk_ppl = SigningKey.generate(curve=NIST384p)
        pk_ppl = sk_ppl.get_verifying_key()
        Cust = customer.Customer(pk_ppl, seller_name)
        t = transaction.Transaction(blockchain.create_message_str(bike.get_has_serial_number(), hashlib.sha256(Cust.get_pk.to_pem()).hexdigest()))
        t.sign(sk)
        self.blockchain.add_transaction(t)
        if seller_name and bike_details:
            messagebox.showinfo("Success", "Transactions successfully added!")
        else:
            messagebox.showwarning("Warning", "Seller name and bike details are required!")

    def mine_b(self):
        b = self.blockchain.new_block()
        b.mine()
        self.blockchain.extend_chain(b)

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()

