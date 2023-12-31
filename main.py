import time
from address_book import *
from contact import *
from main_extended import *

def input_error(func):
    def wrapper(name, phone):
        try:
            result = func(name, phone)
            return result
        except KeyError:
            print("The contact is missing. ")
        except IndexError:
            print("Enter the name and number separated by a space. ")
        except ValueError:
            print("ValueError. Please try again. ")
    return wrapper


def hello():
    return "How i can help you?"

@input_error
def add_contact(name, phone):
    ab = AddressBook()
    #csv and json write
    ab.load_to_file('контакти.csv')
    # ab.write_contacts_to_file('contactss.json')
    record = Record(Name(name))
    record.phones.append(Phone(phone))
    ab.add_record(record)
    #json and csv read
    # ab.read_contacts_from_file('contactss.json')
    ab.save_to_file('контакти.csv')
    return f"Contact {name} with phone number {phone} has been added."

@input_error
def change_contact(name, phone):
    ab = AddressBook()
    ab.load_to_file('контакти.csv')
    # ab.write_contacts_to_file('contactss.json')
    if name in ab.data:
        record = ab.data[name]
        record.phones = [Phone(phone)]
        ab.save_to_file('контакти.csv')
        # ab.write_contacts_to_file('contactss.json')
        return f"Contact {name}'s phone number has been update to {phone}. "
    else:
        return f"Contact {name}'s does not exist"

def get_number_contact(name):
    ab = AddressBook()
    ab.load_to_file('контакти.csv')
    # ab.write_contacts_to_file('contactss.json')
    if name in ab.data:
        return f"The phone number of {name} is {ab.data[name].phones[0].value}. "
    else:
        return f"Contact {name} does not exist. "
    
def show_all_contact():
    ab = AddressBook()
    ab.load_to_file('контакти.csv')
    # ab.write_contacts_to_file('contactss.json')
    contacts_all = ""
    for name, record in ab.data.items():
        phones = [phone.value for phone in record.phones]
        contacts_all += f"| {name}: {', '.join(phones)} |\n"
    return contacts_all

def delete_contact(name):
    ab = AddressBook()
    ab.load_to_file('контакти.csv')
    if name in ab.data:
        del ab.data[name]
        ab.save_to_file('контакти.csv')
        return f"Contact with name {name} has been deleted."
    else:
        return f"Contact with name {name} not found."


def exit_program():
    ab = AddressBook()
    # ab.write_contacts_to_file('contactss.json')
    # ab.read_contacts_from_file('contacts.json')
    ab.load_to_file('контакти.csv')
    ab.save_to_file('контакти.csv')
    return "Goodbye!"


def main():
    print("Welcome to the Assistant bot! ")
    while True:
        user_input = input("Enter a command: ")
        if user_input.lower() in ["goodbye", "close", "exit"]:
            print(exit_program())
            break
        elif user_input.lower() == "hello":
            print(hello())
        elif user_input.lower() == "delete contact":
            name = input("Enter a contact to delete: ")
            print(delete_contact(name))
        elif user_input.lower() == "show all contacts":
             print(show_all_contact())
        elif user_input.lower() == "add contact":
            name = input("Enter the name: ")
            phone = input("Enter the phone number: ")
            print(add_contact(name, phone))
        elif user_input.lower() == "change contact":
            contact_info = input("Enter the name and new phone number separated by a space: ")
            name, phone = contact_info.split()
            print(change_contact(name, phone))
        elif user_input.lower() == "get number contact":
            name = input("Enter the name: ")
            print(get_number_contact(name))
        elif user_input.lower() == "search contact":
            ab = AddressBook()
            ab.load_to_file('контакти.csv')
            search_query = input("Enter the search query: ")
            result = ab.search_contact(search_query)
            if len(result) > 0:
                print("Searching similarities, please wait..")
                time.sleep(2)
                print("Succsessfully completed :D \n ↓ ↓ INFO ↓ ↓")
                time.sleep(1.5)
                for record in result:
                    print(f"Contact found: {record.name.value}")
                    for phone in record.phones:
                        print(f"Phone number: {phone.value}")
            else:
                print("Searching similarities, please wait..")
                time.sleep(2)
                print(f"No contacts found with the provided search query. ")
        else:
            print("Invalid command. ")


if __name__ == "__main__":
    main()
