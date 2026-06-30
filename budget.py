#Budget Management Terminal App
import json
import statistics
import csv

FILE = "budget.json"

def load_data():
    
    try:
        with open(FILE, "r") as f:
            return json.load(f)
        
    except FileNotFoundError:
        return []
    
def save_data(data):
    
    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)


#Creates or edits a month's spendings. This function asks for the month in a (YYYY-MM) format and a set of values, then saves them in labels that form an entry (the new month)
#If the input month already exists, it will just overwrite the values of each label with the newly input ones, hence the option "Create or update month"

def create_month(data):
     
     month = input("\nType the month and the year (YYYY-MM): \n")
     if valid_month(month) == False:
          print("Error, type again")
          return
     
     income = float(input("\nHow much did you earn this month?\n"))
     rent = float(input("\nHow much did you spend in rent?\n"))
     food = float(input("\nHow much did you spend in food?\n"))
     transport = float(input("\nHow much did you spend in transport?\n"))
     leisure = float(input("\nHow much did you spend in leisure?\n"))
     savings = income - (rent+food+transport+leisure)

     new_entry = {
          "month": month,
          "income": income,
          "rent": rent,
          "food": food,
          "transport": transport,
          "leisure": leisure,
          "savings": savings
     }

     for i, entry in enumerate(data):
        
        if entry["month"] == month:
            data[i] = new_entry
            save_data(data)
            print("Month updated successfully!")
            return
    
     data.append(new_entry)
     save_data(data)

     print("Month saved successfully!")

#Displays all the succesfully created entries and all their labels, with the values tagged in $
#Checks if any entry is to be found and sorts the entries from oldest entry to newest judging by the (YYYY-MM) value.

def show(data):

     if not data:

          print("No data found")
          
     sorted_data = sorted(data, key=lambda x: x["month"])
    
     for entry in sorted_data:
        print("\n----------------------")
        print(f"Month: {entry['month']}")
        print(f"Income: ${entry['income']}")
        print(f"Rent: ${entry['rent']}")
        print(f"Food: ${entry['food']}")
        print(f"Transport: ${entry['transport']}")
        print(f"Leisure: ${entry['leisure']}")
        print(f"Savings: ${entry['savings']}")

#Displays a set of useful statistics about your expenses, income and savings
#Again checks for the existence of entries, and goes through all entries and saves the income, savings, and the sum of all the expenses into new values in order to make the statistics

def stats(data):

     if not data:

          print("No data found")
          return
     
     income = [entry['income'] for entry in data]
     saving = [entry['savings'] for entry in data]
     expenses = [entry["rent"] + entry["food"] + entry["transport"] + entry["leisure"] for entry in data]
     
     months_rec = len(data)
     total_income = sum(income)
     total_savings = sum(saving)
     average_income = statistics.mean(income)
     median_income = statistics.median(income)
     average_saving = statistics.mean(saving)
     median_saving = statistics.median(saving)
     highest_income = max(income)
     highest_saving = max(saving)

     print("\n-------Statistics---------------")
     print(f"\nMonths recorded: {months_rec}\n")
     print(f"Total income: ${total_income:.2f}\n")
     print(f"Total savings: ${total_savings:.2f}\n")
     print(f"Average income: ${average_income:.2f}\n")
     print(f"Median income: ${median_income:.2f}\n")
     print(f"Average savings: ${average_saving:.2f}\n")
     print(f"Median savings: ${median_saving:.2f}\n")
     print(f"Highest income: ${highest_income:.2f}\n")
     print(f"Highest savings: ${highest_saving:.2f}\n")
     print(f"Average expenses: ${statistics.mean(expenses):.2f}\n")
     print(f"Median expenses: ${statistics.median(expenses):.2f}\n")

#Displays the mean of all the expenses by category

def stats_cat(data):
    
    
    food = [entry['food']for entry in data]
    rent = [entry['rent']for entry in data]
    transport = [entry['transport']for entry in data]
    leisure = [entry['leisure']for entry in data]
    
    print("\n-------Statistics by categories---------------")
    print(f"\nAverage rent: ${statistics.mean(rent):.2f}\n")
    print(f"Average food: ${statistics.mean(food):.2f}\n")
    print(f"Average transport: ${statistics.mean(transport):.2f}\n")
    print(f"Average leisure: ${statistics.mean(leisure):.2f}\n")
    
#Displays the evolution of income, savings and expenses for all months
    
def trends(data):
    
    sorted_data = sorted(data, key=lambda x: x["month"])
    
    months = [entry["month"] for entry in sorted_data]
    income = [entry["income"] for entry in sorted_data]
    savings = [entry["savings"] for entry in sorted_data]
    expenses = [entry["rent"] + entry["food"] + entry["transport"] + entry["leisure"] for entry in sorted_data]

    print("\n------- Trends -----------")

    print("\nIncome:\n")
    for m, i in zip(months, income):
        print(f"{m}: {i}")

    print("\nSavings:\n")
    for m, s in zip(months, savings):
        print(f"{m}: {s}")

    print("\nExpenses:\n")
    for m, e in zip(months, expenses):
        print(f"{m}: {e}")

#Deletes an entry chosen

def delete_month(data):

    if not data:
        
        print("No data found.")
        return

    month = input("Enter the month to delete (YYYY-MM): ")

    if not valid_month(month):
        
        print("Invalid month.")
        return

    for i, entry in enumerate(data):
        if entry["month"] == month:
            del data[i]
            save_data(data)
            print("Month deleted successfully!")
            return

    print("Month not found.")

#Saves all the entries with their labels into a CSV file openable in Excel/Sheets etc. through the CSV library

def export_csv(data):

    if not data:
        
        print("No data found.")
        return

    with open("budget.csv", "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "month",
                "income",
                "rent",
                "food",
                "transport",
                "leisure",
                "savings"
            ]
        )

        sorted_data = sorted(data, key=lambda x: x["month"])

        writer.writeheader()
        writer.writerows(sorted_data)

    print("\nBudget exported successfully!\n")

#Checks that the month and year input on the create_month function is valid

def valid_month(month):
     
     if len(month)!= 7:
          return False
     
     if month[4]!="-":
          return False
     
     year = month[:4]
     month_part = month[5:]

     if not (year.isdigit() and month_part.isdigit()):
          return False
     
     month_num = int(month_part)
     
     if month_num < 1 or month_num > 12:
        return False
     
     return True

data= load_data()

#Decorative ASCII logo for initiation

print("""---Welcome to--------------------------------------------------------------------------------------
             -------------------|\\------|-----|----|\\---------____---------____---_______-------------------------
             -------------------|-\\-----|-----|----|--\\------/----\\-------|----------|----------------------------
             -------------------|-/-----|-----|----|---|----/------|------|----------|----------------------------
             -------------------|/------|-----|----|---|----|-------------|____------|----------------------------
             -------------------|\\------|-----|----|--/-----|----___------|----------|----------------------------
             -------------------|-/-----|-----|----|-/-------\\-----/------|----------|----------------------------
             -------------------|/-------\\___/-----|/---------\\___/-------|____------|-------by Xavier Fo---------""")

while True:
    print("\n1) Input/update a month\n")
    print("2) View Records\n")
    print("3) Show Statistics\n")
    print("4) Delete a month\n")
    print("5) Export CSV\n")
    print("6) QUIT\n")

    choice = int(input("Choose: "))
    
    if choice == 1:
          create_month(data)

    elif choice == 2:
         show(data)

    elif choice == 3:
         stats(data)
         while True:
             print("\n1) See statistics per category\n")
             print("2) See trends\n")
             print("3) RETURN\n")

             choice_two = int(input("Choose: "))

             if choice_two == 1:
                 stats_cat(data)

             elif choice_two == 2:
                 trends(data)  
             
             elif choice_two == 3:
                 break

             else:
                 print("\nInvalid choice\n")

    elif choice == 4:
        delete_month(data)
    
    elif choice == 5:
        export_csv(data)
     
    elif choice == 6:
        print("\nGoodbye.\n")
        break

    else:
        print("\nInvalid choice\n")

    
