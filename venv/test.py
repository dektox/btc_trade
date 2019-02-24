#!/usr/bin/python
# -*- coding: cp1251 -*-
import csv


prev_ids = []

with open('{}.csv'.format(pair[1]), 'r') as file:
    users = csv.reader(file, delimiter=';')
    for user in users:
        if user[3] != 'id':
            prev_ids.append(int(user[3]))
try:
    a = input('Finished. Press any key to quit')
except SyntaxError:
    pass