# Import libraries
from py_ads_client import ADSClient, ADSSymbol, BOOL, LREAL
from time import sleep

# ADS symbols used to send transfer commands to the PLS simulator
REMOTE_TRANSFER_ITEM = ADSSymbol("Remote.transfer_item", BOOL)
REMOTE_SRC_X = ADSSymbol("Remote.src_x", LREAL)
REMOTE_SRC_Y = ADSSymbol("Remote.src_y", LREAL)
REMOTE_DST_X = ADSSymbol("Remote.dst_x", LREAL)
REMOTE_DST_Y = ADSSymbol("Remote.dst_y", LREAL)

# PLC connection settings
PLC_IP = "127.0.0.1"
PLC_NET_ID = "127.0.0.1.1.1"
PLC_PORT = 851
LOCAL_NET_ID = "127.0.0.1.1.2"

# Fixed coordinate of the transfer slot / home pallet area
TRANSFER_SLOT_CENTER_X = 160.0
TRANSFER_SLOT_CENTER_Y = 410.0

# Storage area limits
AREA_MIN_X = 0.0
AREA_MIN_Y = 0.0
AREA_MAX_X = 400.0
STORAGE_MAX_Y = 300.0

# Block size
BLOCK_SIZE_MM = 60.0
BLOCK_HALF_SIZE_MM = BLOCK_SIZE_MM / 2.0


class Warehouse:
    def __init__(self, ads_client):
        self.ads = ads_client # Store ADS client connection
        self.positions = [] # List of all possible storage coordinates
        self.occupied = {} # Dictionary that stores whether each coordinate is occupied
        # Generate all valid storage positions in a grid
        x = AREA_MIN_X + BLOCK_HALF_SIZE_MM
        while x <= AREA_MAX_X - BLOCK_HALF_SIZE_MM:
            y = AREA_MIN_Y + BLOCK_HALF_SIZE_MM
            while y <= STORAGE_MAX_Y - BLOCK_HALF_SIZE_MM:
                pos = (x, y)
                self.positions.append(pos) # Add coordinate to the position list
                self.occupied[pos] = False # Initially every position is free
                y += BLOCK_SIZE_MM + 20
            x += BLOCK_SIZE_MM +20

    def show(self):
        # Count how many positions are currently occupied
        occupied = sum(1 for value in self.occupied.values() if value) 
        total = len(self.positions)

        # Print storage information
        print("\n--- STORAGE STATUS ---")
        print(f"Total positions: {total}")
        print(f"Occupied: {occupied}")
        print(f"Free: {total - occupied}")

    def transfer(self, src_x, src_y, dst_x, dst_y):
        # Send source coordinates to the PLC
        self.ads.write_symbol(REMOTE_SRC_X, src_x)
        self.ads.write_symbol(REMOTE_SRC_Y, src_y)
        # Send destination coordinates to the PLC
        self.ads.write_symbol(REMOTE_DST_X, dst_x)
        self.ads.write_symbol(REMOTE_DST_Y, dst_y)
        sleep(0.1)
        # Send a short pulse to start the transfer
        self.ads.write_symbol(REMOTE_TRANSFER_ITEM, True)
        sleep(0.1)
        self.ads.write_symbol(REMOTE_TRANSFER_ITEM, False)

    def add_block(self):
        # Search for the first free storage position
        for pos in self.positions:
            if not self.occupied[pos]:
                x, y = pos
                # Send pallet to imaging
                self.ads.write_symbol(ADSSymbol("Remote.send_pallet", BOOL), True)
                sleep(0.1)
                self.ads.write_symbol(ADSSymbol("Remote.send_pallet", BOOL), False)
                sleep(0.5)
                # Release pallet from imaging 
                self.ads.write_symbol(ADSSymbol("Remote.release_from_imaging", BOOL), True)
                sleep(0.1)
                self.ads.write_symbol(ADSSymbol("Remote.release_from_imaging", BOOL), False)
                sleep(0.5)
                # Move block from transfer to storage position
                self.transfer(
                    TRANSFER_SLOT_CENTER_X,
                    TRANSFER_SLOT_CENTER_Y,
                    x,
                    y
                )
                # Mark position as occupied
                self.occupied[pos] = True
                print(f"Block moved to {pos}")

                sleep(0.5)

                # Return the pallet back to home
                self.ads.write_symbol(ADSSymbol("Remote.return_pallet", BOOL), True)
                sleep(0.1)
                self.ads.write_symbol(ADSSymbol("Remote.return_pallet", BOOL), False)
                return

        print("Warehouse is full")# If no free position was found

    def remove_block(self):
        # Search for the first occupied storage position
        for pos in self.positions:
            if self.occupied[pos]:
                x, y = pos
                # Send pallet to imaging
                self.ads.write_symbol(ADSSymbol("Remote.send_pallet", BOOL), True)
                sleep(0.1)
                self.ads.write_symbol(ADSSymbol("Remote.send_pallet", BOOL), False)
                sleep(0.5)
                # Release pallet from imaging
                self.ads.write_symbol(ADSSymbol("Remote.release_from_imaging", BOOL), True)
                sleep(0.1)
                self.ads.write_symbol(ADSSymbol("Remote.release_from_imaging", BOOL), False)
                sleep(0.5)
                # Move block from storage position to the transfer
                self.transfer(
                    x,
                    y,
                    TRANSFER_SLOT_CENTER_X,
                    TRANSFER_SLOT_CENTER_Y
                )
                sleep(0.5)
                # Return pallet back to home
                self.ads.write_symbol(ADSSymbol("Remote.return_pallet", BOOL), True)
                sleep(0.1)
                self.ads.write_symbol(ADSSymbol("Remote.return_pallet", BOOL), False)
                # Mark this position as free
                self.occupied[pos] = False
                print(f"Block removed from {pos}")
                return

        print("Warehouse is empty")# If no occupied position was found


def main():
    # Create ADS client
    ads = ADSClient(local_ams_net_id=LOCAL_NET_ID)
    # Open connection to PLC simulator
    ads.open(
        target_ip=PLC_IP,
        target_ams_net_id=PLC_NET_ID,
        target_ams_port=PLC_PORT
    )
    
    warehouse = Warehouse(ads)# Create warehouse object

    # Terminal menu
    while True:
        print("\n--- MENU ---")
        print("1. Show status")
        print("2. Add block")
        print("3. Remove block")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            warehouse.show()

        elif choice == "2":
            warehouse.add_block()

        elif choice == "3":
            warehouse.remove_block()

        elif choice == "4":
            # Close ADS connection before exiting
            ads.close()
            print("Goodbye")
            break

        else:
            print("Wrong choice")

# Start the program
if __name__ == "__main__":
    main()