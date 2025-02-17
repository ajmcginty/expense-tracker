import tkinter as tk
from tkinter import ttk, messagebox, Button
import datetime
import csv
import os

FILE_NAME = "expenses.csv"

# Create main application window
root = tk.Tk()
root.title("Expense Tracker")
root.geometry("800x550")

# Function to add an expense
def add_expense():
    if entry_date.get().lower() == "today":
        date = datetime.date.today()
    else:
        date = entry_date.get()
    category = entry_category.get()
    description = entry_description.get()
    amount = entry_amount.get()

    if not date or not category or not description or not amount:
        messagebox.showerror("Error", "All fields are required!")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showerror("Error", "Amount must be a number!")
        return

    with open(FILE_NAME, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date, category, description, amount])

    messagebox.showinfo("Success", "Expense added successfully!")
    clear_entries()
    load_expenses()

# Function to delete an expense
def delete():
    selected_item = expense_table.selection()[0] ## get selected item
    expense_table.delete(selected_item)

    """Update CSV file with Treeview data."""
    with open(FILE_NAME, "w", newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for item in expense_table.get_children():
            writer.writerow(expense_table.item(item)["values"])

# Function to clear input fields
def clear_entries():
    entry_date.delete(0, tk.END)
    entry_category.delete(0, tk.END)
    entry_description.delete(0, tk.END)
    entry_amount.delete(0, tk.END)

# Function to load expenses into the table
def load_expenses():
    for row in expense_table.get_children():
        expense_table.delete(row)
    
    if not os.path.exists(FILE_NAME):
        return

    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            expense_table.insert("", tk.END, values=row)

# Function to view summary
def view_summary():
    total = 0
    categories = {}

    if not os.path.exists(FILE_NAME):
        messagebox.showinfo("Summary", "No expenses found!")
        return

    with open(FILE_NAME, mode="r") as file:
        reader = csv.reader(file)
        for row in reader:
            amount = float(row[3])
            total += amount
            categories[row[1]] = categories.get(row[1], 0) + amount

    summary_text = f"Total Expenses: ${total:.2f}\n\n"
    summary_text += "Expenses by Category:\n"
    for category, amount in categories.items():
        summary_text += f"{category}: ${amount:.2f}\n"

    messagebox.showinfo("Expense Summary", summary_text)

# UI Layout
tk.Label(root, text="Date (Today or YYYY-MM-DD):").pack()
entry_date = tk.Entry(root)
entry_date.pack()

tk.Label(root, text="Category:").pack()
entry_category = tk.Entry(root)
entry_category.pack()

tk.Label(root, text="Description:").pack()
entry_description = tk.Entry(root)
entry_description.pack()

tk.Label(root, text="Amount ($):").pack()
entry_amount = tk.Entry(root)
entry_amount.pack()

tk.Button(root, text="Add Expense", command=add_expense).pack(pady=5)
tk.Button(root, text="View Summary", command=view_summary).pack()

# Table to display expenses
expense_table = ttk.Treeview(root, columns=("Date", "Category", "Description", "Amount"), show="headings")
expense_table.heading("Date", text="Date")
expense_table.heading("Category", text="Category")
expense_table.heading("Description", text="Description")
expense_table.heading("Amount", text="Amount ($)")
expense_table.pack(pady=10)

# Button for deleting expenses
button_del = Button(root, text="Delete Selected Expense", command=delete)
button_del.pack()

# Load existing expenses
load_expenses()

# Run the application
root.mainloop()
