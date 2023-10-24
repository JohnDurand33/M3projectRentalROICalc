import pickle

class RentalProperty:

    def __init__(self, property_id):
        self.property_id = property_id
        self.data_file = f'property_{property_id}_data.pkl'

        # Initialize data dictionary
        self.categories = {
            "monthly income": {},
            "monthly expenses": {},
            "up front investments": {}
        }

        # Load user's data if it exists
        self.load_data()

    # Attempt to load saved rental data associated with property ID  
    def load_data(self):
        try:
            with open(self.data_file, 'rb') as file:
                self.categories = pickle.load(file)
                print("Data successfuly loaded")
        except FileNotFoundError:

            # If the data file doesn't exist, initialize with default dictionaries
            self.categories = {
                "monthly income": {'rent' : 0
                },
                "monthly expenses": {"taxes": 0, 
                    "insurance": 0, 
                    "water/sewer": 0, 
                    "electric": 0, 
                    "garbage": 0, 
                    "gas": 0,
                    "HOA dues": 0,
                    "lawncare": 0, 
                    "vacancy": 0, 
                    "repairs": 0, 
                    "capital expenditures": 0, 
                    "management": 0, 
                    "mortgage": 0},
                "up front investments": {"downpayment": 0,
                    "closing costs": 0,
                    "up front repairs": 0}
            }

    def save_data(self):
        with open(self.data_file, 'wb') as file:
            pickle.dump(self.categories, file)

    # Function to get a valid numeric input from the user
    def get_valid_amt(self, input_message):
        while True:
            try:
                value = float(input(input_message))
                return value
            except ValueError:
                print("Invalid input. Please enter a valid number.")
            
    #Function that converts to float when 'done' needs to be an option
    def convert_to_valid_amt(self, new_value):
        format_value = round(float(new_value), 2)
        return format_value

    #Ask analyst if they additional category items to add
    def ask_addtl_items(self, category_name):
        while True:
            response = input(f"Do you have additional items to enter? (y/n)").lower()
            if response == 'y':
                self.enter_custom_items(category_name)
            elif response == 'n':
                break
            else:
                print("Invalid input. Please try again")
    
    #Ask analyst if they category items to remove
    def ask_del_items(self, category_name):
        for item, value in self.categories[category_name].items():
                print(f"{item.title()}: ${value:.2f}")
        while True:
            response = input(f"Do you have items to remove? (y/n)").lower()
            if response == 'y':
                self.delete_items(category_name)
            elif response == 'n':
                break
            else:
                print("Invalid input. Please try again")

    #Final pass to confirm amounts are correct
    def confirm_amounts(self, category_name):
        print(f"\nCurrent {category_name.title()} details:")

        while True:
            for item, value in self.categories[category_name].items():
                print(f"{item.title()}: ${value:.2f}")
            response = input(f"\nAre the '{category_name.title()}' details listed accurate? (y/n): ")
            if response.lower() == 'n':
                while True:
                    update_item = input(f"Please enter the name of the incorrect item you wish to update (or 'done' to finish): ")
                    item = update_item.lower()
                    if item == "done":
                        break
                    elif item in self.categories[category_name]:
                        new_name = input(f"Enter the corrected name for '{item.title()}', or 'done' to finish: ")
                        if new_name == 'done':
                            break
                        else:
                            self.categories[category_name][new_name] = self.categories[category_name][item]
                            new_value = input(f"Enter the correct value for '{new_name.title()}' or Enter to keep the same amount: ")
                            if new_value == '':
                                del self.categories[category_name][item]
                                break
                            else:
                                self.categories[category_name][new_name] = self.convert_to_valid_amt(new_value)
                                del self.categories[category_name][item] 
                    else:
                        print(f"{update_item.title()} not found.")
            elif response == 'y':
                break
            else:
                print("Invalid input. Please enter a 'y' or 'n'.")

    #Data method if property ID is recognized and data exists
    def review_data(self, category_name):
        category_dict = self.categories[category_name]
        items_to_review = list(category_dict)
        i = 0
        print(f"Reviewing existing {category_name.title()}:")
        while i < len(items_to_review):
            item = items_to_review[i]
            value = category_dict[item]

            response = input(f"I show the existing data for '{item.title()}' with a value of ${value:.2f}.  Is this accurate? (Y/N/back, or 'done' to skip reviewing the {category_name.title()} section: ")
            response = response.lower()
            if response == 'done':
                break
            elif response == 'n':
                while True:
                    new_value = self.get_valid_amt(f"Enter the correct value for '{item.title()}': ")
                    category_dict[item] = new_value
                    response = input(f"'{item.title()}' has been updated to ${new_value:.2f}.  Is this correct? (y/n)").lower()
                    if response == 'n':
                        continue
                    elif response == 'y':
                        self.categories[category_name][item] = new_value
                        i+=1
                        break
                    else:
                        print("Invalid input. Please enter a 'y' or 'n'.")
            elif response == 'y':
                i += 1
            elif response == 'back':
                i = max(0, i-1)
            else:
                print("Invalid input. Please enter 'y' or 'n'.")

        self.ask_addtl_items(category_name)
        self.ask_del_items(category_name)
        self.confirm_amounts(category_name)

    # Function to enter predefined items, and validate each naming convention and value once entered
    def enter_predefined_items(self, category_name):
        category_dict = self.categories[category_name]
        predefined_items = list(category_dict)
        print(f"Reviewing {category_name.title()}:")
         
        i = 0 
        while i < len(predefined_items):
            item = predefined_items[i]
            value = self.get_valid_amt(f"Please enter value for the '{item.title()}' Category: ")
            print(f"'{item.title()}' with a value of ${value:.2f} has been added to '{category_name.title()}'.")

            response = input(f"\nIs this correct?: (y/n/back): ").lower()
            if response == 'y':
                self.categories[category_name][item] = value
                i += 1  
            elif response == 'n':
                continue  
            elif response == 'back':
                if i > 0:
                    i -= 1 
                else:
                    print("You are already at the first item.")
            else:
                print("Invalid input. Please enter 'y', 'n', or 'back'.")

        self.ask_addtl_items(category_name)
        self.confirm_amounts(category_name)
        
    def enter_custom_items(self, category_name):
        while True:
            item = input(f"Enter name of additional {category_name.title()} item (or 'done' to finish): ")
            if item.lower() == 'done':
                break
            else:
                value = self.get_valid_amt(f"Enter value for {item.title()}: ")
                self.categories[category_name][item] = value
                (f"\nI've updated '{item.title()}' with a value of ${value:.2f}.")

    def delete_items(self, category_name):
        print(f"\nCurrent {category_name.title()} details:")
        while True:
            for item, value in self.categories[category_name].items():
                print(f"{item}: ${value:.2f}")
            response = input(f"\nPlease enter the '{category_name.title()}' category you would like remove ('done' to finish): ")
            if response == 'done':
                break
            elif response in self.categories[category_name]:
                del self.categories[category_name][response]
            else:
                print("Invalid input received.")

    # Function to calculate rental ROI
    def calculate_rental_roi(self):
        self.categories["Rental ROI"] = {}
        monthly_income_total = sum(self.categories["monthly income"].values())
        print(f"Monthly Income Total: ${monthly_income_total}0")
        self.categories["Rental ROI"]["monthly income total"] = monthly_income_total
        monthly_expenses_total = sum(self.categories["monthly expenses"].values())
        print(f"Monthly Expenses Total: ${monthly_expenses_total}0")
        self.categories["Rental ROI"]["monthly expenses total"] = monthly_expenses_total
        annualized_cashflow = (monthly_income_total - monthly_expenses_total) * 12
        print(f"Annualized Cash Flow: ${annualized_cashflow}0")
        self.categories["Rental ROI"]["annualized cashflow"] = annualized_cashflow
        total_investments = sum(self.categories["up front investments"].values())
        self.categories["Rental ROI"]["up front investments total"] = total_investments
        print(f"Investments Total: ${total_investments}0")
        rental_roi = (annualized_cashflow / total_investments) * 100
        self.categories["Rental ROI"]["total rental roi"] = rental_roi
        return rental_roi

def main():
    print("Welcome to the Rental ROI Calculator!")
    property_id = input("Enter your property's ID: ")
    
    property_1 = RentalProperty(property_id)

    # Enter income details
    print("\nMonthly Income:")
    if all(value == 0 for value in property_1.categories["monthly income"].values()):
        property_1.enter_predefined_items("monthly income")
    else:
        property_1.review_data("monthly income")

    # Enter expenses details
    print("\nMonthly Expenses:")
    if all(value == 0 for value in property_1.categories["monthly expenses"].values()):
        property_1.enter_predefined_items("monthly expenses")
    else:
        property_1.review_data("monthly expenses")

    # Enter investment details
    print("\nTotal Investments:")
    if all(value == 0 for value in property_1.categories["up front investments"].values()):
        property_1.enter_predefined_items("up front investments")
    else:
        property_1.review_data("up front investments")

    # Calculate and display rental ROI
    rental_roi = property_1.calculate_rental_roi()
    print(f"\nRental ROI: {rental_roi:.2f}%")

    # Save user's data
    property_1.save_data()

if __name__ == "__main__":
    main()