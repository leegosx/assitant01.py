from collections import UserDict
from collections.abc import Iterator
from datetime import date
import csv
import time
import json

class Field:
    def __init__(self, value):
        self._value = None
        self.value = value

    @property
    def value(self):
        return self._value
    
    @value.setter
    def value(self, value):
        self._value = value

class Name(Field):
    pass
        
class Phone(Field):
    def __init__(self, value):
        super().__init__(value)
        if value.isdigit():
            self.value = value
        else:
            self.value = self._extract_digits(value)

        self.record = None

    def _extract_digits(self, value):
        digits = ''.join(filter(str.isdigit, value))
        return digits

    def add_to_record(self, record):
        self.record = record
        record.phones.append(self)

    # def __init__(self, value):
    #     super().__init__(value)
    #     if value.isdigit():
    #         self.value = value 
            
    #     self.record = None

    # def add_to_record(self, record):
    #     self.record = record
    #     record.phones.append(self)

class AddressBook(UserDict):

    def add_record(self, record):
        self.data[record.name.value] = record

    def save_to_file(self, filename):
        with open(filename, "w", newline="") as file:
            writer = csv.writer(file)
            for record in self.data.values():
                phones = [phone.value for phone in record.phones]
                writer.writerow([record.name.value, *phones]) 

    def load_to_file(self, filename):
        with open(filename, "r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                name = Name(row[0])
                phones = [Phone(phone) for phone in row[1:]]
                record = Record(name)
                for phone in phones:
                    phone.add_to_record(record)
                self.add_record(record)


    def __init__(self, phonebook=None, page_size=10):
        super().__init__()
        self.data = phonebook or {}
        self.page_size = page_size
        self.current_page = 0

    def __iter__(self):
        return self
    
    def __next__(self):
        start = self.current_page * self.page_size
        end = start + self.page_size
        if start >= len(self.data):
            raise StopIteration
        page = list(self.data.keys())[start:end]
        self.current_page += 1
        return page   

class Record:
    def __init__(self, name=None, birthday=None):
        self.name = name
        self.birthday = birthday
        self.phones = []
    def days_to_birthday(self):
        today = date.today()
        next_birthday = date(today.year, self.birthday.month, self.birthday.day)

        if next_birthday < today:
            next_birthday = date(today.year + 1, self.birthday.month, self.birthday.day)

        days_left = (next_birthday - today).days
        print(f"{self.name.value}'s birthday is {days_left} away! ")
        return days_left

# if __name__ == "__main__":
#     ab = AddressBook()
#     ab.load_to_file('контакти.csv')

#     ab.delete_contact("Lisa")
#     name = Name("Dimas")
#     phone = Phone("0990658131")

#     rec = Record(name)
#     phone.add_to_record(rec)

#     ab = AddressBook()


#     # ab.write_contacts_to_file('contactss.json')
#     # ab.load_to_file('contactss.json')
#     ab.save_to_file('контакти.csv')
#     ab.load_to_file('контакти.csv')

#     name = input("Enter contact: ")
#     ab.delete_contact(name)


#     result = ab.search_contact("81")

#     if len(result) > 0:
#         print("Searching similarities, please wait..")
#         time.sleep(2)
#         print("Successfully completed :D \n↓ ↓ INFO ↓ ↓")
#         time.sleep(1.5)
#         for record in result:
#             print(f"Contact found: {record.name.value}")
#             for phone in record.phones:
#                 print(f"Phone number: {phone.value}")
#     else:
#         print("Searching similarities, please wait..")
#         time.sleep(2)
#         print(f"No contacts found with the provided search query.")


# def write_contacts_to_file(self, filename):
    #     with open(filename, "w") as file:
    #         json_data = {
    #             "contacts": [
    #                 {
    #                     "name": record.name.value,
    #                     "phones": [phone.value for phone in record.phones]
    #                 }
    #                 for record in self.data.values()
    #             ]
    #         }
    #         json.dump(json_data, file, indent=4)

    
  
    # def read_contacts_from_file(self, filename):
    #     with open(filename, "r") as file:
    #         json_data = json.load(file)
    #         contacts = json_data.get("contacts", [])
    #         for contact in contacts:
    #             name = Name(contact["name"])
    #             phones = [Phone(phone) for phone in contact["phones"]]
    #             record = Record(name)
    #             for phone in phones:
    #                 phone.add_to_record(record)
    #             self.add_to_record(record)


      # def search_contact(self, search_query):
    #     results = []
    #     for record in self.data.values():
    #         for phone in record.phones:
    #             if search_query in phone.value:
    #                 results.append(record)
    #                 break
    #         else:
    #             continue
    #         break
    #     return results

    # def delete_contact(self, name):
    #     if name in self.data:
    #         record = self.data[name]
    #         for phone in record:
    #             phone.record = None
    #         del self.data[name]
    #         print(f"Contact with name {name} has been deleted.")
    #     else:
    #         print(f"Contact with name {name} not found.")
