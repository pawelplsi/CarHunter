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

bot = telegram.Bot(token=TELEGRAM_TOKEN)


def notify(text):
    bot.sendMessage(chat_id=TELEGRAM_CHAT_ID, text=text)


# fetch_exams(WORD_ID, EXAM_CATEGORY, datetime.now())
# exit()
bestExam = None
while True:
    try:
        exams = fetch_exams(WORD_ID, EXAM_CATEGORY, datetime.now())
        exams_practical = [exam for exam in exams if exam.type == ExamType.PRACTICE]
        exams_practical.sort(key=lambda exam: exam.date)
        exam = exams_practical[0]
        if bestExam != exam:
            if bestExam is None or exam.date < bestExam.date:
                notify("NEW BEST EXAM: " + str(exam))
                print("NEW BEST EXAM: " + str(exam))
            else:
                notify("CHUJ: " + str(exam))
                print("CHUJ: " + str(exam))
            bestExam = exam
        for P in exams_practical:
            print (P)
    except Exception as e:
        print(e)

    systime.sleep(60)
