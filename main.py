from py_ads_client import ADSClient, ADSSymbol, BOOL, LREAL
from time import sleep
from collections import deque


REMOTE_TRANSFER_ITEM = ADSSymbol("Remote.transfer_item", BOOL)
REMOTE_SRC_X = ADSSymbol("Remote.src_x", LREAL)
REMOTE_SRC_Y = ADSSymbol("Remote.src_y", LREAL)
REMOTE_DST_X = ADSSymbol("Remote.dst_x", LREAL)
REMOTE_DST_Y = ADSSymbol("Remote.dst_y", LREAL)

REMOTE_SEND_PALLET = ADSSymbol("Remote.send_pallet", BOOL)
REMOTE_RELEASE_FROM_IMAGING = ADSSymbol("Remote.release_from_imaging", BOOL)
REMOTE_RETURN_PALLET = ADSSymbol("Remote.return_pallet", BOOL)


PLC_IP = "127.0.0.1"
PLC_NET_ID = "127.0.0.1.1.1"
PLC_PORT = 851
LOCAL_NET_ID = "127.0.0.1.1.2"

TRANSFER_SLOT_CENTER_X = 160.0
TRANSFER_SLOT_CENTER_Y = 410.0

AREA_MIN_X = 0.0
AREA_MIN_Y = 0.0
AREA_MAX_X = 400.0
STORAGE_MAX_Y = 300.0

BLOCK_SIZE_MM = 60.0
BLOCK_HALF_SIZE_MM = BLOCK_SIZE_MM / 2.0


class Warehouse:
    def __init__(self, ads_client):
        self.ads = ads_client
        self.positions = []
        self.occupied = {}
        self.fifo_queue = deque()

        x = AREA_MIN_X + BLOCK_HALF_SIZE_MM
        while x <= AREA_MAX_X - BLOCK_HALF_SIZE_MM:
            y = AREA_MIN_Y + BLOCK_HALF_SIZE_MM
            while y <= STORAGE_MAX_Y - BLOCK_HALF_SIZE_MM:
                pos = (x, y)
                self.positions.append(pos)
                self.occupied[pos] = False
                y += BLOCK_SIZE_MM
            x += BLOCK_SIZE_MM

    def show(self):
        occupied = sum(1 for value in self.occupied.values() if value)
        total = len(self.positions)

        print("\n--- STORAGE STATUS ---")
        print(f"Total positions: {total}")
        print(f"Occupied: {occupied}")
        print(f"Free: {total - occupied}")
        print(f"FIFO queue: {list(self.fifo_queue)}")

    def transfer(self, src_x, src_y, dst_x, dst_y):
        self.ads.write_symbol(REMOTE_SRC_X, src_x)
        self.ads.write_symbol(REMOTE_SRC_Y, src_y)
        self.ads.write_symbol(REMOTE_DST_X, dst_x)
        self.ads.write_symbol(REMOTE_DST_Y, dst_y)

        sleep(0.1)

        self.ads.write_symbol(REMOTE_TRANSFER_ITEM, True)
        sleep(0.1)
        self.ads.write_symbol(REMOTE_TRANSFER_ITEM, False)

    def add_block(self):
        for pos in self.positions:
            if not self.occupied[pos]:
                x, y = pos

                # send pallet
                self.ads.write_symbol(REMOTE_SEND_PALLET, True)
                sleep(0.1)
                self.ads.write_symbol(REMOTE_SEND_PALLET, False)
                sleep(0.5)

                # release from imaging
                self.ads.write_symbol(REMOTE_RELEASE_FROM_IMAGING, True)
                sleep(0.1)
                self.ads.write_symbol(REMOTE_RELEASE_FROM_IMAGING, False)
                sleep(0.5)

                # move to storage
                self.transfer(
                    TRANSFER_SLOT_CENTER_X,
                    TRANSFER_SLOT_CENTER_Y,
                    x,
                    y
                )

                self.occupied[pos] = True
                self.fifo_queue.append(pos)

                print(f"Block added to {pos}")

                sleep(0.5)

                # return pallet
                self.ads.write_symbol(REMOTE_RETURN_PALLET, True)
                sleep(0.1)
                self.ads.write_symbol(REMOTE_RETURN_PALLET, False)

                return

        print("Warehouse is full")

    def remove_block(self):
        if not self.fifo_queue:
            print("Warehouse is empty")
            return

        pos = self.fifo_queue.popleft()

        if not self.occupied[pos]:
            print(f"FIFO error at {pos}")
            return

        x, y = pos

        # send pallet
        self.ads.write_symbol(REMOTE_SEND_PALLET, True)
        sleep(0.1)
        self.ads.write_symbol(REMOTE_SEND_PALLET, False)
        sleep(0.5)

        # release from imaging
        self.ads.write_symbol(REMOTE_RELEASE_FROM_IMAGING, True)
        sleep(0.1)
        self.ads.write_symbol(REMOTE_RELEASE_FROM_IMAGING, False)
        sleep(0.5)

        # move from storage
        self.transfer(
            x,
            y,
            TRANSFER_SLOT_CENTER_X,
            TRANSFER_SLOT_CENTER_Y
        )

        self.occupied[pos] = False

        print(f"Oldest block removed from {pos}")

        sleep(0.5)

        # return pallet
        self.ads.write_symbol(REMOTE_RETURN_PALLET, True)
        sleep(0.1)
        self.ads.write_symbol(REMOTE_RETURN_PALLET, False)


def main():
    ads = ADSClient(local_ams_net_id=LOCAL_NET_ID)

    ads.open(
        target_ip=PLC_IP,
        target_ams_net_id=PLC_NET_ID,
        target_ams_port=PLC_PORT
    )

    warehouse = Warehouse(ads)

    while True:
        print("\n--- MENU ---")
        print("1. Show status")
        print("2. Add block")
        print("3. Remove block FIFO")
        print("4. Exit")

        choice = input("Choose: ")

        if choice == "1":
            warehouse.show()

        elif choice == "2":
            warehouse.add_block()

        elif choice == "3":
            warehouse.remove_block()

        elif choice == "4":
            ads.close()
            print("Goodbye")
            break

        else:
            print("Wrong choice")


if __name__ == "__main__":
    main()