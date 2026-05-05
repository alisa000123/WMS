##Tier 2
#Adding an item
1. The system searches for the first free coordinate (x, y) in the storage area.
2. The system checks positions sequentially until it finds an empty one.
3. If a free position is found:
    * The block is moved to that coordinate.
    * The position is marked as occupied.
    * The coordinate is added to a FIFO sequence.
4. If no free position is available:
    * The system reports that the warehouse is full.

#FIFO logic
1. The system maintains a FIFO sequence of occupied coordinates.
2. Each new coordinates is added to the end of the sequence.
3. The sequence represents the arrival order of blocks. The first element corresponds to the oldest stored block.
4. Coordinates are removed from the beginning of the sequence

#Removing an item
1. The system takes the first coordinate from the FIFO sequence.
2. The block at that coordinate is removed.
3. The position is marked as free.
4. The coordinate is removed from the FIFO sequence.
5. If the sequence is empty:
    * The system reports that the warehouse is empty.
