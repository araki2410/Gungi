#!/usr/local/bin/python3

import gungi

import random ### ランダム行動のために呼んでる。ランダム行動消したら不要
import time ###
import pickle

class Match:
    def __init__(self):
        self.gungi = gungi.Gungi()
        self.players = ["Black", "White"] #[後手,先手]
        self.gamephase = "init" ## init, setup, main, gameset
        self.new_game()

    def new_game(self):
        self.winner = None
        self.turn = 0
        self.gungi.init_game()

    def new_game_begginer01(self):
        self.new_game()
        self.gungi.setup_game_begginer01()
        self.gamephase = "main"

    def play_piece(self, score):
        match self.gamephase:
            case "setup":
                y,x,lv,pID = score 
                self.gungi.setup_piece(self.gungi.all_piece[pID], [y,x,lv])
            case "main":
                y,x,lv,pID = score 
                self.gungi.play_piece(self.gungi.all_piece[pID], [y,x,lv])
            case _:
                return False
        return True


    def possible_action(self):
        player = self.turn%2
        pieceIDs = self.gungi.return_playable_piece()[player].keys()
        actions = []
        for i in pieceIDs:
            ### ID i の駒の移動可能セル[0,0]毎に、段とiを挿入[0,0,段,i]して、可能な行動をリストにする。
            i_acts = self.gungi.return_movable_area(self.gungi.all_piece[i])
            list(map(lambda x: x.append(i), i_acts))
            actions = actions + i_acts
        return actions

    def check_gameset(self):
        suiIDs = [self.gungi.white_SUI, self.gungi.black_SUI]
        for suiID in suiIDs:
            sui = self.gungi.all_piece[suiID]
            try:
                y,x,lv = sui.location
                if (self.gungi.board[y][x].active_piece() != sui) or (sui.state != sui.state_board()):
                    return True
            except:
                ## 師の位置が取れない => 取られている
                return True

    def fullscore(self):
        return self.gungi.score

    def process(self, score=["y","x","lv"]):
        phase = self.gamephase
        match phase:
            case "init":
                self.new_game()
                #self.gamephase = "setup"
                self.new_game_begginer01()

                self.gamephase = "main"

            case "setup":
                ## 初期配置
                self.gamephase = "main"

            case "main":
                #print("try score: ", score)
                played = self.play_piece(score) ### [y,x,lv]

                if played:
                    self.turn += 1

                if self.check_gameset():
                    self.gamephase = "gameset"
                    self.winner = ["S","F"][self.turn%2]
                    #print("gameset")
                    #print("TURN:",self.turn, "   WINNER: ",self.players[self.turn%2])

            case "gameset":
                self.gamephase = "init"

            case _:
                print("ERROR: [CASE EXCEPTION] gamephase have a something error.")
                raise

        return self.gamephase

def main():
    logpath = "Log/"

    game = Match()
    phase = game.process()
    #game.gungi.show_board()


    while phase:
        phase = game.process(random.choice(game.possible_action()))
        #game.gungi.show_board()
        if phase == "gameset":
            if game.turn < 100:
                filename = time.strftime("%Y%b%d_%H:%M:%S_", time.gmtime()) + game.winner + str(game.turn)
                print(filename)

                pickle.dump(game.fullscore(), open(logpath+filename, mode='wb'))

            time.sleep(0.4)
            while not game.process() == "main":
                pass

        #print("=========")

main()