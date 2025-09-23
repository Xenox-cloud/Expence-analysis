import csv
import os
from datetime import datetime
from ml_model import predict_category, train_model, MODEL_FILE

# CSV file name
FILE_NAME = "expenses.csv"

# Expense categories
CATEGORIES = ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"]


def get_category():
    while True:
        print("\nSelect a category:")
        for i, cat in enumerate(CATEGORIES, 1):
            print(f"{i}. {cat}")

        choice = input(f"Enter choice (1-{len(CATEGORIES)}): ")

        if not choice.isdigit():
            print("❌ Please enter a number.")
            continue

        choice = int(choice)

        if 1 <= choice <= len(CATEGORIES):
            return CATEGORIES[choice - 1]
        else:
            print(f"❌ Invalid choice. Please enter between 1 and {len(CATEGORIES)}.")


def add_expense():
    """Collects user input and saves an expense to CSV, can auto-predict category"""
    date = datetime.now().strftime("%Y-%m-%d")
    amount = float(input("Enter amount: "))
    description = input("Enter description: ")

    # Ask user if they want ML prediction
    use_ai = input("Auto-detect category using AI? (y/n): ").lower()
    if use_ai == "y":
        category = predict_category(description, amount)
        if category:
            print(f"🤖 Predicted category: {category}")
        else:
            print("❌ Prediction failed, please select manually.")
            category = get_category()
    else:
        category = get_category()

    # Save to CSV
    file_exists = os.path.isfile(FILE_NAME)
    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Date", "Amount", "Description", "Category"])
        writer.writerow([date, amount, description, category])

    print("\n✅ Expense added successfully!\n")

    # Optional: retrain model automatically after each addition
    train_model(FILE_NAME)
