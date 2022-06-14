import phonenumbers
import shelve
import re
from itertools import islice
from collections import UserDict
from datetime import datetime


class Field:
    """
    Класс родительский для всех полей - общая логика для всех полей
    """
    def __init__(self, value) -> None:
        self._value = None
        self.value = value


class Name(Field):
    pass


class Phone(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            number = phonenumbers.parse(value, "UA")
            self._value = phonenumbers.format_number(number, phonenumbers.PhoneNumberFormat.NATIONAL)
        except Exception:
            raise ValueError("Phone is not valid. Please enter again.")


class Birthday(Field):
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = datetime.strptime(value, '%Y-%m-%d').date()


class Record:
    def __init__(self, name: Name, phone=None, end_phone=None, birthday=None) -> None:
        self.name = name
        self.end_phone = end_phone
        self.phones = []
        if phone:
            self.phones.append(phone)
        self.birthday = birthday

    def add_phone(self, phone: Phone):
        for p in self.phones:
            if phone.value == p.value:
                return f'Phone {p} in record'
            else:
                self.phones.append(phone)
                return f'Phone {phone.value} add successful'

    def del_phone(self, phone: Phone):
        for p in self.phones:
            if phone.value == p.value:
                self.phones.remove(p)
                return f'Phone {phone.value} deleted successful'

    def edit_phone(self, phone: Phone, end_phone: Phone):
        for p in self.phones:
            if phone.value == p.value:
                self.phones.remove(p)
            if end_phone != p.value:
                self.phones.append(end_phone)
                return f'Phone {phone.value} edited on {end_phone.value}'

    # возвращает количество дней до следующего дня рождения контакта, если день рождения задан.

    def days_to_birthday(self):
        day_now = datetime.now().date()
        if self.birthday:
            day_to_birth = self.birthday - day_now
            day_to_birth = day_to_birth.days
            return f'Birthday:{day_to_birth}'

    def __repr__(self) -> str:
        return f'{self.name.value} : {[p.value for p in self.phones]}'


class AddressBook(UserDict):

    def add_record(self, rec):
        self.data[rec.name.value] = rec

    def iterator(self, n=2):
        start = 0
        step = n
        while True:
            yield dict(islice(self.data.items(), start, n))
            start, n = n, n + step
            if start >= len(self.data):
                break

    def search_str(self, value):
        user_list = []
        if len(value) < 3:
            raise ValueError("The search parameter must contain more than 3 characters")
        for k, v in self.data.items():
            if value in v.name.value or [phone for phone in v.phones if value in phone.value]:
                user_list.append(self.data[k])
        return user_list


if __name__ == '__main__':
    name_new = Name("Bill")
    name_new1 = Name("Ann")
    name_new2 = Name("Lili")
    name_new3 = Name("Dan")

    try:
        phone_first = Phone("+380678996777")
    except ValueError as e:
        print(e)
        phone_first = None

    try:
        phone_first1 = Phone("+380677654321")
    except ValueError as e:
        print(e)
        phone_first = None

    try:
        phone_first2 = Phone("+380678991111")
    except ValueError as e:
        print(e)
        phone_first2 = None

    try:
        phone_first3 = Phone("+380678922222")
    except ValueError as e:
        print(e)
        phone_first3 = None

    new_birthday = Birthday("2011-09-05")
    # print(new_birthday.value)

    rec = Record(name_new, phone_first)
    rec1 = Record(name_new1, phone_first1)
    # print(rec)
    rec2 = Record(name_new2, phone_first2)
    rec3 = Record(name_new3, phone_first3)

    # phone_second = Phone("+380678996765")
    # print(phone_second.value)

    try:
        phone_second = Phone("+380965035661")
    except ValueError as e:
        print(e)
        phone_second = None

    rec.add_phone(phone_second)
    # rec.del_phone(phone_first)
    # rec.edit_phone(phone_first, phone_second)

    ab = AddressBook()
    ab.add_record(rec)
    ab.add_record(rec1)
    # print(ab)

    ab.add_record(rec2)
    ab.add_record(rec3)

# -------------iterator-------------------------------------
    it = ab.iterator(2)
    for i in it:
        print(i)

# -------------'My Address book'----------------------------
    file_name = 'ad_book'
    with shelve.open(file_name) as ad:
        print('----------------------------------------------')
        ad['Bill'] = ["+380678996765", "+380965035661"]
        ad['Ann'] = ["+380677654321"]
        ad['Lili'] = ["+380678991111"]
        ad['Dan'] = ["+380678922222"]

        # Способ обновить значение -------------------------------
        # який спосіб кращий, оскільки додає не в основной словник????
        temp = ad['Ann']
        temp.append("+380678997777")
        ad['Ann'] = temp

        ad['My Address book'] = ab
    #   спробувати додати конкретно щось у цей словник !!!!!!!!

    with shelve.open(file_name) as states:
        for key in states:
            print(f'{key}: {states[key]}')
        print('----------------------------------------------')
        print(states['My Address book'])

# -------------'Search'-----------------------------------------
    try:
        s_ch = ab.search_str("777")
        print(s_ch)
    except ValueError as e:
        print(e)