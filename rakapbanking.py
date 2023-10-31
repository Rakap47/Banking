import tkinter as tk
from tkinter import simpledialog, messagebox
import sqlite3
import random

# Database Setup
def setup_db():
    conn = sqlite3.connect('banking.db')
    c = conn.cursor()

    # Create user table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (passport_code TEXT PRIMARY KEY, name TEXT, dob TEXT, password TEXT, 
                 balance REAL, sort_code TEXT, account_number TEXT, card_number TEXT)''')

    # Create statements table
    c.execute('''CREATE TABLE IF NOT EXISTS statements
                 (account_number TEXT, statement TEXT)''')

    conn.commit()
    conn.close()

setup_db()

# Registration
def register():
    window = tk.Toplevel()
    window.title("Registration")
    window.geometry("320x420")

    passport_label = tk.Label(window, text="Passport Code")
    passport_label.pack()
    passport_entry = tk.Entry(window)
    passport_entry.pack()

    name_label = tk.Label(window, text="Name")
    name_label.pack()
    name_entry = tk.Entry(window)
    name_entry.pack()

    dob_label = tk.Label(window, text="Date of Birth")
    dob_label.pack()
    dob_entry = tk.Entry(window)
    dob_entry.pack()

    password_label = tk.Label(window, text="Password")
    password_label.pack()
    password_entry = tk.Entry(window, show="*")
    password_entry.pack()

    repeat_password_label = tk.Label(window, text="Repeat Password")
    repeat_password_label.pack()
    repeat_password_entry = tk.Entry(window, show="*")
    repeat_password_entry.pack()

    def submit():
        passport_code = passport_entry.get()
        name = name_entry.get()
        dob = dob_entry.get()
        password = password_entry.get()
        repeat_password = repeat_password_entry.get()

        if password != repeat_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        sort_code = f"{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(10, 99)}"
        account_number = str(random.randint(10000000, 99999999))
        card_number = str(random.randint(1000000000000000, 9999999999999999))

        try:
            conn = sqlite3.connect('banking.db')
            c = conn.cursor()
            c.execute("INSERT INTO users VALUES (?, ?, ?, ?, 2000, ?, ?, ?)", 
                      (passport_code, name, dob, password, sort_code, account_number, card_number))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Registration successful!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Passport Code already registered!")

    submit_button = tk.Button(window, text="Submit", command=submit)
    submit_button.pack(pady=20)

# Login
def login():
    window = tk.Toplevel()
    window.title("Login")
    window.geometry("320x420")

    passport_label = tk.Label(window, text="Passport Code")
    passport_label.pack(pady=10)
    passport_entry = tk.Entry(window)
    passport_entry.pack(pady=10)

    password_label = tk.Label(window, text="Password")
    password_label.pack(pady=10)
    password_entry = tk.Entry(window, show="*")
    password_entry.pack(pady=10)

    def authenticate():
        passport_code = passport_entry.get()
        password = password_entry.get()

        conn = sqlite3.connect('banking.db')
        c = conn.cursor()
        user = c.execute("SELECT * FROM users WHERE passport_code=? AND password=?", 
                         (passport_code, password)).fetchone()
        conn.close()

        if user:
            main_dashboard(user)
        else:
            messagebox.showerror("Error", "Incorrect login details")

    login_button = tk.Button(window, text="Login", command=authenticate)
    login_button.pack(pady=20)

# Main Dashboard
def main_dashboard(user):
    window = tk.Toplevel()
    window.title("Dashboard")
    window.geometry("520x720")

    card_label = tk.Label(window, text=f"Card Number: {user[7]}\nName: {user[1]}\nBalance: ${user[4]}\nSort Code: {user[5]}\nAccount Number: {user[6]}")
    card_label.pack(pady=20)

    transfer_button = tk.Button(window, text="Transfer", command=lambda: transfer(user))
    transfer_button.pack(pady=10)

    withdraw_button = tk.Button(window, text="Withdraw", command=lambda: withdraw(user))
    withdraw_button.pack(pady=10)

    deposit_button = tk.Button(window, text="Deposit", command=deposit)
    deposit_button.pack(pady=10)

    statements_button = tk.Button(window, text="Statements", command=lambda: statements(user))
    statements_button.pack(pady=10)

# Transfer function
def transfer(user):
    window = tk.Toplevel()
    window.title("Transfer")
    window.geometry("320x420")

    to_sort_code_label = tk.Label(window, text="To Sort Code")
    to_sort_code_label.pack(pady=10)
    to_sort_code_entry = tk.Entry(window)
    to_sort_code_entry.pack(pady=10)

    to_account_number_label = tk.Label(window, text="To Account Number")
    to_account_number_label.pack(pady=10)
    to_account_number_entry = tk.Entry(window)
    to_account_number_entry.pack(pady=10)

    amount_label = tk.Label(window, text="Amount")
    amount_label.pack(pady=10)
    amount_entry = tk.Entry(window)
    amount_entry.pack(pady=10)

    def do_transfer():
        to_sort_code = to_sort_code_entry.get()
        to_account_number = to_account_number_entry.get()
        amount = float(amount_entry.get())

        conn = sqlite3.connect('banking.db')
        c = conn.cursor()

        receiver = c.execute("SELECT * FROM users WHERE sort_code=? AND account_number=?", 
                             (to_sort_code, to_account_number)).fetchone()

        if not receiver:
            messagebox.showerror("Error", "Receiver account not found!")
            return

        if user[4] < amount:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        # Deduct amount from sender
        c.execute("UPDATE users SET balance = balance - ? WHERE account_number = ?", (amount, user[6]))

        # Add amount to receiver
        c.execute("UPDATE users SET balance = balance + ? WHERE account_number = ?", (amount, receiver[6]))

        # Commit the transaction
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Transfer successful!")

    transfer_button = tk.Button(window, text="Transfer", command=do_transfer)
    transfer_button.pack(pady=20)

# Withdraw function
def withdraw(user):
    window = tk.Toplevel()
    window.title("Withdraw")
    window.geometry("320x420")

    amount_label = tk.Label(window, text="Amount")
    amount_label.pack(pady=10)
    amount_entry = tk.Entry(window)
    amount_entry.pack(pady=10)

    def do_withdraw():
        amount = float(amount_entry.get())
        if user[4] < amount:
            messagebox.showerror("Error", "Insufficient balance!")
            return

        code = random.randint(10000000, 99999999)
        messagebox.showinfo("Withdraw Code", f"Your withdrawal code is: {code}\nAmount: ${amount}")

    withdraw_button = tk.Button(window, text="Withdraw", command=do_withdraw)
    withdraw_button.pack(pady=20)

# Deposit function
def deposit():
    window = tk.Toplevel()
    window.title("Deposit")
    window.geometry("320x420")

    amount_label = tk.Label(window, text="Amount")
    amount_label.pack(pady=10)
    amount_entry = tk.Entry(window)
    amount_entry.pack(pady=10)

    def do_deposit():
        amount = float(amount_entry.get())
        code = random.randint(10000000, 99999999)
        messagebox.showinfo("Deposit Code", f"Your deposit code is: {code}\nAmount: ${amount}\nPlease visit the nearest Rakap ATM to deposit using this code.")

    deposit_button = tk.Button(window, text="Deposit", command=do_deposit)
    deposit_button.pack(pady=20)

# Show Statements function
def statements(user):
    window = tk.Toplevel()
    window.title("Statements")
    window.geometry("1080x1920")

    conn = sqlite3.connect('banking.db')
    c = conn.cursor()

    statement_list = c.execute("SELECT statement FROM statements WHERE account_number=?", 
                               (user[6],)).fetchall()

    for stmt in statement_list:
        stmt_label = tk.Label(window, text=stmt[0])
        stmt_label.pack()

    conn.close()

# Main App Window
root = tk.Tk()
root.title("Rakap Banking")
root.geometry("1080x720")

login_button = tk.Button(root, text="Login", command=login, width=40, height=2)
login_button.pack(pady=20)

register_button = tk.Button(root, text="Register", command=register, width=40, height=2)
register_button.pack(pady=20)

root.mainloop()
