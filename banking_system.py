import mysql.connector
import random
import re
from datetime import datetime


# Function to create a connection to the database
def create_connection():
    return mysql.connector.connect(
        host="localhost",      
        user="root",          
        password="mysqlshreya11@",   
        database="banking_system"
    )


# Function to generate a random 10-digit account number
def create_account_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])


# Function to validate email format using regex
def validating_email(email):
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))


# Function to validate contact number (should be 10 digits)
def validating_contact(contact_number):
    return len(contact_number) == 10 and contact_number.isdigit()


# Function to validate password (minimum 8 characters with letters and numbers)
def validating_password(password):
    return len(password) >= 8 and any(char.isdigit() for char in password) and any(char.isalpha() for char in password)


# Function to validate date of birth (should be in YYYY-MM-DD format)
def validating_dob(dob):
    try:
        datetime.strptime(dob, "%Y-%m-%d")
        return True
    except ValueError:
        return False


# Function to add a new user to the database
def add_user():
    connection = create_connection()
    cursor = connection.cursor()

    # Input details from the user
    name = input("Enter name: ")
    dob = input("Enter date of birth (YYYY-MM-DD): ")
    
    if not validating_dob(dob):
        print("Error: Date of birth must be in the format YYYY-MM-DD.")
        return
    
    city = input("Enter city: ")
    contact_number = input("Enter contact number: ")
    
    if not validating_contact(contact_number):
        print("Invalid contact number. It should be 10 digits.")
        return
    
    email = input("Enter email: ")
    
    if not validating_email(email):
        print("Invalid email address.")
        return
    
    address = input("Enter address: ")
    password = input("Enter password: ")
    
    if not validating_password(password):
        print("Password must be at least 8 characters, including letters and numbers.")
        return
    
    account_number = create_account_number()
    initial_balance = float(input("Enter initial balance (minimum 2000): "))
    
    if initial_balance < 2000:
        print("Initial balance must be at least 2000.")
        return
    
    # Insert user data into 'users' and 'login' tables
    cursor.execute("INSERT INTO users (name, account_number, dob, city, contact_number, email, address, balance) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                   (name, account_number, dob, city, contact_number, email, address, initial_balance))
    cursor.execute("SELECT LAST_INSERT_ID()")
    user_id = cursor.fetchone()[0]
    cursor.execute("INSERT INTO login (user_id, password) VALUES (%s, %s)", (user_id, password))
    
    connection.commit()
    cursor.close()
    connection.close()

    print(f"User added successfully! Account Number: {account_number}")


# Function to show all user details from the database
def show_user_details():
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()

    if not users:
        print("No users found.")
    else:
        for user in users:
            print(f"User ID: {user[0]}")
            print(f"Name: {user[1]}")
            print(f"Account Number: {user[2]}")
            print(f"DOB: {user[3]}")
            print(f"City: {user[4]}")
            print(f"Contact Number: {user[5]}")
            print(f"Email: {user[6]}")
            print(f"Address: {user[7]}")
            print(f"Balance: {user[8]}")
            print("-" * 30)

    cursor.close()
    connection.close()
    input("Press ENTER to return to the main menu +_+")
    main_menu()


# Function to handle user login
def login():
    connection = create_connection()
    cursor = connection.cursor()

    account_number = input("Enter your account number: ")
    password = input("Enter your password: ")

    cursor.execute("SELECT u.user_id, l.password FROM users u JOIN login l ON u.user_id = l.user_id WHERE u.account_number = %s", (account_number,))
    result = cursor.fetchone()

    if result and result[1] == password:
        print("Login successful!")
        user_id = result[0]
        cursor.close()
        connection.close()
        login_menu(user_id)
    else:
        print("Sorry, Invalid account number or password.")
        cursor.close()
        connection.close()


# Function to show balance of a user
def show_balance(user_id):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    balance = cursor.fetchone()[0]
    print(f"Your current account balance is: {balance}")

    cursor.close()
    connection.close()


# Function to credit an amount to the user's balance
def credit_amount(user_id, amount):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, user_id))
    cursor.execute("INSERT INTO transaction (user_id, type, amount) VALUES (%s, 'Credit', %s)", (user_id, amount))

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Amount of {amount} credited to your account.")


# Function to debit an amount from the user's balance
def debit_amount(user_id, amount):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
        cursor.execute("INSERT INTO transaction (user_id, type, amount) VALUES (%s, 'Debit', %s)", (user_id, amount))
        connection.commit()
        print(f"Amount of {amount} debited from your account.")
    else:
        print("Insufficient balance!")

    cursor.close()
    connection.close()


# Function to transfer amount between users
def transfer_amount(user_id, receiver_account_number, amount):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT balance FROM users WHERE user_id = %s", (user_id,))
    balance = cursor.fetchone()[0]

    if balance >= amount:
        cursor.execute("SELECT user_id FROM users WHERE account_number = %s", (receiver_account_number,))
        receiver_user = cursor.fetchone()

        if receiver_user:
            receiver_user_id = receiver_user[0]

            cursor.execute("UPDATE users SET balance = balance - %s WHERE user_id = %s", (amount, user_id))
            cursor.execute("UPDATE users SET balance = balance + %s WHERE user_id = %s", (amount, receiver_user_id))
            cursor.execute("INSERT INTO transaction (user_id, type, amount) VALUES (%s, 'Transfer Out', %s)", (user_id, amount))
            cursor.execute("INSERT INTO transaction (user_id, type, amount) VALUES (%s, 'Transfer In', %s)", (receiver_user_id, amount))

            connection.commit()
            print(f"Amount of {amount} transferred to account number {receiver_account_number}.")
        else:
            print("Receiver account not found.")
    else:
        print("Insufficient balance!")

    cursor.close()
    connection.close()


# Function to change password
def change_password(user_id, new_password):
    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("UPDATE login SET password = %s WHERE user_id = %s", (new_password, user_id))

    connection.commit()
    cursor.close()
    connection.close()

    print("Password changed successfully.")


# Function to update user profile information
def update_profile(user_id, name=None, city=None, contact_number=None, email=None, address=None):
    connection = create_connection()
    cursor = connection.cursor()

    if name:
        cursor.execute("UPDATE users SET name = %s WHERE user_id = %s", (name, user_id))
    if city:
        cursor.execute("UPDATE users SET city = %s WHERE user_id = %s", (city, user_id))
    if contact_number:
        cursor.execute("UPDATE users SET contact_number = %s WHERE user_id = %s", (contact_number, user_id))
    if email:
        cursor.execute("UPDATE users SET email = %s WHERE user_id = %s", (email, user_id))
    if address:
        cursor.execute("UPDATE users SET address = %s WHERE user_id = %s", (address, user_id))

    connection.commit()
    cursor.close()
    connection.close()

    print("Profile updated successfully.")


# Function to toggle account status (active/deactive)
def toggle_account_status(user_id, status):
    if status not in ['Active', 'Deactive']:
        print("Invalid status! Please enter 'Active' or 'Deactive'.")
        return

    connection = create_connection()
    cursor = connection.cursor()

    cursor.execute("UPDATE users SET status = %s WHERE user_id = %s", (status, user_id))

    connection.commit()
    cursor.close()
    connection.close()

    print(f"Account status updated to {status}.")


# Main menu to choose options
def main_menu():
    while True:
        print("WELCOME TO THE CODING BANKING SYSTEM")
        print("1. *Add User*")
        print("2. *Show User*")
        print("3. *Login*")
        print("4. *Exit*")

        choice = input("Enter your choice: ")

        if choice == '1':
            add_user()
        elif choice == '2':
            show_user_details()
        elif choice == '3':
            login()
        elif choice == '4':
            print("Exiting...")
            exit()
        else:
            print("Invalid choice, try again.")


# Login menu for after successful login
def login_menu(user_id):
    while True:
        print("\n#Login Menu:")
        print("1. Show Balance")
        print("2. Credit Amount")
        print("3. Debit Amount")
        print("4. Transfer Amount")
        print("5. Change Password")
        print("6. Update Profile")
        print("7. Toggle Account Status")
        print("8. Logout")

        choice = input("Enter your choice: ")

        if choice == '1':
            show_balance(user_id)
        elif choice == '2':
            amount = float(input("Enter amount to credit: "))
            credit_amount(user_id, amount)
        elif choice == '3':
            amount = float(input("Enter amount to debit: "))
            debit_amount(user_id, amount)
        elif choice == '4':
            receiver_account = input("Enter receiver account number: ")
            amount = float(input("Enter amount to transfer: "))
            transfer_amount(user_id, receiver_account, amount)
        elif choice == '5':
            new_password = input("Enter new password: ")
            change_password(user_id, new_password)
        elif choice == '6':
            update_profile_menu(user_id)
        elif choice == '7':
            status = input("Enter status (Active/Deactive): ")
            toggle_account_status(user_id, status)
        elif choice == '8':
            print("Logging out...")
            break
        else:
            print("Invalid choice, try again.")


# Function to update profile from the login menu
def update_profile_menu(user_id):
    print("Update Profile:")
    name = input("Enter new name (leave blank to keep unchanged): ")
    city = input("Enter new city (leave blank to keep unchanged): ")
    contact_number = input("Enter new contact number (leave blank to keep unchanged): ")
    email = input("Enter new email (leave blank to keep unchanged): ")
    address = input("Enter new address (leave blank to keep unchanged): ")

    update_profile(user_id, name, city, contact_number, email, address)

# Starting the program by calling the main menu function
if __name__ == "__main__":
    main_menu()
