import sqlite3
import datetime
from datetime import date
from helper import print_table


conn = sqlite3.connect('expenses.db')
cur = conn.cursor()

print("Database connection successful!")


cur.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        category TEXT NOT NULL,
        description TEXT,
        amount REAL NOT NULL
    )
''')
conn.commit()


def add_expense():
    dt_input = input("Date (YYYY-MM-DD) [Leave blank for today]: ").strip()

    if dt_input == "":
        dt = datetime.date.today().isoformat()  # Default to today's date
    else:
        try:
            # Validate date format
            datetime.datetime.strptime(dt_input, "%Y-%m-%d")
            dt = dt_input
        except ValueError:
            print("Invalid date format!")
            return

    
    cat = input("Category: ")
    desc = input("Short description: ")

    try:
        amt = float(input("Amount (in $): "))
        if amt <= 0:
            print("Amount must be more than zero.")
            return
    except ValueError:
        print("Invalid amount.")
        return

    cur.execute("INSERT INTO expenses (date, category, description, amount) VALUES (?, ?, ?, ?)",
                (dt, cat, desc, amt))
    conn.commit()
    print("Expense added successfully!")

# Function to view all expenses
def view_expenses():
    rows = cur.execute("SELECT * FROM expenses;").fetchall()
    print_table(rows)

# Function to show the total expenses
def show_total_expenses():
    cur.execute("SELECT IFNULL(SUM(amount), 0) FROM expenses")
    (total, ) = cur.fetchone()
    print(f"Total spent: ${float(total):.2f}")

# Function to show expenses for a selected month
def show_selected_month_expenses():
    selected = input("Enter month (YYYY-MM): ").strip()
    cur.execute("SELECT * FROM expenses WHERE date LIKE ?", (selected + '%',))
    rows = cur.fetchall()
    if rows:
        print_table(rows)
    else:
        print("No expenses found for that month.")


def reset_expenses():
    confirm = input("Are you sure you want to delete all expenses? (y/n): ").strip().lower()
    if confirm in ("y", "yes"):
        cur.execute("DELETE FROM expenses")
        conn.commit()
        print("All expenses wiped clean.")
    else:
        print("Reset canceled.")
    

while True:
    print("Menu:")
    print("1. Add an expense")
    print("2. View all expenses")
    print("3. Show total expenses")
    print("4. Show selected month's expenses")
    print("5. Reset all expenses")
    print("6. Exit")

    try:
        choice = int(input("Choose an option (1–6): "))
    except ValueError:
        print("Invalid input. Please enter a number from 1 to 6.")
        continue

   
    if choice == 1:
        add_expense()
    elif choice == 2:
        view_expenses()
    elif choice == 3:
        show_total_expenses()
    elif choice == 4:
        show_selected_month_expenses()
    elif choice == 5:
        reset_expenses()
    elif choice == 6:
        break
    else:
        print("Invalid option. Try again.")


print("Goodbye! Thanks for using the Expense Tracker.")
conn.close()
