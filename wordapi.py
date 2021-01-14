import json
from enum import Enum
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import requests

class ExamType(Enum):
    THEORY = 1
    PRACTICE = 2


class Exam:
    def __init__(self, exam_type, category, word_id, date, places, price):
        self.type = exam_type
        self.category = category
        self.word_id = word_id
        self.date = date
        self.places = places
        self.price = price

    def __str__(self):
        return str(self.type) + ", cat. " + str(self.category) + \
               ", word=" + str(self.word_id) + ", date=" + str(self.date) + \
               ", places=" + str(self.places) + ", price=" + str(self.price)

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        return hash(self).__cmp__(hash(other))

    def __eq__(self, other):
        return hash(self) == hash(other)


def make_exam(exam_type: ExamType, category: str, word_id: str, examObject):
    return Exam(exam_type, category, word_id,
                datetime.strptime(examObject["date"], '%d.%m.%y %H:%M'),
                examObject["places"], examObject["amount"])


def fetch_exams(word_id: str, exam_category: str, months_forward: int = 1, month=None):
    if not month:
        month = date.today()

    month = month.replace(day=1)
    month_str = month.strftime('%Y-%m')

    api_params = dict(
        wordId=word_id,
        examCategory=exam_category,
        month=month_str
    )

    response = requests.get(
        "https://info-car.pl/services/word/ajax/getSchedule", params=api_params)

    if response.status_code != 200:
        print("HTTP error: code " + str(response.status_code))

    exams = list()
    data = json.loads(response.text)
    for term in data["terms"].values():
        for exam in term:
            if "theory" in exam:
                exams_theory = exam["theory"]
                exams.append(make_exam(ExamType.THEORY,
                                       exam_category, word_id, exams_theory))
            if "practice" in exam:
                exams_practical = exam["practice"]
                for practical_exam in exams_practical:
                    exams.append(make_exam(ExamType.PRACTICE,
                                           exam_category, word_id, practical_exam))
    if months_forward <= 1:
        return exams

    # Recursively fetch months
    return exams + fetch_exams(word_id, exam_category, months_forward - 1,
                               month + relativedelta(months=1))
