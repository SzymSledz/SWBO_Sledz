import random as rand
from flask import Flask, redirect, url_for, render_template, request, session, flash, Blueprint
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from pjf import app
from pjf import db
from pjf.models import users, groups, cards
from pjf.main import *

def swapPositions(list, pos1, pos2):
    list[pos1], list[pos2] = list[pos2], list[pos1]
    return list
def shuffle_list(list):

    for j in range(3):
        for i in range(len(list)):
            randomNumber = rand.randint(0, len(list) - 1)
            list = swapPositions(list, i, randomNumber)

    return list

def check_answer(card, answer): # card - object form DB answer - string

    answer = answer.lower()
    card_translation = card.translation.lower()
    correct_ans_len = len(str(card_translation))
    users_ans_len = len(str(answer))

    if answer == card_translation: # if answer and translation are exactly the same
        return 'correct'

    if abs(correct_ans_len - users_ans_len) > 1: # if length differenc beetwen translation and anser > 1
        return 'wrong'

    print("odp: " + answer + " poprawna: " + card_translation)

    mistake = False # 1 typo in word is allowed

    for i in range(correct_ans_len):            # checks how many mistakes were made > 1 mistake == wrong answer
        if i >= users_ans_len:                     # if index is out of answers scope
            if mistake == True:                 # if it's 2nd mistake
                return 'wrong'
            mistake = True                      # if it's 1st mistake
        elif answer[i] != card_translation[i]:  # if letters are different
            if mistake == True:                 # it's 2nd mistake
                return 'wrong'
            mistake = True                      # if its 1st mistake

    if users_ans_len > correct_ans_len:
        if not mistake:
            return 'nearly'         # there is only 1 mistake - last letter
        return 'wrong'              # there were 2 mistakes - previous mistake and last letter
    return 'nearly'                 # only last letter is wrong


def check_answers(cards, answers): # check for whole lesson
    results = []

    for i in range(len(cards)):
        result = check_answer(cards[i], answers[i])
        results.append(result)

    return results
