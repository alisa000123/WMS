import sys
import os
import time
import threading

current_dir = os.path.dirname(os.path.abspath(__file__))
sim_path = os.path.abspath(os.path.join(current_dir, "../block_storage_sim/src"))
sys.path.append(sim_path)

try:
    from block_storage_simulator.simulator import BlockStorageSimulator
    from block_storage_simulator.gui import SimulatorApp
    from block_storage_simulator.constants import ConveyorState
    from block_storage_simulator.models import TransferCommand
    Has_Simulator = True
except ImportError:
    Has_Simulator = False
if not Has_Simulator:
    print("Error:simulator is not found")
    sys.exit(1)

class Warehouse:
    def __init__(self):
        self.stock = {}
        self.history = []

    def add_stock(self, product, quantity):
        if quantity <= 0:
            print("Quantity must be greater than 0")
            return

        if product in self.stock:
            self.stock[product] += quantity
        else:
            self.stock[product] = quantity

        self.history.append(f"IN: {product} x{quantity}")
        print(f"Added {quantity} of {product}")

    def remove_stock(self, product, quantity):
        if product not in self.stock:
            print("Product not found")
            return

        if self.stock[product] < quantity:
            print("Not enough stock")
            return

        self.stock[product] -= quantity
        self.history.append(f"OUT: {product} x{quantity}")
        print(f"Removed {quantity} of {product}")

        if self.stock[product] == 0:
            del self.stock[product]

    def show_stock(self):
        print("\nCurrent stock:")
        if not self.stock:
            print("Empty")
            return

        for product, quantity in self.stock.items():
            print(f"{product}: {quantity}")

    def show_history(self):
        print("\nTransaction history:")
        if not self.history:
            print("No transactions yet")
            return

        for item in self.history:
            print(item)


def main():
    warehouse = Warehouse()

    while True:
        print("\n--- MENU ---")
        print("1. Show stock")
        print("2. Add stock")
        print("3. Remove stock")
        print("4. Show history")
        print("5. Exit")

        choice = input("Choose: ")

        if choice == "1":
            warehouse.show_stock()
            input("Press Enter to continue...")

        elif choice == "2":
            product = input("Product name: ")
            quantity = int(input("Quantity: "))
            warehouse.add_stock(product, quantity)
            input("Press Enter to continue...")

        elif choice == "3":
            product = input("Product name: ")
            quantity = int(input("Quantity: "))
            warehouse.remove_stock(product, quantity)
            input("Press Enter to continue...")

        elif choice == "4":
            warehouse.show_history()
            input("Press Enter to continue...")

        elif choice == "5":
            print("Bye!")
            break

        else:
            print("Wrong choice")


if __name__ == "__main__":
    main()