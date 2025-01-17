import matplotlib.pyplot as plt
import pandas as pd
import os

# Initialize data
data_file = 'expenses.csv'

# Check if the file exists, if not create it
if not os.path.exists(data_file):
    df = pd.DataFrame(columns=["Date", "Category", "Amount"])
    df.to_csv(data_file, index=False)

# Function to add an expense
def add_expense(date, category, amount):
    df = pd.read_csv(data_file)
    df = df.append({"Date": date, "Category": category, "Amount": amount}, ignore_index=True)
    df.to_csv(data_file, index=False)

# Function to set a budget
def set_budget(category, budget_limit):
    budgets = pd.read_csv('budgets.csv') if os.path.exists('budgets.csv') else pd.DataFrame(columns=["Category", "Limit"])
    if category not in budgets['Category'].values:
        budgets = budgets.append({"Category": category, "Limit": budget_limit}, ignore_index=True)
    else:
        budgets.loc[budgets['Category'] == category, "Limit"] = budget_limit
    budgets.to_csv('budgets.csv', index=False)

# Function to generate spending reports (monthly, yearly)
def generate_report(period="monthly"):
    df = pd.read_csv(data_file)
    df['Date'] = pd.to_datetime(df['Date'])
    
    if period == "monthly":
        report = df.groupby([df['Date'].dt.to_period('M'), 'Category']).agg({'Amount': 'sum'}).reset_index()
    elif period == "yearly":
        report = df.groupby([df['Date'].dt.to_period('Y'), 'Category']).agg({'Amount': 'sum'}).reset_index()

    return report

# Function to visualize spending
def visualize_spending(period="monthly"):
    report = generate_report(period)
    if period == "monthly":
        report['Date'] = report['Date'].dt.strftime('%B %Y')
    elif period == "yearly":
        report['Date'] = report['Date'].dt.strftime('%Y')

    fig, ax = plt.subplots(figsize=(10, 6))
    for category in report['Category'].unique():
        category_data = report[report['Category'] == category]
        ax.plot(category_data['Date'], category_data['Amount'], label=category)

    ax.set_title(f"Spending Report ({period.capitalize()})")
    ax.set_xlabel('Date')
    ax.set_ylabel('Amount Spent')
    ax.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Main menu
def main():
    print("Welcome to the Budget Tracker/Expense Manager!")
    while True:
        print("\nChoose an option:")
        print("1. Add an expense")
        print("2. Set budget limit")
        print("3. Generate monthly report")
        print("4. Generate yearly report")
        print("5. Visualize monthly spending")
        print("6. Visualize yearly spending")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            date = input("Enter the date (YYYY-MM-DD): ")
            category = input("Enter the category (e.g., Groceries, Entertainment): ")
            amount = float(input("Enter the amount: "))
            add_expense(date, category, amount)
            print("Expense added successfully!")

        elif choice == '2':
            category = input("Enter the category: ")
            budget_limit = float(input("Enter the budget limit: "))
            set_budget(category, budget_limit)
            print(f"Budget for {category} set to {budget_limit}.")

        elif choice == '3':
            print("\nMonthly Report:")
            report = generate_report("monthly")
            print(report)

        elif choice == '4':
            print("\nYearly Report:")
            report = generate_report("yearly")
            print(report)

        elif choice == '5':
            print("\nVisualizing monthly spending...")
            visualize_spending("monthly")

        elif choice == '6':
            print("\nVisualizing yearly spending...")
            visualize_spending("yearly")

        elif choice == '7':
            print("Exiting the app. Goodbye!")
            break

        else:
            print("Invalid choice! Please enter a number between 1 and 7.")

if __name__ == "__main__":
    main()
