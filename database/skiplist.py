# Created via Gemini 2.5 Flash

import random


class SkipNode:
    """
    Represents a node in the Skip List.
    Each node has a value and a list of 'next' pointers, one for each level.
    """

    def __init__(self, value, level):
        self.value = value
        self.next = [None] * (level + 1)  # Pointers for each level

    def __str__(self):
        return f"Node({self.value}, levels={len(self.next)})"


class SkipList:
    """
    Implements a Skip List data structure.
    """
    HEAD_VALUE = -float('inf')  # A value smaller than any possible key
    MAX_LEVEL = 16              # Maximum number of levels in the Skip List
    PROBABILITY = 0.5           # Probability of increasing a node's level

    def __init__(self):
        # Head node with MAX_LEVEL pointers
        self.head = SkipNode(self.HEAD_VALUE, self.MAX_LEVEL)
        self.level = 0  # Current maximum level of the Skip List

    def _random_level(self):
        """
        Generates a random level for a new node.
        The level increases with a probability (PROBABILITY) up to MAX_LEVEL.
        """
        lvl = 0
        while random.random() < self.PROBABILITY and lvl < self.MAX_LEVEL:
            lvl += 1
        return lvl

    def insert(self, value):
        """
        Inserts a new value into the Skip List.
        """
        update = [None] * (self.MAX_LEVEL +
                           1)  # Stores nodes to update pointers

        current = self.head
        # Traverse from the highest level down to find the insertion point
        for i in range(self.level, -1, -1):
            while current.next[i] and current.next[i].value < value:
                current = current.next[i]
            update[i] = current  # Store the node to update at this level

        # Move to the lowest level (level 0) to check for duplicates
        # current.next[0] is the node *after* where 'value' should be
        current = current.next[0]

        if current and current.value == value:
            # Value already exists, no insertion needed (or update if handling duplicates)
            # For simplicity, we just return for now.
            return

        # Determine a random level for the new node
        new_level = self._random_level()

        # If the new node's level is higher than the current max level of the Skip List,
        # update the head's pointers for these new levels.
        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.head
            self.level = new_level

        # Create the new node
        new_node = SkipNode(value, new_level)

        # Insert the new node by updating pointers at all relevant levels
        for i in range(new_level + 1):
            new_node.next[i] = update[i].next[i]
            update[i].next[i] = new_node

    def starts_with(self, prefix: str):
        results = []
        current = self.head
        # Traverse from the highest level down
        for i in range(self.level, -1, -1):
            while current.next[i] and current.next[i].value[:len(prefix)] < prefix:
                current = current.next[i]

        # At level 0, current.next[0] should be the potential node
        current = current.next[0]

        if current and current.value[:len(prefix)] == prefix:
            while current and current.value[:len(prefix)] == prefix:
                results.append(current.value)
                current = current.next[0]
        return results

    def search(self, value):
        """
        Searches for a value in the Skip List.
        Returns the node if found, None otherwise.
        """
        current = self.head
        # Traverse from the highest level down
        for i in range(self.level, -1, -1):
            while current.next[i] and current.next[i].value < value:
                current = current.next[i]

        # At level 0, current.next[0] should be the potential node
        current = current.next[0]

        if current and current.value == value:
            return current.value  # Found
        else:
            return None  # Not found

    def delete(self, value):
        """
        Deletes a value from the Skip List.
        Returns True if deleted, False if not found.
        """
        update = [None] * (self.MAX_LEVEL + 1)
        current = self.head

        # Traverse from highest level down to find nodes whose pointers need updating
        for i in range(self.level, -1, -1):
            while current.next[i] and current.next[i].value < value:
                current = current.next[i]
            update[i] = current

        # At level 0, current.next[0] is the node to potentially delete
        # Renamed to avoid confusion with traversal 'current'
        current_to_delete = current.next[0]

        if current_to_delete and current_to_delete.value == value:
            # Update pointers to bypass the node to be deleted
            # Iterate up to the effective level of the node being deleted
            # which is len(current_to_delete.next) - 1
            # Iterate from 0 up to its highest level
            for i in range(len(current_to_delete.next)):
                # Only update if current node points to it
                if update[i].next[i] == current_to_delete:
                    update[i].next[i] = current_to_delete.next[i]

            # Adjust the Skip List's overall max level if the deleted node
            # was at the highest level and no other nodes exist at that level.
            while self.level > 0 and self.head.next[self.level] is None:
                self.level -= 1
            return True  # Successfully deleted
        else:
            return False  # Value not found

    def display(self):
        """
        Prints the Skip List in a readable format.
        """
        print(f"\n--- Skip List (Max Level: {self.level}) ---")
        for i in range(self.level, -1, -1):
            print(f"Level {i:2d}: ", end="")
            node = self.head
            while node:
                print(f"{node.value}", end=" -> ")
                node = node.next[i]
            print("None")
        print("------------------------------")
