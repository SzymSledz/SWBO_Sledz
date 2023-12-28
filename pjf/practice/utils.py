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


def check_answer(card_id, answer):
    card = cards.query.filter_by(id=card_id).first()

    answer = answer.lower()
    card_translation = card.translation.lower()

    if answer == card_translation:
        return 'correct'

    mistake = False                          # 1 typo in word is allowed
    for i in range(len(cards.translation)):  # checks how many mistakes were made > 1 mistake == wrong answer
        if answer[i] != card_translation[i]:
            if mistake == True:
                return 'wrong'
            mistake = True
    return 'nearly'
