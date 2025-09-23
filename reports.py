import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime
from data_entry import FILE_NAME


def view_reports():
    if not os.path.isfile(FILE_NAME):
        print("No expenses found yet.")
        return

    df = pd.read_csv(FILE_NAME)

    print("\nReports Menu")
    print("1. View today’s expenses")
    print("2. View this month’s total")
    print("3. View category breakdown (with chart)")
    print("4. View daily trend this month (with chart)")
    choice = input("Enter choice: ")

    today = datetime.now().strftime("%Y-%m-%d")
    this_month = datetime.now().strftime("%Y-%m")

    if choice == "1":
        today_expenses = df[df["Date"] == today]
        if today_expenses.empty:
            print("\nNo expenses recorded today.")
        else:
            print("\nToday’s Expenses:")
            print(today_expenses)

    elif choice == "2":
        month_expenses = df[df["Date"].str.startswith(this_month)]
        total = month_expenses["Amount"].sum()
        print(f"\n Total spending this month ({this_month}): {total} Tk")

    elif choice == "3":
        breakdown = df.groupby("Category")["Amount"].sum()
        print("\n Category-wise Breakdown:")
        print(breakdown)

        breakdown.plot(kind="pie", autopct='%1.1f%%', figsize=(6, 6))
        plt.title("Category-wise Spending")
        plt.ylabel("")
        plt.show()

    elif choice == "4":
        month_expenses = df[df["Date"].str.startswith(this_month)]
        if month_expenses.empty:
            print("\nNo expenses recorded this month.")
        else:
            daily_trend = month_expenses.groupby("Date")["Amount"].sum()
            print("\n Daily Spending Trend:")
            print(daily_trend)

            daily_trend.plot(kind="line", marker="o")
            plt.title(f"Daily Spending Trend ({this_month})")
            plt.xlabel("Date")
            plt.ylabel("Amount Spent (Tk)")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            plt.show()
    else:
        print("Invalid choice.")
