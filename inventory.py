'''
This program simulates a stock-taking system for a Nike warehouse. As a store
manager, the goal is to maintain, analyse, and update shoe inventory data in
order to optimise warehouse organisation and delivery efficiency.
'''

from tabulate import tabulate


#========The beginning of the class==========
class Shoe:
   
    def __init__(self, country, code, product, cost, quantity):
        '''
         Initialise a Shoe object.
        '''
        # Assigning attributes to the object
        self.country = country
        self.code = code
        self.product = product
        self.cost = cost
        self.quantity = quantity
        
    def get_cost(self):
        '''
        Return the cost of the shoe.
        '''
        return self.cost

    def get_quantity(self):
        '''
        Return the stock quantity of the shoe.
        '''
        return self.quantity

    def __str__(self):
        '''
        Return a readable string representation of the shoe object.
        '''
        return (f"{self.country} | {self.code} | {self.product} | "
                f"Cost: R{self.cost} | Quantity: {self.quantity}")


#=============Shoe list===========
'''
The list will be used to store a list of objects of shoes.
'''
# This list will store all Shoe objects created from the text file
shoe_list = []


#==========Functions outside the class==============
def read_shoes_data():
    '''
    Reads data from inventory.txt, creates Shoe objects,
    and saves them in shoe_list. Includes error handling.
    '''
    try:
        # Try to open the inventory file
        with open("inventory.txt", "r") as f:
            next(f)  # Skip the header line

            # Read the rest of the lines
            for line in f:
                try:
                    # Split the line by commas
                    country, code, product, cost, quantity = line.strip().split(",")

                    # Create a Shoe object and append it to the shoe list
                    shoe = Shoe(country, code, product, float(cost), int(quantity))
                    shoe_list.append(shoe)
                except ValueError:
                    # Handles formatting errors
                    print(f"Error reading line: {line.strip()}")

    except FileNotFoundError:
        # Handles missing file
        print("inventory.txt file not found.")

def capture_shoes():
    '''
   Collect input from user and create a new Shoe object.
    '''
   # Collect data from user
    country = input("Country: ")
    code = input("Code: ")
    product = input("Product Name: ")

    try:
        cost = float(input("Cost: ")) # Convert to float
        quantity = int(input("Quantity: ")) # Convert to int

        # Create and store the new object
        new_shoe = Shoe(country, code, product, cost, quantity)
        shoe_list.append(new_shoe)

        print("Shoe added successfully.")

    except ValueError:
        print("Invalid input for cost or quantity. Please enter numeric values.")

def view_all():
    '''
    Prints all shoes using the __str__ method.
    '''
    if not shoe_list: # Handle empty list
        print("No shoes loaded.")
        return

    # Prepare data for tabulation
    table_data = []

    for shoe in shoe_list:
        table_data.append([
            shoe.country, 
            shoe.code, 
            shoe.product, 
            shoe.cost, 
            shoe.quantity
            ])

    # Define headers for the table
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]

    # Print the table
    print("\n=== Shoe Inventory Table ===")
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

def re_stock():
    '''
    Finds the shoe with the lowest quantity and allows user to restock it.
    Updates the text file afterwards.
    '''
    if not shoe_list: # Handle empty list
        print("No shoes loaded.")
        return
    
    # Find the shoe with the lowest quantity using lambda
    lowest_stock_shoe = min(shoe_list, key=lambda s: s.quantity)
    print(f"Shoe with the lowest stock: {lowest_stock_shoe}")

    # Ask user if they want to restock
    choice = input("Would you like to restock this item? (Yes/No): ").lower()
    if choice == "yes":
        try:
            amount = int(input("Enter the quantity to add: "))
            lowest_stock_shoe.quantity += amount

            # Save changes to file
            update_inventory_file()
            print("Stock updated successfully.")

        except ValueError:
            print("Invalid input. Please enter a numeric value.")

def search_shoe():
    '''
    Search for a shoe using its code.
    '''
    code = input("\nEnter shoe code to search: ")

    # Search through the shoe list
    for shoe in shoe_list:
        if shoe.code == code:
            print(shoe)
            return # Exit after finding the shoe

    # If no match found
    print("No shoe found with that code.")

def value_per_item():
    '''
    Calculates and prints the total value of each shoe:
    Formula: cost * quantity
    '''
    # Prepare data for tabulation
    total_value = []

    for shoe in shoe_list:
        value = shoe.cost * shoe.quantity
        total_value.append([ 
            shoe.product, 
            shoe.code, 
            value,
            ])

    # Define headers for the table
    headers = ["Product", "Code", "Total Value (R)"]

    # Print the table
    print("\n=== Total Value per Item ===")
    print(tabulate(total_value, headers=headers, tablefmt="grid"))

def highest_qty():
    '''
   Finds the shoe with the highest quantity and displays it.
    '''
    if not shoe_list: # Handle empty list
        print("No shoes in inventory yet.")
        return
    
    # Find the shoe with the highest quantity using lambda
    highest_stock_shoe = max(shoe_list, key=lambda s: s.quantity)

    print(f"{highest_stock_shoe.product} ({highest_stock_shoe.code})")
    print(f"In Stock: {highest_stock_shoe.quantity}")
    print("STATUS: *** FOR SALE ***")

def update_inventory_file():
    '''
    Writes the updated shoe_list back into inventory.txt.
    Ensures file is always up to date after restocking.
    '''
    with open("inventory.txt", "w") as f:
        # Write the heade
        f.write("Country,Code,Product,Cost,Quantity\n")

        # Wite each shoe object
        for s in shoe_list:
            f.write(f"{s.country},{s.code},{s.product},{s.cost},{s.quantity}\n")


#==========Main Menu=============
'''
Main loop menu allowing user to navigate the program.
'''
read_shoes_data()  # Load data at program start

while True:
    # Display menu options
    print("""
========== Inventory Menu ==========
1. View all shoes
2. Add a new shoe
3. Restock lowest quantity item
4. Search shoe by code
5. View value per item
6. Show item with highest quantity
7. Exit
""")
    
    choice = input("Enter your choice: ")

    # Matching input to function
    if choice == "1":
        view_all()
    elif choice == "2":
        capture_shoes()
    elif choice == "3":
        re_stock()
    elif choice == "4":
        search_shoe()
    elif choice == "5":
        value_per_item()
    elif choice == "6":
        highest_qty()
    elif choice == "7":
        print("Exiting program.")
        break
    else:
        print("Invalid choice. Please select a valid option.")

# Program entry point
if __name__ == "__main__":
    read_shoes_data()