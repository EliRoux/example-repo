from tabulate import tabulate

class Shoe:

    def __init__(self, country, code, product, cost, quantity):
        self.country = country
        self.code = code
        self.product = product 
        self.cost = float(cost)
        self.quantity = int(quantity)


    def get_cost(self):
        return self.cost
  

    def get_quantity(self):
        return self.quantity


    def __str__(self):
        return f"{self.country}-{self.code}-{self.product}-R{self.cost}-{self.quantity}"


#=============Shoe list===========


shoe_list = []



#==========Functions outside the class==============

# This function reads the text file "inventory.txt" and is used to 
# Help use the data within that file for this program.
def read_shoes_data():
    try:
        with open("inventory.txt", "r") as file:
            lines = file.read().splitlines()
            data_lines = lines[1:]  

            for line in data_lines:
                parts = line.split(",")
                if len(parts) != 5:
                    continue

                country, code, product, cost, quantity = parts
                shoe = Shoe(country, code, product, cost, quantity)
                shoe_list.append(shoe)
                
    except FileNotFoundError:
        print("Error: inventory.txt not found.")

    except ValueError as v_error:
        print(f"Error converting data: {v_error}")

    except Exception as error:
        print(f"An unexpected error occurred: {error}")



# This function adds a new shoe to the stock.
def capture_shoes():
    try:
        country = input("Enter the country: ")
        code = input("Enter the product code: ")
        product = input("Enter the product name: ")
        cost = float(input("Enter the cost of the shoe: "))
        quantity = int(input("Enter the quantity in stock: "))

        new_shoe = Shoe(country, code, product, cost, quantity)
        shoe_list.append(new_shoe)
        print("Shoe added successfully!\n")

        with open("inventory.txt", "a") as file:
            file.write(f"{country},{code},{product},{cost},{quantity}\n")

    except ValueError:
        print("Invalid input! Cost must be a number and quantity must be an integer.\n")
        
    except Exception as error:
        print(f"An unexpected error occurred: {error}")

    


# This function displays all shoes in stock.
def view_all():

    if not shoe_list:
        print("No shoes to display.")
        return

    table = [[s.country, s.code, s.product, f"R{s.cost}", s.quantity] for s in shoe_list]
    headers = ["Country", "Code", "Product", "Cost", "Quantity"]
    print(tabulate(table, headers=headers, tablefmt="grid")) # This line I found by making use of chat gpt.


# This function finds the shoe with the least quantity and
# Requests the user if they would like to add quantity to this item.
def re_stock():

    # I have discovered "key=lambda" through chatgpt.
    # Chat GPTs definition of lambda:
    # A lambda is a way to define a small, anonymous function in a single line.
    # It's typically used when you need a simple function for a short time 
    # (usually passed as an argument to functions like map, filter, sorted, max, min, etc.).
    # I made use of this code again in line 162 to find the max quantity
    lowest_shoe = min(shoe_list, key=lambda s: s.get_quantity())
    print("Shoe with the lowest quantity:")
    print(lowest_shoe)

    choice = input("Would you like to restock this item? (yes/no): ").strip().lower()
    if choice == "yes":
        try:
            add_qty = int(input("Enter the quantity to add: "))
            if add_qty < 0:
                print("Quantity must be a positive number.")
                return

            lowest_shoe.quantity += add_qty
            print("Quantity updated successfully.")


            with open("inventory.txt", "r") as file:
                lines = file.readlines()


            updated_lines = []
            for line in lines:
                if line.strip().startswith("Country"):  # Preserve the header
                    updated_lines.append(line)
                    continue

                parts = line.strip().split(",")
                if len(parts) != 5:
                    updated_lines.append(line)
                    continue

                country, code, product, cost, quantity = parts
                if (code == lowest_shoe.code and 
                    product == lowest_shoe.product and 
                    country == lowest_shoe.country):
                    # Update the quantity
                    new_line = f"{country},{code},{product},{lowest_shoe.cost},{lowest_shoe.quantity}\n"
                    updated_lines.append(new_line)
                else:
                    updated_lines.append(line)

            with open("inventory.txt", "w") as file:
                file.writelines(updated_lines)

        except ValueError:
            print("Invalid input. Quantity must be an integer.")
    else:
        print("Restock cancelled.")



# This function is used to search for a shoe by entering its code.
def search_shoe():

    shoe_code = input("Please enter the shoe code for the shoe you are looking for: ").strip()

    for shoe in shoe_list:
        if shoe.code.lower() == shoe_code.lower():
            print(shoe)
            return

    print("Shoe with code {shoe_code} not found.")
    return None

def value_per_item():


    print("\nTotal Value per Item:")
    print("-" * 75)
    for shoe in shoe_list:
        value = shoe.get_quantity() * shoe.get_cost()
        print(f"{shoe.product} ({shoe.code}): R{value}")

# This function displays the shoe with the highest quantity in stock.
# Then displays it as an item on sale.
def highest_qty():

    highest_shoe = max(shoe_list, key=lambda s: s.get_quantity()) 

    print("This product has the most quantity and is now on sale:")
    print(highest_shoe)




#==========Main Menu=============

read_shoes_data()

while True:
    print("\n Shoe Inventory Menu ")
    print("-" * 75)
    print("1. Capture new shoe")
    print("2. View all shoes")
    print("3. Restock lowest quantity item")
    print("4. Search for a shoe by code")
    print("5. Calculate value per item")
    print("6. Display item with highest quantity")
    print("0. Exit")
    print("-" * 75)

    user_input = input("Enter your choice (0-6): ").strip()

    if user_input == "1":
        capture_shoes()
    elif user_input == "2":
        view_all()
    elif user_input == "3":
        re_stock()
    elif user_input == "4":
        search_shoe()
    elif user_input == "5":
        value_per_item()
    elif user_input == "6":
        highest_qty()
    elif user_input == "0":
        print("Goodbye!")
        break
    else:
        print("Error. Please enter a number from 0 to 6.")


# This was most definitely the hardest practical task so far.
# I had to do a lot of research using Stack Overflow and google search AI
# or if my code would not run properly I made use of chatgpt to check 
# for my mistakes and help explain to me what the mistake was and how to improve it.








