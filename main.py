import random
import numpy as np
from progress.bar import Bar
import mysql.connector
import time
import logging
from random import randint

SqlFormulaUser = 'INSERT INTO DataUser (User_name, User_surname,User_Age) VALUES '
SqlFormulaTask = 'INSERT INTO DataTask (Task_TypeOfDoctor, Task_NameProced,Task_Pain,Task_Cost) VALUES '
count = 100


def takes_names():
    logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')
    names = 'names.txt'
    try:
        with open(names, encoding='utf-8') as file:
            data_name = file.read().split('\n')

        logging.debug("names.txt file has %d words", len(data_name))

    except OSError as e:
        logging.error("error reading the file %d", names)

    return data_name


def takes_surnames():
    logging.basicConfig(level=logging.DEBUG, filename='myapp.log', format='%(asctime)s %(levelname)s:%(message)s')
    surnames = 'surname.txt'
    try:
        with open(surnames, encoding='utf-8') as file:
            data_surnames = file.read().split('\n')

        logging.debug("surname.txt file has %d words", len(data_surnames))

    except OSError as e:
        logging.error("error reading the file %d", surnames)
    return data_surnames


if __name__ == "__main__":
    # Данные для DataTask
    doctor = ['Allergist', 'Gastroenterologist', 'Hepatologist', 'Gerontologist', 'Cardiologist', 'Mammologist',
              'Neurologist', 'Neonatologist', 'Oncologist', 'Ophthalmologist', 'Pediatrician', 'Psychotherapist',
              'Resuscitator']
    procedure = ['inspection', 'Prescribe treatment', 'Getting Help']
    pain = ['acute', 'planned']

    bar = Bar('Processing', max=count)
    for i in range(count):
        SqlFormulaUser += f"('{takes_names()[randint(1, len(takes_names()) - 1)]}','{takes_surnames()[randint(1, len(takes_surnames()) - 1)]}',{np.random.randint(18, 99)}),\n "
        bar.next()
    bar.finish()
    SqlFormulaUser = SqlFormulaUser[:-3] + ';'
    # print(SqlFormulaUser)

    bar = Bar('Processing', max=count)
    for i in range(count):
        SqlFormulaTask += f"('{random.choice(doctor)}','{random.choice(procedure)}','{random.choice(pain)}',{np.random.randint(1000, 2000)}),\n "
        bar.next()
    bar.finish()
    SqlFormulaTask = SqlFormulaTask[:-3] + ';'

    # print(SqlFormulaTask)

    with mysql.connector.connect(
            host='localhost',
            port=3306,
            user='TestUser',
            password='05062002',
            database='testtask') as connection:
        cursor = connection.cursor()
        cursor.execute(SqlFormulaUser)
        cursor.execute(SqlFormulaTask)
        connection.commit()
