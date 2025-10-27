"""Inventory Management System Module."""

import json
from datetime import datetime
import os


class InventorySystem:
    """Handles item stock operations and transaction logging."""

    def __init__(self, file="inventory.json"):
        """Initialize inventory and load data if file exists."""
        self.stock_data = {}
        self.transaction_logs = []
        self.file = file
        self.load_data()

    def add_item(self, item="default", qty=0):
        """Add a quantity of an item to the stock."""
        if (not isinstance(item, str)
                or not isinstance(qty, int)
                or qty < 0):
            self.transaction_logs.append(
                f"{datetime.now()}: ERROR - Invalid input for add_item. "
                "Item must be string and quantity must be non-negative "
                "integer."
            )
            return

        if not item:
            return

        self.stock_data[item] = self.stock_data.get(item, 0) + qty
        self.transaction_logs.append(
            f"{datetime.now()}: Added {qty} of {item}"
        )

    def remove_item(self, item, qty):
        """Remove a quantity of an item from the stock."""
        if (not isinstance(item, str)
                or not isinstance(qty, int)
                or qty < 0):
            self.transaction_logs.append(
                f"{datetime.now()}: ERROR - Invalid input for remove_item. "
                "Item must be string and quantity must be non-negative "
                "integer."
            )
            return

        try:
            current_qty = self.stock_data.get(item, 0)
            if current_qty < qty:
                self.transaction_logs.append(
                    f"{datetime.now()}: WARNING - Insufficient stock to "
                    f"remove {qty} of {item}. Current stock: {current_qty}."
                )
                return

            self.stock_data[item] -= qty
            if self.stock_data[item] <= 0:
                self.transaction_logs.append(
                    f"{datetime.now()}: Item {item} stock reached zero "
                    "and was removed."
                )
                del self.stock_data[item]
        except KeyError:
            self.transaction_logs.append(
                f"{datetime.now()}: WARNING - Attempted to remove "
                f"non-existent item: {item}"
            )
        except RuntimeError as e:
            self.transaction_logs.append(
                f"{datetime.now()}: ERROR removing {item}: {e}"
            )

    def get_qty(self, item):
        """Return the stock quantity for an item."""
        return self.stock_data.get(item, 0)

    def load_data(self):
        """Load stock data from the JSON file."""
        try:
            if os.path.exists(self.file):
                with open(self.file, "r", encoding="utf-8") as f:
                    data = f.read()
                    if data:
                        self.stock_data = json.loads(data)
                        self.transaction_logs.append(
                            f"{datetime.now()}: Data loaded successfully."
                        )
        except FileNotFoundError:
            self.transaction_logs.append(
                f"{datetime.now()}: WARNING - Data file not found."
            )
        except json.JSONDecodeError as e:
            self.transaction_logs.append(
                f"{datetime.now()}: ERROR decoding JSON: {e}"
            )
        except IOError as e:
            self.transaction_logs.append(
                f"{datetime.now()}: ERROR accessing file: {e}"
            )

    def save_data(self):
        """Save current stock data to the JSON file."""
        try:
            with open(self.file, "w", encoding="utf-8") as f:
                f.write(json.dumps(self.stock_data, indent=4))
        except IOError as e:
            self.transaction_logs.append(
                f"{datetime.now()}: ERROR saving data: {e}"
            )

    def print_data(self):
        """Print the current inventory stock report."""
        print("Items Report")
        for i, qty in self.stock_data.items():
            print(f"{i} -> {qty}")

    def check_low_items(self, threshold=5):
        """Return list of items with stock below the threshold."""
        return [i for i, qty in self.stock_data.items() if qty < threshold]


def main():
    """Main execution block to demonstrate inventory functionality."""
    system = InventorySystem()

    system.add_item("apple", 10)
    system.add_item("banana", 15)
    system.add_item(123, "ten")
    system.add_item("grape", 5)
    system.remove_item("apple", 3)
    system.remove_item("orange", 1)
    system.remove_item("grape", 10)

    print("Apple stock:", system.get_qty("apple"))
    print("Low items:", system.check_low_items())
    system.save_data()

    print("\n--- Transaction Logs ---")
    for log in system.transaction_logs:
        print(log)


if __name__ == '__main__':
    main()
