from collections import UserDict
from collections.abc import Iterator
from datetime import date

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
            print("The number should contain only numbers, without other symbol or signs! ")
    
        self.record = None

    def add_to_record(self, record):
        self.record = record
        record.phones.append(self)

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

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
        print(f"{self.name.value}'s birthday is {days_left} days away! ")
        return days_left
