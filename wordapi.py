import json
from enum import Enum
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta
import requests


class ExamType(Enum):
    THEORY = 1
    PRACTICE = 2


class Exam:
    def __init__(self, ID, exam_type, category, word_id, date, places, price):
        self.ID = ID 
        self.type = exam_type
        self.category = category
        self.word_id = word_id
        self.date = date
        self.places = places
        self.price = price

    def __str__(self):
        return str(self.type) + ", cat. " + str(self.category) + \
            ", word=" + str(self.word_id) + ", date=" + str(self.date) + \
            ", places=" + str(self.places) + ", price=" + str(self.price) + ", id="+str(self.ID)

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        return hash(self).__cmp__(hash(other))

    def __eq__(self, other):
        return hash(self) == hash(other)


def make_exam(exam_type: ExamType, category: str, word_id: str, examObject):
    return Exam(examObject["id"], exam_type, category, word_id,
            datetime.strptime(examObject["date"], '%Y-%m-%dT%H:%M:%S'),
                examObject["places"], examObject["amount"])


def fetch_exams(word_id: str, exam_category: str, start_date: datetime, end_date: datetime = None):
    if not end_date:
        end_date = start_date + relativedelta(months=1)

    def jsonDate(dt): return datetime.isoformat(dt)[:-3]+'Z'

    api_params = dict(
        wordId=word_id,
        category=exam_category,
        startDate=jsonDate(start_date),
        endDate=jsonDate(end_date),
    )

    response = requests.put(
        "https://info-car.pl/api/word/word-centers/exam-schedule", data=json.dumps(api_params), headers = {"Content-Type": "application/json"})
    if response.status_code != 200:
        print("HTTP error: code " + str(response.status_code))

    exams = list()
    data = json.loads(response.text)
    for day in data["schedule"]["scheduledDays"]:
        for hour in day["scheduledHours"]:
            for theory in hour["theoryExams"]:
                exams.append(make_exam(ExamType.THEORY, exam_category, word_id, theory))
            for practice in hour["practiceExams"]:
                exams.append(make_exam(ExamType.PRACTICE, exam_category, word_id, theory))
    return exams
