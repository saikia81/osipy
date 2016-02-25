__author__ = 'Pablo'

course_information_ids = []

class Course(object):
    def __init__(self, information):
        self.name = information['Cursus']
        self.information = information

    def __get__(self, index):
        return self.information[index]

    def __str__(self):
        information_string = self.name + "\n"
        for info in self.informaion:
            information_string += "-" + info + ": " + self.information[info] + "\n"
        return  information_string