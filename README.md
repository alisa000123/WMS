##Tier 1
#Adding an item
1. The system searches for the first free coordinate (x, y) in the warehouse.
2. The system checks positions sequentially until it finds an empty one.
3. If a free position is found:
    * The block is moved to that coordinate.
    * The position is marked as occupied.
    * The coordinate is stored in the system.
4. If no free position is available:
    * The system reports that the warehouse is full.

#Removing an item
1. The system searches for the first occupied coordinate.
2. The system selects the first occupied position based on storage order.
3. The block is removed from that coordinate.
4. The position is marked as free.
5. If no occupied positions exist:
    * The system reports that the warehouse is empty.