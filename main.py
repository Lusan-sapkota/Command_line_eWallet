import json

# File to store user data
USERS_FILE = "user_data.json"


# Function to load user data from the file
def load_user_data():
    try:
        with open(USERS_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Function to save user data to the file
def save_user_data(users_data):
    with open(USERS_FILE, "w") as file:
        json.dump(users_data, file, indent=4)


# Function to get valid input from the user
def get_valid_input(prompt, valid_options):
    while True:
        user_input = input(prompt).lower()
        if user_input in valid_options:
            return user_input
        print(f"Invalid input. Please choose from {', '.join(valid_options)}.")


# Function to handle user registration
def register_user():
    print("Registration")
    name = input("Enter your name: ").upper()
    password = input("Create a password: ")
    while True:
        phone_number = input("Enter your phone number: ")
        if len(phone_number) != 10:
            print("please check your phone number again.")
            continue
        elif not phone_number.isdigit():
            print("please check your phone number again.")
            continue
        else:
            break
    while True:
        user_pin = input("Enter a 4-digit PIN: ")
        if len(user_pin) != 4:
            print("please check your pin again.")
            continue
        elif not user_pin.isdigit():
            print("please check your pin again.")
            continue
        else:
            break
    # Create a new user dictionary
    user = {
        "name": name,
        "password": password,
        "pin": user_pin,
        "balance": 0.0
    }

    return phone_number, user


# Function to handle loading money into the user's account
def load_money(user):
    while True:
        try:
            amount = float(input("Specify the amount you want to load: "))
            input_pin = input("Enter your pin: ")
            if input_pin == user['pin']:
                user['balance'] += amount
                print(f'Loaded balance: Nrs.{user["balance"]:.2f}')
                return user['balance']
            else:
                print('Invalid pin')
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


# Function to handle withdrawing money from the user's account
def withdraw_money(user):
    while True:
        try:
            amount = float(input("Specify the amount you want to withdraw: "))
            input_pin = input("Enter your pin: ")
            if input_pin == user['pin']:
                if amount <= user['balance']:
                    user['balance'] -= amount
                    print(f"Successfully withdrawn: Nrs.{amount:.2f}")
                    return user['balance']
                else:
                    print(f"You only have Nrs.{user['balance']:.2f} in your account.")
            else:
                print('Invalid pin')
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


# Function to handle transferring money between users
def transfer_money(sender, receiver):
    while True:
        try:
            amount = float(input("Specify the amount you want to transfer: "))
            input_pin = input("Enter your pin: ")
            if input_pin == sender['pin']:
                if amount <= sender['balance']:
                    sender['balance'] -= amount
                    receiver['balance'] += amount
                    print(f"Successfully transferred to {receiver['name']}: Nrs.{amount:.2f}")
                    return sender['balance']
                else:
                    print(f"You only have Nrs.{sender['balance']:.2f} in your account. Please load more.")
                    return load_money(sender)
            else:
                print('Invalid pin')
        except ValueError:
            print("Invalid input. Please enter a numeric value.")


# Function to check if the provided number and PIN are valid
def is_valid_user(phone_number, password, users_data):
    user = users_data.get(phone_number)
    return user and user['password'] == password


# Function to handle the exit confirmation
def exit_program():
    confirm_exit = get_valid_input("Are you sure you want to exit (y/n): ", ['y', 'n'])
    return confirm_exit == 'y'


# Main function to run the eWallet program
def main():
    # Load existing user data or initialize an empty dictionary
    users_data = load_user_data()
    print("eWallet ---> Proudly made by LUSAN SAPKOTA")

    while True:
        # Get user credentials
        phone_number = input("Enter your phone number: ")
        if len(phone_number) != 10:
            print("please check your phone number again.")
            continue
        elif not phone_number.isdigit():
            print("please check your phone number again.")
            continue
        password = input("Enter your Password: ")

        # Check if the user is valid
        if is_valid_user(phone_number, password, users_data):
            user = users_data[phone_number]
            print(f'Welcome {user["name"]}!')
        elif phone_number in users_data:
            print("Incorrect password. Please try again.")
            continue
        else:
            register_option = get_valid_input("User not found. Do you want to register (y/n): ", ['y', 'n'])
            if register_option == 'y':
                phone_number, user = register_user()
                users_data[phone_number] = user
                print("Registration successful!")
            else:
                continue

        while True:
            # Display user's available balance
            print(f'Available balance: Nrs.{user["balance"]:.2f}')

            # Get user's choice for the operation to perform
            user_options = int(input("Choose an option:\n1. Load money\n2. Withdraw money\n3. Transfer money\n4. "
                                     "Login to another account\n5. Exit\n--------> "))

            try:
                # Execute the chosen operation
                if user_options == 1:
                    load_money_option = get_valid_input("Do you want to load money (y/n): ", ['y', 'n'])
                    if load_money_option == 'y':
                        user['balance'] = load_money(user)
                elif user_options == 2:
                    withdraw_option = get_valid_input("Do you want to withdraw money (y/n): ", ['y', 'n'])
                    if withdraw_option == 'y':
                        user['balance'] = withdraw_money(user)
                elif user_options == 3:
                    transfer_option = get_valid_input("Do you want to transfer money (y/n): ", ['y', 'n'])
                    if transfer_option == 'y':
                        receiver_phone_number = input("Receiver's phone number: ")
                        receiver = users_data.get(receiver_phone_number)
                        if receiver:
                            user['balance'] = transfer_money(user, receiver)
                        else:
                            print("Invalid receiver number.")
                elif user_options == 4:
                    logging_option = get_valid_input("Do you want to logout (y/n): ", ['y', 'n'])
                    if logging_option == 'y':
                        print("Re-login........")
                        break
                elif user_options == 5:
                    program_exit_option = get_valid_input("Do you want to exit the program (y/n): ", ['y', 'n'])
                    if program_exit_option == 'y' and exit_program():
                        print("Exiting the program!")

                        # Save the updated user data before exiting
                        save_user_data(users_data)
                        return
                else:
                    raise ValueError("Please input a valid option.")
            except ValueError as ve:
                print(ve)


# Entry point of the program
if __name__ == "__main__":
    main()
