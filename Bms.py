import mysql.connector
from prettytable import PrettyTable
import random

mydatabase = mysql.connector.connect(
    host="localhost",

    user="root",
    password="micky11",
    database="banking_details"
)

mycursor = mydatabase.cursor()

mycursor.execute("CREATE TABLE IF NOT EXISTS signup (username VARCHAR(30) PRIMARY KEY, password VARCHAR(30))")

mycursor.execute("CREATE TABLE IF NOT EXISTS acc (acc_no INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(30), address VARCHAR(100), contact_no VARCHAR(20), total_balance INT)")

mycursor.execute("CREATE TABLE IF NOT EXISTS transactions (transaction_id INT AUTO_INCREMENT PRIMARY KEY, acc_no INT, transaction_type VARCHAR(10), amount INT, transaction_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

def generate_otp():
    return str(random.randint(1000, 9999))

def generate_account_number():
    return random.randint(100000, 999999)

def create_account(name, address, contact_no, total_balance):
    acc_no = generate_account_number()
    sql = "INSERT INTO acc (acc_no, name, address, contact_no, total_balance) VALUES (%s, %s, %s, %s, %s)"
    values = (acc_no, name, address, contact_no, total_balance)
    mycursor.execute(sql, values)
    mydatabase.commit()
    return acc_no

def signup():
    username = input("Enter username: ")
    password = input("Enter password: ")
    mycursor.execute("SELECT username FROM signup WHERE username = %s", (username,))
    result = mycursor.fetchone()
    if result:
        print("Username already exists. Please choose a different username.")
        signup()
    else:
        sql = "INSERT INTO signup (username, password) VALUES (%s, %s)"
        values = (username, password)
        mycursor.execute(sql, values)
        mydatabase.commit()
        print("\t\t\t****************++++SIGNUP SUCCESSFULLY++++++******")
        print("Now please login to continue")
        login()

def login():
    username = input("Enter username: ")
    password = input("Enter password: ")
    mycursor.execute("SELECT username, password FROM signup WHERE username = %s", (username,))
    result = mycursor.fetchone()
    if result is None or result[1] != password:
        print("WRONG USERNAME OR PASSWORD !!!!!!")
        while True:
            choice = int(input("Press 1 to Try Again\nPress 2 to exit: "))
            if choice == 1:
                login()
            elif choice == 2:
                exit()
            else:
                print("Invalid choice. Please enter 1 or 2.")
    else:
        print("\t\t\t*********************+++++++LOGIN SUCCESSFULLY+++++*****")
        while True:
            print('1. Open a new account')
            print('2. Deposit amount')
            print('3. Withdraw amount')
            print('4. Balance enquiry')
            print('5. Customer details')
            print('6. Update information')
            print('7. Close account')
            print('8. Show data/information')
            print('Press any other key to EXIT')
            choice = input('Enter your choice: ')
            if choice == '1':
                openacc()
            elif choice == '2':
                dep()
            elif choice == '3':
                withdraw()
            elif choice == '4':
                bal_enq()
            elif choice == '5':
                cust_det()
            elif choice == '6':
                update()
            elif choice == '7':
                close()
            elif choice == '8':
                show()
            else:
                print('\t\t\t\tTHANK YOU ')
                print('\t\t\t\tHAVE A GOOD DAY ')
                exit()

def openacc():
    name = input('Enter full name of the owner: ')
    address = input('Enter permanent address of the owner: ')
    contact_no = input('Enter contact number of the owner: ')
    generated_otp = generate_otp()
    print(f'OTP sent to {contact_no}: {generated_otp}')
    entered_otp = input('Enter the OTP received: ')
    if entered_otp != generated_otp:
        print('Invalid OTP. Account not opened.')
        return

    while True:
        try:
            total_balance = int(input("Enter the initial balance: "))
            if total_balance < 0:
                print("Invalid amount. Balance cannot be negative.")
            else:
                break
        except ValueError:
            print("Invalid input. Please enter a valid integer value for the initial balance.")

    acc_no = create_account(name, address, contact_no, total_balance)
    print("\n\t\t\t__**** Account created successfully ****__")
    print(f'Your account number is: {acc_no}')
    print('______________________________________')

def dep():
    acc_no = int(input('Enter your account number: '))
    amount = int(input('Enter the amount to deposit: '))
    if amount < 0:
        print("Invalid amount. Deposit amount cannot be negative.")
        return
    mycursor.execute("SELECT total_balance FROM acc WHERE acc_no = %s", (acc_no,))
    result = mycursor.fetchone()
    if not result:
        print("Account not found. Please enter a valid account number.")
    else:
        current_balance = result[0]
        new_balance = current_balance + amount
        data = (acc_no, "Deposit", amount)
        sql = 'INSERT INTO transactions (acc_no, transaction_type, amount) VALUES (%s, %s, %s)'
        mycursor.execute(sql, data)
        mycursor.execute("UPDATE acc SET total_balance = %s WHERE acc_no = %s", (new_balance, acc_no))
        mydatabase.commit()
        print(f'Deposit of {amount} successful. New balance: {new_balance}')

def withdraw():
    acc_no = int(input('Enter your account number: '))
    amount = int(input('Enter the amount to withdraw: '))
    if amount < 0:
        print("Invalid amount. Withdrawal amount cannot be negative.")
        return

    mycursor.execute("SELECT total_balance FROM acc WHERE acc_no = %s", (acc_no,))
    result = mycursor.fetchone()
    if not result:
        print("Account not found. Please enter a valid account number.")
    else:
        current_balance = result[0]
        if current_balance < amount:
            print("Insufficient balance.")
        else:
            new_balance = current_balance - amount
            data = (acc_no, "Withdraw", amount)
            sql = 'INSERT INTO transactions (acc_no, transaction_type, amount) VALUES (%s, %s, %s)'
            mycursor.execute(sql, data)
            mycursor.execute("UPDATE acc SET total_balance = %s WHERE acc_no = %s", (new_balance, acc_no))
            mydatabase.commit()
            print(f'Withdrawal of {amount} successful. New balance: {new_balance}')

def bal_enq():
    acc_no = int(input('Enter your account number: '))
    mycursor.execute("SELECT total_balance FROM acc WHERE acc_no = %s", (acc_no,))
    result = mycursor.fetchone()
    if not result:
        print("Account not found. Please enter a valid account number.")
    else:
        print(f'Balance for account {acc_no}: {result[0]}')

def cust_det():
    acc_no = int(input('Enter account number: '))
    mycursor.execute("SELECT * FROM acc WHERE acc_no = %s", (acc_no,))
    result = mycursor.fetchone()
    if not result:
        print("Account not found. Please enter a valid account number.")
    else:
        t = PrettyTable(['Account No', 'Name', 'Address', 'Contact No', 'Total Balance'])
        t.add_row(result)
        print(t)

def update():
    acc_no = int(input('Enter account number: '))
    new_contact = input('Enter new contact number: ')
    mycursor.execute("UPDATE acc SET contact_no = %s WHERE acc_no = %s", (new_contact, acc_no))
    mydatabase.commit()
    print('Contact number updated successfully.')

def close():
    acc_no = int(input('Enter account number: '))
    mycursor.execute("DELETE FROM acc WHERE acc_no = %s", (acc_no,))
    mycursor.execute("DELETE FROM transactions WHERE acc_no = %s", (acc_no,))
    mydatabase.commit()
    print('Account closed successfully.')

def show():
    mycursor.execute("SELECT * FROM acc")
    result = mycursor.fetchall()
    if not result:
        print("No accounts found.")
    else:
        t = PrettyTable(['Account No', 'Name', 'Address', 'Contact No', 'Total Balance'])
        for row in result:
            t.add_row(row)
        print(t)


print("\t\t\t_______>>>>>>>  SECURE BANK - BANKING MANAGEMENT SYSTEM   <<<<______")
print("\t1: SIGNUP\n\t2: LOGIN")
ch = input("\n\tSIGNUP / LOGIN (1,2): ")

if ch == '1':
    signup()
elif ch == '2':
    login()
else:
    print("Wrong Entry")
