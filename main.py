from data_entry import add_expense
from reports import view_reports


if __name__ == "__main__":
    while True:
        print("\n--- Expense Tracker ---")
        print("1. Add Expense")
        print("2. View Reports")
        print("3. Exit")
        action = input("Choose an option: ")

        if action == "1":
            add_expense()
        elif action == "2":
            view_reports()
        elif action == "3":
            print("👋 Bye! Your data is saved in 'expenses.csv'")
            break
        else:
            print("Invalid option. Please try again.")
