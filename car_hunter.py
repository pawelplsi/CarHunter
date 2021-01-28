import os
import time
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


bestExam = None
while True:
    try:
        exams = fetch_exams(WORD_ID, EXAM_CATEGORY, months_forward=3)
        exams_practical = [exam for exam in exams if exam.type == ExamType.PRACTICE]
        exams_practical.sort(key=lambda exam: exam.date)
        exam = exams_practical[0]
        if bestExam != exam:
            if exam.date < bestExam.date:
                notify("NEW BEST EXAM: " + str(exam))
                print("NEW BEST EXAM: " + str(exam))
            else:
                notify("CHUJ: " + str(exam))
                print("CHUJ: " + str(exam))
            bestExam = exam
    except Exception as e:
        print(e)

    time.sleep(3 * 60)
