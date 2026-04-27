# Warehouse flow
Supplier → Warehouse → Customer

System must answer:
What is in stock?
What leaves the warehouse?
What remains?

# Three Levels of Complexity
## Tier 1 (required to pass)
Track quantities (bulk storage)

## Tier 2
FIFO batches (oldest first)

## Tier 3
Individual item tracking

# Workflow
1. Understand the problem
2. Define requirements
3. Design structure
4. Implement
5. Test
6. Improve

# Requirements for all tiers
The system must:
- User Interface
  - Indicates the stock state
    - Item count
    - Item info (depending on the tier)
  - Controls for operating the stock
    - Adding item
    - Removing item (according to the tier requirements)
- Usage
  - Single run operation. All actions must be able to performed by single launch of the program. The launch of the simulator is excluded from this requirement.
  - The operation of the software must be possible without seeing the source code
- Compatibility
  - The program must be compatible with the real device in the lab and the simulator. The demonstrations are made with the simulator.
- Software architecture
  - The source code must be clear and readable
  - Object oriented programming is to be used
  - The software needs to be documented in a proper way so that it can be understood
- Source code management
  - The commits are made in consistent manner
  - The stable versions are clearly marked
  - Each Tier has their own branch in Git
