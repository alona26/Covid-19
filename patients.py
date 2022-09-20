import csv
from csv import writer
import re


class InputError(Exception):
    pass


class OurPatient(object):

    def __init__(self, id, name, bitrhYear, phone, email):
        # try:
        if re.fullmatch('[0-9]{9}', id):
            with open('patient.csv', 'r', newline='') as fh:
                reader = csv.reader(fh, delimiter=',')
                for line in reader:  # Iterates through the rows of your csv
                    if str(id) == str(line[0]):
                        raise InputError("patient id already exit")

            self.id = id
        else:
            raise InputError("ID is not numbers or is not 9 in length.")
        # except ValueError:
        #     print(id + " is not an ID!")
        if re.fullmatch('[a-zA-Z]+', name):
            self.name = name
        else:
            raise InputError("Name must be only letters and at least one letter.")
        if re.fullmatch('[0-9]{4}', bitrhYear):
            self.birthYear = bitrhYear
        else:
            raise InputError("Birth year only 4 numbers.")
        if re.fullmatch('[0-9]{2,3}-[0-9]{7}', phone):
            self.phone = phone
        else:
            raise InputError("Wrong phone number!!")
        if re.fullmatch('([a-zA-Z]|[0-9])+@(gmail|walla)\.com', email):
            self.email = email
        else:
            raise InputError("Wrong Email!!")

    def add_patient(self):
        with open('patient.csv', 'a', newline='') as fh:
            writer_object = writer(fh)
            x = [self.id, self.name, self.birthYear, self.phone, self.email]
            writer_object.writerow(x)
            # Close the file object
            fh.close()

    @staticmethod
    def add_patient_from_file(file):
        # Add patient from file
        with open(file, 'r', newline='') as fh:
            original = fh.read()
            with open('patient.csv', 'a', newline='') as wf:
                wf.write(original)
                wf.write("\n")

