Banking App with Tkinter

A simple banking application developed with Python's Tkinter for GUI and SQLite for the database.

Download exe: [here](https://github.com/Rakap47/Banking/releases/Rakap-Banking-v0.1)

# 🔥 Features

💻User Registration: 

Allows new users to register with details such as passport code & name, date of birth, and password.
User Login: Existing users can login using their passport code and password.
Account Overview: Once logged in, users can view their debit card details, balance, sort code, and account number.
Money Transfer: Users can transfer money to other accounts using sort code and account number.
Withdraw Money: Users can specify an amount to withdraw. Upon confirmation, an 8-digit code is generated for reference.
Deposit Money: Users can deposit money by specifying an amount. They'll then receive an 8-digit code, which they can use at an ATM to complete the deposit.
Statements: Users can view random stored statements from their account.

# 🏗️ How to Set up
Clone the Repository:

```bash
git clone https://github.com/Rakap47/Banking.git

cd Banking
```

Install Dependencies:
Ensure you have Python and pip installed. Then, install the required dependencies:

```bash
pip install -r requirements.txt
```

Run the Application:

```bash
python main.py
```
# 🍔 Usage
🔑 Registration:

Launch the app.
Click on the 'Register' button.
Fill in the required details and register.

🔍 Login:

Use the passport code and password set during registration to log in.

🔢Transfer Money:

Click on the 'Transfer' button.
Provide the recipient's sort code and account number.
Specify the amount and confirm.

🔢Withdraw Money:

Click on the 'Withdraw' button.
Specify the amount you wish to withdraw.
Note down the generated 8-digit code for reference at the ATM.

🔢Deposit Money:

Click on the 'Deposit' button.
Specify the amount you wish to deposit.
Use the generated 8-digit code at the ATM to complete the deposit.

🔢View Statements:

Click on the 'Statements' button to view your account statements.
Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss what you would like to change.

# 🛡️ License
This project is licensed under the MIT License.
