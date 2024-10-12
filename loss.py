import gungi
import copy
import random

class Org():
    def __init__(self):
        a = "A"

    def search(self, gungi, max_depth=1, color="WHITE"):
        infe = self.tree(max_depth, gungi)
        #print(infe)
        return infe[0]


    
    def tree(self, max_depth, gungi, depth=0, turn=0):
        player = ["WHITE", "BLACK"][turn%2]
        if max_depth > depth:
            """board_valid = {"game": gungi,
                            "depth": depth,
                            "player": player,
                            "player_num": turn%2,
                            }"""
            player_num = turn%2
            depth += 1
            turn += 1

            legal_moves = gungi.legal_move()[player_num]

            max_value = None
            next_value = None
            next_moves = []
            move_and_value = []
            candy = random.sample(legal_moves, min(len(legal_moves),100))
            for i in candy:
            #for i in legal_moves[:100]:
                test = copy.deepcopy(gungi)
                test.play_piece(i)
                value = self.value(test)

                if max_value == None: ##1パターン目を基準値にする
                    move_and_value.append([i, value])
                    max_value = value

                if player_num==0:
                    if value > max_value:
                        move_and_value = []

                    if value >= max_value:
                        move_and_value.append([i, value])
                        max_value = value
                else:
                    if value < max_value:
                        move_and_value = []
                    if value <= max_value:
                        move_and_value.append([i, value])
                        max_value = value

                m1, v1 = move_and_value[0]
                m2, v2 = self.tree(max_depth, test, depth, turn)
                v3 = v1+v2
                if next_value == None:
                    next_value = v3

                if next_value < v3:
                    next_value = v3
                    next_moves.append([m1,m2,next_value])


            #print(next_moves)

            return m1, v1

        else:
            #move = None
            #gungi.show_board()
            value = self.value(gungi)
            #print("Tree:",max_depth, ", now depth:",depth , ", value:", value, ", move:",move)
            return [], value

    def value(self, gungi):
        board = gungi.board
        value = 0
        y = len(board)
        x = len(board[0])
        if gungi.all_piece[26].state == gungi.all_piece[26].state_taken():
            return 100
        for i in range(0,y):
            for j in range(0,x):
                cell = board[i][j]
                active_piece = cell.active_piece()
                try:
                    pid = active_piece.pieceID
                except:
                    pid = -1

                if 1 <= pid <= 25:
                    value += cell.level() * cell.level() 
                else:
                    value -= cell.level() * cell.level()
                if pid == 1:
                    value += cell.level() #師の高さを追加で評価
                if pid == 26:
                    value -= cell.level()
                    ey = cell.y
                    ex = cell.x

                    for k in range(0,x):
                        if 0<= (ex - k) < 9:
                            pass
                        elif 0<= (ex + k) < 9:
                            k = -1 * (ex - k)
                        try:
                            mpid = board[ey][k].active_piece()
                            if 0 < mpid  <= 25:
                                mylevel = board[ey][k].level()
                                distance = abs(ex - k)
                                value += mylevel*distance
                        except:
                            pass

                    for k in range(0,y):
                        if 0<= (ey - k) < 9:
                            pass
                        elif 0<= (ey + k) < 9:
                            k = -1 * (ey - k)
                        try:
                            mpid = board[k][ex].active_piece().pieceID
                            if 0 < mpid <= 25:
                                mylevel = board[k][ex].level()
                                distance = abs(ex - k)
                                value += mylevel*distance
                        except:
                            pass


        return value
                
#Org()