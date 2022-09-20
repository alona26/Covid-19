import csv
from csv import writer
from datetime import date
from datetime import datetime
from patients import InputError
import re


class PcrTest(object):

    def __init__(self, patient_id,pcr_id, result):

        flag = 0
        with open('patient.csv', 'r', newline='') as fh:
            reader = csv.reader(fh, delimiter=',')
            for line in reader:  # Iterates through the rows of your csv
                if str(patient_id) == str(line[0]):  # If the string you want to search is in the row
                    flag = 1
                    self.patient_id = patient_id
                    break
            if flag == 0:
                raise InputError("patient id wrong")
        fh.close()
        with open('pcr_tests.csv', 'r', newline='') as f_pcr:
            reader = csv.reader(f_pcr, delimiter=',')
            for line in reader:  # Iterates through the rows of your csv
                if str(pcr_id) == str(line[1]):
                    raise InputError("PCR test id already exit")
        f_pcr.close()
        self.pcr_id = pcr_id
        if re.fullmatch('True|False', result):
            self.result = result
        else:
            raise InputError("Wrong input")

        self.date_test = date.today()
        self.time_test = datetime.now().strftime("%H:%M:%S")

    def add_pcr(self):
        with open('pcr_tests.csv', 'a', newline='') as fh:
            writer_object = writer(fh)
            x = [self.patient_id, self.pcr_id, self.result, self.date_test, self.time_test]
            writer_object.writerow(x)
            # Close the file object
            fh.close()

    @staticmethod
    def delete_pcr(in_pcr_id):
        flag = 0
        lines = list()
        with open('pcr_tests.csv', 'r', newline='') as in_f:
            reader = csv.reader(in_f)
            for row in reader:
                x = str(row).split(",")
                x = str(row).split("'")
                if x[3] == in_pcr_id:
                    flag = 1
                    continue  # skip row / don't write row
                else:
                    lines.append(row)
            in_f.close()
            # print(lines)
            with open('pcr_tests.csv', 'w', newline='') as out_f:
                out_f.truncate()
                writer1 = csv.writer(out_f)
                writer1.writerows(lines)
            out_f.close()
            if flag == 0:
                raise InputError("pcr test id does not exit")

    @staticmethod
    def delete_pcr_test_file(file):
        lines = list()
        print(file)
        with open(file, 'r', newline='') as fh:
            for row1 in fh:
                x1 = str(row1).split(",")
                with open('pcr_tests.csv', 'r', newline='') as in_f:
                    reader = csv.reader(in_f)
                    for row2 in reader:
                        x2 = str(row2).split(",")
                        x2 = str(row2).split("'")
                        if x2[3] == x1[1]:
                            continue  # skip row / don't write row
                        else:
                            lines.append(row2)
                    in_f.close()
            fh.close()
        with open('pcr_tests.csv', 'w', newline='') as out_f:
            out_f.truncate()
            writer2 = csv.writer(out_f)
            writer2.writerows(lines)
        out_f.close()


    @staticmethod
    def update_test(test_id, new_result):
        flag = 0
        if re.fullmatch('True|False', new_result) and re.fullmatch('[1-9][0-9]*', test_id):
            lines = list()
            with open('pcr_tests.csv', 'r', newline='') as test_file:
                reader = csv.reader(test_file)
                for row in reader:
                    x = str(row).split(",")
                    x = str(row).split("'")
                    if x[3] == test_id:
                        flag = 1
                        row[2] = new_result
                        lines.append(row)
                    else:
                        lines.append(row)

            test_file.close()
            with open('pcr_tests.csv', 'w', newline='') as out_f:
                out_f.truncate()
                writer2 = csv.writer(out_f)
                writer2.writerows(lines)
            out_f.close()
        if flag == 0:
            raise InputError("Wrong input")

    @staticmethod
    def positive_rep(patient_name_key):
        my_tuple_list = []
        this_dict = {}
        with open('patient.csv', 'r', newline='') as fh:
            reader1 = csv.reader(fh)
            for row1 in reader1:
                x = str(row1).split(",")
                x = str(row1).split("'")
                if x[3] == patient_name_key:
                    patient_id_key = x[1]
        fh.close()
        with open('pcr_tests.csv', 'r', newline='') as file_test:
            reader2 = csv.reader(file_test)
            for row2 in reader2:
                x = str(row2).split(",")
                x = str(row2).split("'")
                if x[1] == patient_id_key and x[5] == 'True':
                    my_tuple_list.append((x[7], x[9]))
        file_test.close()
        this_dict[patient_name_key] = my_tuple_list
        return this_dict

    @staticmethod
    def high_risk_people_rep():
        list_of_dic = list()
        flag = 0
        current_year = date.today().year
        with open('patient.csv', 'r', newline='') as fh:
            reader1 = csv.reader(fh)
            for row1 in reader1:
                x = str(row1).split(",")
                x = str(row1).split("'")
                if current_year - int(x[5]) > 80:
                    flag = 1
                    list_of_dic.append(PcrTest.positive_rep(x[3]))

                elif 60 <= current_year - int(x[5]) <= 80 and "walla" in x[9]:
                    flag = 1
                    list_of_dic.append(PcrTest.positive_rep(x[3]))

        fh.close()
        if flag == 1:
            return list_of_dic
        else:
            raise InputError("There are no high risk patients")

    @staticmethod
    def rep_by_dates(start_date, end_date):
        l = list()
        if start_date <= end_date and re.fullmatch('[0-9]{4}-[0-9]{2}-[0-9]{2}', start_date) and re.fullmatch(
                '[0-9]{4}-[0-9]{2}-[0-9]{2}', end_date):
            with open('pcr_tests.csv', 'r', newline='') as fh:
                reader1 = csv.reader(fh)
                for row1 in reader1:
                    x = str(row1).split(",")
                    x = str(row1).split("'")
                    if start_date <= x[7] <= end_date:
                        l.append(row1)
            fh.close()
        if len(l) == 0:
            raise InputError("dates not like the format -> yyyy-mm-dd\nor\nend date before start date...")
        else:
            return l
