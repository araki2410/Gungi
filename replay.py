#!/usr/local/bin/python3

import gungi
import pickle
from sys import argv 

try:
    filepath = argv[1]
except:
    print("$ python3 replay.py Log/2024Oct07_15:06:42_F25")
    print()
    filepath = "Log/2024Oct07_15:06:42_F25"

gungi = gungi.Gungi()
score = pickle.load(open(filepath, 'rb'))
turn = 0
gungi.show_board()

for i in score:
    input("turn: " + str(turn))
    print("===============")
    turn += 1
    y,x,lv,pID = i
    piece = gungi.all_piece[pID]
    location = [y,x,lv]
    gungi.play_piece(piece,location)
    gungi.show_board()
    gungi.show_score(piece)
