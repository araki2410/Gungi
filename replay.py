#!/usr/local/bin/python3

import gungi
from sys import argv 

try:
    filepath = argv[1]
except:
    filepath = "Log/2024Oct19_16:59:12_S22"
    print("$ python3 replay.py <FILE PATH>")
    print("$ python3 replay.py", filepath)
    print()


gungi = gungi.Gungi()
score = open(filepath, 'r').read().split(" ")
turn = 0
gungi.show_board()

for i in score:
    input("turn: " + str(turn))
    print("===============")
    log16 = format(int(i,16), "016b")
    to_location = gungi.hex2location(hex(int(log16[8:],2)))
    pID = int(log16[2:8],2)
    act = int(log16[:2], 2)
    turn += 1

    move = to_location + [pID]
    piece = gungi.all_piece[pID]
    gungi.play_piece(move)
    gungi.show_board()
    gungi.show_score(piece)
