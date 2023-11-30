import tkinter as tk
from tkinter import messagebox, simpledialog
import utils, block, blockchain, customer, twowheel

class BlockchainApp:
    """Runs the blockchain"""
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to BikeChain")

        self.blockchain = blockchain.Blockchain()

        self.menu_label = tk.Label(root, text="Blockchain Menu")
        self.menu_label.pack()

        self.view_button = tk.Button(root, text="View Bikes for Sale", command=self.view_bikes)
        self.view_button.pack()

        self.sell_button = tk.Button(root, text="Sell Bike", command=self.sell_bike)
        self.sell_button.pack()

        self.exit_button = tk.Button(root, text="Exit", command=self.root.destroy)
        self.exit_button.pack()

    def view_bikes(self):
        bikes_for_sale = "\n".join([f"Index: {block.index}, Seller: {block.data}" for block in self.blockchain.chain[1:]])
        messagebox.showinfo("Bikes for Sale", bikes_for_sale)

    def sell_bike(self):
        seller_name = simpledialog.askstring("Sell Bike", "Enter your name:")
        bike_details = simpledialog.askstring("Sell Bike", "Enter bike details:")

        if seller_name and bike_details:
            latest_block = self.blockchain.last_block()
            self.blockchain.new_block(latest_block, f"Seller: {seller_name}, Bike: {bike_details}")
            messagebox.showinfo("Success", "Bike successfully added for sale!")
        else:
            messagebox.showwarning("Warning", "Seller name and bike details are required!")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()

