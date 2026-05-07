#Tier 3
##Adding a block
1. The system searches for the first free coordinate (x, y) in the storage area.
2. The system checks each position until it finds an empty one.
3. If a free position is found:
    * A unique ID is assigned to the block.
    * The block is moved to that coordinate.
    * The position is marked as occupied.
    * The block information is stored:
        * block ID
        * coordinate
4. If no free position is available:
    * The system reports that the warehouse is full.

##Sequence logic
1. The system keeps a sequence of block IDs.
2. Each new block ID is added to the end of the sequence.
3. The sequence represents the arrival order of blocks.The first element corresponds to the oldest stored block.
4.IDs are removed from the beginning of the sequence.

##Removing a block by ID
1. The system asks the user which block to remove by ID.
2. The system checks if the block ID exists.
3. If the block exists:
    * The system finds its coordinate.
    * The block is removed from that coordinate.
    * The position is marked as free.
    * The block ID is removed from the sequence.
    * The block information is deleted from the system.
4. If the block does not exist:
    * The system reports that the block does not exist.