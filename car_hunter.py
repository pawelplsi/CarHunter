import os
import datetime
import time as systime
from wordapi import *

import telegram
from dotenv import load_dotenv

load_dotenv(verbose=True)

TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
WORD_ID = os.getenv("WORD_ID")
EXAM_CATEGORY = os.getenv("EXAM_CATEGORY")
LOGIN = os.getenv("LOGIN")
PASSWORD = os.getenv("PASSWORD")

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def notify(text):
    bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=text)


# fetch_exams(WORD_ID, EXAM_CATEGORY, datetime.now())
# exit()
bestExam = None
while True:
    try:
        authorization = getAuthorization(LOGIN, PASSWORD)
        print(f"AUTH = {authorization}")
        while True:
            exams = fetch_exams(authorization, WORD_ID, EXAM_CATEGORY, datetime.now())
            exams_practical = [exam for exam in exams if exam.type == ExamType.PRACTICE]
            exams_practical.sort(key=lambda exam: exam.date)
            exam = exams_practical[0]
            if bestExam != exam:
                if bestExam is None or exam.date < bestExam.date:
                    notify("GIT: " + str(exam))
                    print("GIT: " + str(exam))
                else:
                    notify("DUPA: " + str(exam))
                    print("DUPA: " + str(exam))
                bestExam = exam
            for P in exams_practical:
                print (P)
            systime.sleep(60)
    except Exception as e:
        print(e)
    systime.sleep(60)
