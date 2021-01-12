import requests
import json
import itertools
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from enum import Enum
import telegram
import time


class ExamType(Enum):
    THEORY = 1
    PRACTICE = 2


class Exam:
    def __init__(self, exam_type, category, wordId, date, places, price):
        self.type = exam_type
        self.category = category
        self.wordId = wordId
        self.date = date
        self.places = places
        self.price = price

    def __str__(self):
        return str(self.type) + ", cat. " + str(self.category) + \
            ", word=" + str(self.wordId)+", date="+str(self.date) + \
            ", places="+str(self.places)+", price="+str(self.price)

    def __hash__(self):
        return hash(str(self))

    def __cmp__(self, other):
        return hash(self).__cmp__(hash(other))

    def __eq__(self, other):
        return hash(self) == hash(other)


def fetchExams(wordId="43", examCategory="B", monthsForward=1, month=None):
    if not month:
        month = date.today()
    month = month.replace(day=1)
    monthStr = month.strftime('%Y-%m')
    params = dict(
        wordId=wordId,
        examCategory=examCategory,
        month=monthStr
    )
    response = requests.get(
        "https://info-car.pl/services/word/ajax/getSchedule", params=params)
    if response.status_code != 200:
        raise "HTTP error: code "+response.status_code
    exams = list()

    def makeExam(examType, category, wordId, examObject):
        return Exam(examType, category, wordId,
                    datetime.strptime(examObject["date"], '%d.%m.%y %H:%M'), examObject["places"], examObject["amount"])

    data = json.loads(response.text)
    for term in data["terms"].values():
        for exam in term:
            if "theory" in exam:
                t = exam["theory"]
                exams.append(makeExam(ExamType.THEORY,
                                      examCategory, wordId, t))
            if "practice" in exam:
                practices = exam["practice"]
                for p in practices:
                    exams.append(makeExam(ExamType.PRACTICE,
                                          examCategory, wordId, p))
    if monthsForward <= 1:
        return exams
    return exams + fetchExams(wordId, examCategory, monthsForward-1,
                              month+relativedelta(months=1))


T_CHATID = 
T_TOKEN = 
bot = telegram.Bot(token=T_TOKEN)


def notify(text):
    bot.sendMessage(chat_id=T_CHATID, text=text)


bestExam = None
while(True):
    try:
        exams = fetchExams(monthsForward=3)
        ps = [p for p in exams if p.type == ExamType.PRACTICE]
        ps.sort(key= lambda e: e.date)
        e = ps[0]
        if bestExam != e:
            bestExam = e
            if e.date < bestExam.date:
                notify("NEW BEST EXAM: " + str(e))
                print("NEW BEST EXAM: " + str(e))
            else:
                notify("CHUJ: " + str(e))
                print("CHUJ: " + str(e))
    except Exception as e:
        print(e)
    time.sleep(3*60)

exams=fetchExams(month = datetime.now()+relativedelta(months=3))

ps=[p for p in exams if p.type == ExamType.PRACTICE]

for exam in exams:
    print(exam.date)
