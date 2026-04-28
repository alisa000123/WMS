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

class Item:
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name

    def __str__(self):
        return f"ID: {self.item_id}, Name: {self.name}"


class Warehouse:
    def __init__(self):
        self.items = []
        self.next_id = 1

    def add_item(self, name):
        if name == "":
            print("Invalid name")
            return

        item = Item(self.next_id, name)
        self.items.append(item)
        self.next_id += 1

        print(f"Added: {item}")

    def remove_item(self, name):
        if not self.items:
            print("Warehouse is empty")
            return

        for item in self.items:
            if item.name == name:
                self.items.remove(item)
                print(f"Removed: {item}")
                return

        print("Item not found")

    def show_stock(self):
        if not self.items:
            print("\nEmpty warehouse")
            return

        print("\n--- STOCK ---")
        print(f"Total items: {len(self.items)}")

        for i, item in enumerate(self.items):
            if i == 0:
                label = "(oldest)"
            elif i == len(self.items) - 1:
                label = "(newest)"
            else:
                label = ""

            print(f"{i+1}. {item} {label}")


def main():
    warehouse = Warehouse()

    while True:
        print("\n--- MENU ---")
        print("1. Show stock")
        print("2. Add item")
        print("3. Remove item")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            warehouse.show_stock()

        elif choice == "2":
            name = input("Enter item name: ")
            warehouse.add_item(name)

        elif choice == "3":
            name = input("Enter item name: ")
            warehouse.remove_item(name)

        elif choice == "4":
            break

        else:
            print("Wrong choice")


if __name__ == "__main__":
    main()