#import sys
#import os
#import time
#import threading

#current_dir = os.path.dirname(os.path.abspath(__file__))
#sim_path = os.path.abspath(os.path.join(current_dir, "../block_storage_sim/src"))
#sys.path.append(sim_path)

#try:
    #from block_storage_simulator.simulator import BlockStorageSimulator
    #from block_storage_simulator.simulator.gui import SimulatorApp
    #from block_storage_simulator.simulator.constants import ConveyorState
    #from block_storage_simulator.simulator.models import TransferCommand
    #Has_Simulator = True
#except ImportError:
    #Has_Simulator = False
#if not Has_Simulator:
    #print("Error:simulator is not found")
    # sys.exit(1)


class Batch:
    def __init__(self, quantity):
        self.quantity = quantity


class Warehouse:
    def __init__(self):
        self.stock = {}

    def add_stock(self, product, quantity):
        if quantity <= 0:
            print("Invalid quantity")
            return

        batch = Batch(quantity)

        if product not in self.stock:
            self.stock[product] = []

        self.stock[product].append(batch)
        print(f"Added batch: {quantity} x {product}")

    def remove_stock(self, product, quantity):
        if quantity <= 0:
            print("Invalid quantity")
            return

        if product not in self.stock or not self.stock[product]:
            print(f"{product} is not in stock")
            return

        print(f"\nRemoving {quantity} x {product} using FIFO...")

        batches = self.stock[product]

        while quantity > 0 and batches:
            oldest_batch = batches[0]

            if oldest_batch.quantity <= quantity:
                print(f"Removed {oldest_batch.quantity} from OLDEST batch")
                quantity -= oldest_batch.quantity
                batches.pop(0)
            else:
                print(f"Removed {quantity} from OLDEST batch")
                oldest_batch.quantity -= quantity
                quantity = 0

        if quantity > 0:
            print(f"Not enough stock! Missing {quantity} x {product}")

        if product in self.stock and not self.stock[product]:
            del self.stock[product]

    def show_stock(self):
        if not self.stock:
            print("\nWarehouse is empty")
            return

        print("\n--- STOCK ---")

        for product, batches in self.stock.items():
            total = sum(batch.quantity for batch in batches)

            print(f"\nitem: {product}")
            print(f"Total: {total}")

            for i, batch in enumerate(batches):
                if i == 0:
                    label = "(oldest)"
                elif i == len(batches) - 1:
                    label = "(newest)"
                else:
                    label = ""

                print(f"Batch {i + 1}: {batch.quantity} {label}")


def main():
    warehouse = Warehouse()

    while True:
        print("\n--- MENU ---")
        print("1. Show stock")
        print("2. Add stock")
        print("3. Remove stock")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            warehouse.show_stock()

        elif choice == "2":
            product = input("Enter product name: ")

            try:
                quantity = int(input("Enter quantity: "))
                warehouse.add_stock(product, quantity)
            except ValueError:
                print("Invalid input")

        elif choice == "3":
            product = input("Enter product name: ")

            try:
                quantity = int(input("Enter quantity: "))
                warehouse.remove_stock(product, quantity)
            except ValueError:
                print("Invalid input")

        elif choice == "4":
            print("Exiting...")
            break

        else:
            print("Wrong choice")


if __name__ == "__main__":
    main()