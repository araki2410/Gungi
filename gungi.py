#!/usr/bin/python3

class Gungi:
    def __init__(self, y=9, x=9):
        self.width = x
        self.height = y
        self.max_level = 3
        self.white_SUI = 1
        self.black_SUI = 26

        self.init_game()

    def init_game(self):
        rowid = ["1","2","3","4","5","6","7","8","9"]
        colid = ["a","b","c","d","e","f","g","h","i"]
        self.score = []
        self.all_piece = {}

        self.board = []
        for i in range(self.height):
            cid = rowid[i]+colid[i]
            self.board.append([0]*self.width)
            for j in range(self.width):
                self.board[i][j]=Cell(i,j,cid)

        """
        _allpiece={
            1:"帥", 2:"大", 3:"中", 4:"小", 5:"小", 6:"侍", 7:"侍", 8:"槍", 9:"槍", 10:"槍",
            11:"馬", 12:"馬", 13:"忍", 14:"忍", 15:"砦", 16:"砦", 17:"兵", 18:"兵", 19:"兵", 20:"兵", 
            21:"砲", 22:"弓", 23:"弓", 24:"筒", 25:"謀",
            26:"帥", 27:"大", 28:"中", 29:"小", 30:"小", 31:"侍", 32:"侍", 33:"槍", 34:"槍", 35:"槍",
            36:"馬", 37:"馬", 38:"忍", 39:"忍", 40:"砦", 41:"砦", 42:"兵", 43:"兵", 44:"兵", 45:"兵",
            46:"砲", 47:"弓", 48:"弓", 49:"筒", 50:"謀"
        }
        """
        for i in range(1, 51):
            self.all_piece[i]=Piece(i)

    def add_score(self, piece, from_location, setup=False, take=False, change=False):
        blank = "00"
        if from_location == None:
            from_hex = "00"
        else:
            from_hex = self.location2hex(from_location)

        if setup:
            act = 1
        elif take:
            act = 2
        elif change:
            act = 3
        else:
            act = 0

        pID_bin = format(piece.pieceID, "06b")
        to_hex = self.location2hex(piece.location)

        #log32 = blank + from_hex + format(int((str(act) + pID_bin), 2), "02x") + to_hex
        log16 = format(int((format(act,"02b") + pID_bin), 2), "02x") + to_hex

        self.score.append(log16)
        return log16

    def show_score(self, piece):
        y, x, level = piece.location
        for_pc = [y, x, level, piece.pieceID]
        for_human = str(9-x)+str(y+1)+str(level)+piece.piecetype
        print(for_pc, for_human)
        

    def play_piece(self, move, setup=False, change=False):
        ## 指定の位置に指定の駒を打てるか検証して、可能なら操作を実行する。
        y,x,to_lv,pID = move
        piece = self.all_piece[pID]
        from_location = piece.location
        take = False
        result = False
        if setup:
            result = self.setup_piece(move)

        elif piece.state == piece.state_hand():
            ### 「新」
            if self.can_drop(move):
                self.push(move)
                result = True
            else:
                result = False

        elif piece.state == piece.state_board():
            ### 動かしたい駒が盤上にある場合、今の状況から目的地に動けるか確認してから動く。
            ## 駒から見てどこに動くのか逆算してから、動けるかどうか確認する。
            vector = [move[0]-from_location[0], move[1]-from_location[1]]
            if self.can_move(piece, vector):
                ## 駒が重なる場合取る
                to_cell = self.board[y][x]
                if to_cell.level() >= to_lv:
                    to_cell.take_piece(piece)
                    take = True

                result = self.push(move)

        if result:
            self.add_score(piece, from_location, setup, take, change)
        else:
            print("操作に失敗しました。")

        return result

    def push(self, move):
        ### 駒を設置する。ここでは設置の正当性は検証しない。
        y,x,lv,pID = move
        piece = self.all_piece[pID]
        try:
            from_y, from_x, _ = piece.location
            self.board[from_y][from_x].pop_piece()
        except:
            pass

        self.board[y][x].push_piece(piece)
        piece.location = [y,x,lv]
        piece.state = piece.state_board()
        return True

    def change_piece(self, location):
        ### 「謀将」用関数
        return True

    def setup_piece(self, move):
        ### 初期配置
        if move[3] < 26: ### WHITE
            if move[0] < self.height-3: # < 6:
                ### 初期配置は3列目まで
                print("初期配置は3列目まで_W")
                return False

        else:                  ### BLACK
            if move[0] > 2:
                ### 初期配置は3列目まで
                print("初期配置は3列目まで_B")
                return False

        if self.can_drop(move):
            self.push(move)
            return True

        raise

    def show_board(self):
        for i in self.board:
            for j in i:
                cell = [0,0,0]
                l = 0
                for k in j.piece_list:
                    cell[l] = k
                    l += 1
                print("[", end="")
                for k in cell:
                    try:
                        pID = k.pieceID
                        if pID < 26:
                            print("\x1b[7m" + k.piecetype + "\x1b[m", end="")
                        else:
                            print(k.piecetype,end="")
                    except:
                        print(" 0",end="")

                print("]", end="")
            #print()
            print()

    def merge_move(self, moves):
        hands = {}
        for i in moves:
            pID = i[3]
            if self.all_piece[pID].state == self.all_piece[pID].state_hand():
                ptype = self.all_piece[pID].piecetype
                vecs = hands.get(ptype, {})
                hands[ptype] = vecs
                vec = vecs.get(pID, [])
                vec.append(i[:3])
                vecs[pID] = vec
        for i in hands.keys():
            if len(hands[i]):
                l = list(hands[i].keys())[1:]
                for j in l:
                    for k in hands[i][j]:
                        rm_move = k+[j]
                        moves.remove(rm_move)
        return moves

    def legal_move(self):
        w_pIDs = self.return_playable_piece()[0].keys()
        b_pIDs = self.return_playable_piece()[1].keys()
        w_actions = []
        b_actions = []
        for i in w_pIDs:
            ### ID i の駒の移動可能セル[0,0]毎に、段とiを挿入[0,0,段,i]して、可能な行動をリストにする。
            i_acts = self.return_movable_area(self.all_piece[i])
            list(map(lambda x: x.append(i), i_acts))
            w_actions = w_actions + i_acts
        for i in b_pIDs:
            i_acts = self.return_movable_area(self.all_piece[i])
            list(map(lambda x: x.append(i), i_acts))
            b_actions = b_actions + i_acts

        return self.merge_move(w_actions), self.merge_move(b_actions)

    def return_playable_piece(self):
        white = {}
        black = {}
        for i in self.all_piece.values():
            if i.state == i.state_hand() or i.state == i.state_board():
                if i.pieceID < 26:
                    white[i.pieceID]=[i.piecetype, i.location]
                else:
                    black[i.pieceID]=[i.piecetype, i.location]
        return white, black

    def return_dropable_area(self, piece):
        ### 「新」可能な範囲（range()）を返す。
        ## 白黒駒で上下が異なる
        if piece.pieceID <= 25: ### WHITE
            pIDrange = range(1,25)
            ran = range(0, self.height)
        else:
            pIDrange = range(26,51)
            ran = range(self.height-1, -1, -1)
        
        ## 自駒の先頭を、相手陣地側から確認する。
        for y in ran:
            for x in ran:
                ## 指定したセルに駒がある場合、駒のIDを取得する。
                try:
                    pID = self.board[y][x].active_piece().pieceID
                except:
                    pID = -1

                ## 取得したIDから、自駒の場合そこで探索を終了する。「新」可能な範囲を返す。
                if pIDrange.count(pID):
                    if piece.pieceID <= 25: ### WHITE
                        return range(y, self.height)
                    else:
                        return range(0,y+1)


    def return_movable_area(self, piece):
        potential = piece.potential
        movable_cell = []
        ### 手駒/盤駒のみ判定
        if piece.state == piece.state_taken() or piece.state == piece.state_ban():
            return None
        elif piece.state == piece.state_hand():
            y_range = self.return_dropable_area(piece)
            for y in y_range:
                for x in range(0, self.width):
                    locations = self.can_drop([y,x,0,piece.pieceID])
                    if locations:
                        movable_cell.append(locations)
            return movable_cell

        for i in range(1, piece.level()+1):
            ### ツケの段ごとに移動範囲を追加
            for vector in potential[i]:
                ### 移動範囲に移動可能か判定
                ## 相対座標[0,-1]を入力して、絶対座標[7,4,1]をlocationsに受け取る
                locations = self.can_move(piece, vector)
                if locations:
                    movable_cell = movable_cell + locations
        
        return movable_cell


    def can_drop(self, move):
        ### 指定の位置に指定の駒を「新」できるか検証する
        to_y, to_x, _, pID = move
        piece = self.all_piece[pID]
        try:
            to_pID = self.board[to_y][to_x].active_piece().pieceID
        except:
            to_pID = -1

        ## 手駒以外は「新」できない
        if piece.state != piece.state_hand():
            return False
        ## 盤外には設置できない
        if to_y >= self.height or to_y < 0 or to_x >= self.width or to_x < 0:
            return False
        ## 相手駒の上には「新」できない
        if (0 < to_pID <= 25 and pID > 25) or (to_pID >= 26 and pID < 26):
            return False
        ## 帥の上には「新」できない
        if to_pID == self.white_SUI or to_pID == self.black_SUI:
            return False
        ## すでに3段の場合、4段以上ツケることはできない。
        if self.board[to_y][to_x].level() >= self.max_level:
            return False

        return [to_y, to_x, self.board[to_y][to_x].level()+1]

    def can_move(self, piece, move_vector):
        ### 駒と移動先を比較して、移動可能か判断
        ## 取られている or 使用外の駒は移動不可
        pID = piece.pieceID
        if piece.state == piece.state_ban() or piece.state == piece.state_taken():
            return False

        ## 「新」
        if piece.state == piece.state_hand():
            ### この関数では「新」の範囲を確認しない
            raise
            return False
        
        ## 盤上から盤上へ動かす場合、詳細に判断する
        if piece.state == piece.state_board():
            y1,x1,level1 = piece.location
            vec_y,vec_x = move_vector
            to_y = y1 + vec_y
            to_x = x1 + vec_x

            try:
                to_cell = self.board[to_y][to_x]
            except:
                ### 盤外
                return False

            try:
                to_pID = to_cell.active_piece().pieceID
            except:
                to_pID = -1

            ## 動かしたい駒の上に、別の駒が乗っていないか
            if not (piece == self.board[y1][x1].active_piece()):
                return False

            ## 駒の性能通りの動きか
            if not (piece.potential[1]+piece.potential[2]+piece.potential[3]).count([vec_y,vec_x]):
                return False

            ## 盤外 (目的地toがマイナスの場合、端から端にワープしてしまうので、これを防ぐ)
            if to_y < 0 or to_x < 0:
                return False

            ### 段位差 1から3にはツケられない。
            if self.board[to_y][to_x].level() > piece.level():
                return False

            ### 自駒帥の上にはツケられない
            if (to_pID == self.white_SUI and pID < 26) or (to_pID == self.black_SUI and pID >= 26):
                return False

            ### 3段目が自駒の場合は移動できない
            if to_cell.level() == self.max_level:
                if pID > 25 and to_cell.active_piece().pieceID > 25:
                    return False
                if pID <= 25 and to_cell.active_piece().pieceID <= 25:
                    return False

            ### 駒を飛び越えられるか
            if abs(vec_y) >= 2 or abs(vec_x) >= 2:
                ### 砲, 弓, 筒 = [21,22,23,24,46,47,48,49] は、前方移動のみ飛び越えができる。別処理
                if [21,22,23,24,46,47,48,49].count(pID):
                    ### 未実装
                    if pID <= 25: ## WHITE
                        dir = -1
                    else: ## BKACK
                        dir = 1

                    ## 前方移動。飛び越えられるか判定する
                    if (vec_y > 0 and dir < 0) or (vec_y < 0 and dir > 0):
                        ## 正面 (砲, 弓, 筒）
                        if vec_x == 0: 
                            if vec_y > 0:
                                ran = range(y1+1, to_y)
                            else:
                                ran = range(to_y+1, y1)
                            for i in ran:
                                if self.board[i][to_x].level() > piece.level():
                                    return False
                            pass

                        ## 桂馬移動 (弓のみ)
                        else:
                            if self.board[y1+dir][x1].level() > piece.level():
                                # 1マス正面が、自マスより段が高い場合飛び越えは不可
                                return False
                            else:
                                i = 0
                                xdic = -1
                                y_range = range(y1+2, to_y)
                                if vec_x > 0:
                                    xdic = 1
                                for j in y_range:
                                    i += 1
                                    k = x1 + (i * xdic)
                                    if self.board[j][k].level() > piece.level():
                                        return False
                            pass

                    else:
                        ## 後方 or 横 移動の場合飛び越えできない。通常処理へ
                        pass
                
                ### 通常の駒は飛び越えができない。移動先への直線上に別の駒があったら移動できない
                ## 斜め移動
                elif abs(vec_y) >= 2 and abs(vec_x) >= 2:
                    i = 0
                    xdic = -1
                    if vec_y > 0:
                        y_range = range(y1+1, to_y)
                    else:
                        y_range = range(to_y+1, y1)
                    if vec_x > 0:
                        xdic = 1
                    for j in y_range:
                        i += 1
                        k = x1 + (i * xdic)
                        if self.board[j][k].level() > 0:
                            return False
                    pass

                ## 縦移動
                elif abs(vec_y) >= 2:
                    if vec_y > 0:
                        ran = range(y1+1, to_y)
                    else:
                        ran = range(to_y+1, y1)
                    for i in ran:
                        if self.board[i][to_x].level() > 0:
                            return False
                    pass

                ## 横移動
                elif abs(vec_x) >= 2:
                    if (vec_x > 0):
                        ran = range(x1+1, to_x)
                    else:
                        ran = range(to_x+1, x1)
                    for i in ran:
                        if self.board[to_y][i].level() > 0:
                            return False
                    pass

        ### 駒を置けるので、既存の駒を取れるかどうか確認して、設置可能な座標[y,x,level]を返す
        cells = []
        if to_pID > 0:
            level = to_cell.level()
            if level < self.max_level:
                if to_pID == 1 or to_pID == 26:
                    ## 帥の場合は取る。ツケられないことにする。
                    pass
                else:
                    ## 移動先が2段以下なら、ツケることが可能
                    cells.append([to_y,to_x,level+1])
        
            enemy_count = 0
            if (to_pID > 25 and pID <= 25):
                for i in to_cell.piece_list:
                    if range(26,51).count(i.pieceID):
                        enemy_count += 1
                cells.append([to_y,to_x,level+1-enemy_count])
            elif (to_pID <= 25 and piece.pieceID > 25):
                for i in to_cell.piece_list:
                    if range(1,26).count(i.pieceID):
                        enemy_count += 1
                cells.append([to_y,to_x,level+1-enemy_count])
        else:
            cells.append([to_y,to_x,1])

        return cells

    def location2hex(self, location):
        y,x,lv = location
        dec = y + (self.width * x) + (self.width * self.height * (lv-1))
        return format(dec, '02x')

    def hex2location(self, hex):
        dec = int(hex, 16)
        lv = int(dec / (self.width * self.height))
        x = int((dec-(self.width * self.height * lv))/ self.height)
        y = dec  - (self.width * self.height * lv) - (self.width * x)
        location = [y,x,lv+1]
        return location


    def setup_game_begginer01(self):
        self.init_game()
        self.play_piece([8,4,1,1], setup=True)
        self.play_piece([8,3,1,2], setup=True)
        self.play_piece([8,5,1,3], setup=True)
        self.play_piece([6,3,1,6], setup=True)
        self.play_piece([6,5,1,7], setup=True)
        self.play_piece([7,4,1,8], setup=True)
        self.play_piece([7,1,1,13], setup=True)
        self.play_piece([7,7,1,14], setup=True)
        self.play_piece([6,2,1,15], setup=True)
        self.play_piece([6,6,1,16], setup=True)
        self.play_piece([6,0,1,17], setup=True)
        self.play_piece([6,4,1,18], setup=True)
        self.play_piece([6,8,1,19], setup=True)
        self.all_piece[21].state = self.all_piece[1].state_ban()
        self.all_piece[22].state = self.all_piece[1].state_ban()
        self.all_piece[23].state = self.all_piece[1].state_ban()
        self.all_piece[24].state = self.all_piece[1].state_ban()
        self.all_piece[25].state = self.all_piece[1].state_ban()
        self.play_piece([0,4,1,26], setup=True)
        self.play_piece([0,5,1,27], setup=True)
        self.play_piece([0,3,1,28], setup=True)
        self.play_piece([2,3,1,31], setup=True)
        self.play_piece([2,5,1,32], setup=True)
        self.play_piece([1,4,1,33], setup=True)
        self.play_piece([1,1,1,38], setup=True)
        self.play_piece([1,7,1,39], setup=True)
        self.play_piece([2,2,1,40], setup=True)
        self.play_piece([2,6,1,41], setup=True)
        self.play_piece([2,0,1,42], setup=True)
        self.play_piece([2,4,1,43], setup=True)
        self.play_piece([2,8,1,44], setup=False)
        self.all_piece[46].state = self.all_piece[1].state_ban()
        self.all_piece[47].state = self.all_piece[1].state_ban()
        self.all_piece[48].state = self.all_piece[1].state_ban()
        self.all_piece[49].state = self.all_piece[1].state_ban()
        self.all_piece[50].state = self.all_piece[1].state_ban()
        return 0
    
    def setup_game_begginer02(self):
        self.setup_game_begginer01()
        self.all_piece[22].state = self.all_piece[1].state_hand()
        self.all_piece[23].state = self.all_piece[1].state_hand()
        self.all_piece[47].state = self.all_piece[1].state_hand()
        self.all_piece[48].state = self.all_piece[1].state_hand()
        self.play_piece([7,2,1,22], setup=True)
        self.play_piece([7,6,1,23], setup=True)
        self.play_piece([1,2,1,47], setup=True)
        self.play_piece([1,6,1,48], setup=True)




class Cell:
    def __init__(self, y, x, cid):
        self.x = x
        self.y = y
        self.cid = cid
        self.piece_list = []

    def push_piece(self, piece):
        self.piece_list.append(piece)
        if len(self.piece_list) > 3:
            for i in self.piece_list:
                i.location = None
                i.state = i.state_taken()
            self.piece_list = []
        return True

    def pop_piece(self):
        try:
            piece = self.piece_list.pop()
            piece.location = None
            return piece
        except:
            return None

    def take_piece(self, piece):
        ### 相手駒を取る
        ### 移動は行わない
        pID = piece.pieceID
        if pID > 25:
            ran = range(1,26)
        else:
            ran = range(25,51)

        new_list = []
        for i in range(0, len(self.piece_list)):
            if ran.count(self.piece_list[i].pieceID):
                self.piece_list[i].location = None
                #self.piece_list[i].level() = 0
                self.piece_list[i].state = self.piece_list[i].state_taken()
            else:
                new_list.append(self.piece_list[i])
        
        self.piece_list = new_list
        return True

    def change_piece(self, piece):
        ### 謀将用関数
        pass

    def active_piece(self):
        try:
            #piece = self.piece_list.pop(-1)
            piece = self.piece_list[-1]
            return piece
        except:
            return None

    def level(self):
        return len(self.piece_list)

    def active_piece(self):
        try:
            return self.piece_list[-1]
        except:
            return None


class Piece:
    def __init__(self, pieceID, imagepath=None):
        self.location = None ### [0,0,1] y,x,lv
        self.state = "hand" ### hand, board, taken, ban
        self.pieceID = pieceID
        self.imagepath = imagepath
        self.potential = {1:[], 2:[], 3:[]}

        if pieceID < 1 or pieceID > 50: 
            print("ERROR: pieceID")
            raise

        p={
             1:"帥",  2:"大",  3:"中",  4:"小",  5:"小",  6:"侍",  7:"侍",  8:"槍",  9:"槍", 10:"槍",
            11:"馬", 12:"馬", 13:"忍", 14:"忍", 15:"砦", 16:"砦", 17:"兵", 18:"兵", 19:"兵", 20:"兵", 
            21:"砲", 22:"弓", 23:"弓", 24:"筒", 25:"謀",
            26:"帥", 27:"大", 28:"中", 29:"小", 30:"小", 31:"侍", 32:"侍", 33:"槍", 34:"槍", 35:"槍",
            36:"馬", 37:"馬", 38:"忍", 39:"忍", 40:"砦", 41:"砦", 42:"兵", 43:"兵", 44:"兵", 45:"兵",
            46:"砲", 47:"弓", 48:"弓", 49:"筒", 50:"謀"
        }
        self.piecetype = p[pieceID]

        ### 元帥 =[1,26]
        if self.piecetype == "帥":
            self.potential = {1:[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]], 
                        2:[[-2,-2],[-2,0],[-2,2],[0,-2],[0,2],[2,-2],[2,0],[2,2]], 
                        3:[[-2,-2],[-2,0],[-2,2],[0,-2],[0,2],[2,-2],[2,0],[2,2]]}
        ### 大 = [2, 27]
        if self.piecetype == "大":
            self.potential = {1:[[-8,0],[-7,0],[-6,0],[-5,0],[-4,0],[-3,0],[-2,0],[-1,0],[8,0],[7,0],[6,0],[5,0],[4,0],[3,0],[2,0],[1,0],[0,-8],[0,-7],[0,-6],[0,-5],[0,-4],[0,-3],[0,-2],[0,-1],[0,8],[0,7],[0,6],[0,5],[0,4],[0,3],[0,2],[0,1],[-1,-1],[-1,1],[1,-1],[1,1]], 
                        2:[[-2,-2],[-2,2],[2,-2],[2,2]], 
                        3:[[-3,-3],[-3,3],[3,-3],[3,3]]}
        ### 中 = [3, 28]
        if self.piecetype == "中":
            self.potential = {1:[[-8,-8],[-7,-7],[-6,-6],[-5,-5],[-4,-4],[-3,-3],[-2,-2],[-1,-1],[-8,8],[-7,7],[-6,6],[-5,5],[-4,4],[-3,3],[-2,2],[-1,1],[8,-8],[7,-7],[6,-6],[5,-5],[4,-4],[3,-3],[2,-2],[1,-1],[-1,1],[8,8],[7,7],[6,6],[5,5],[4,4],[3,3],[2,2],[1,1],[-1,0],[0,-1],[1,0],[0,1]], 
                        2:[[-2,0],[0,-2],[2,0],[0,2]], 
                        3:[[-3,0],[0,-3],[3,0],[0,-3]]}
            
        ### 小 = [4, 5, 29, 30]
        if self.piecetype == "小":
            self.potential = {1:[[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,0]],
                        2:[[-2,-2],[-2,0],[-2,2],[0,-2],[0,2],[2,0]],
                        3:[[-3,-3],[-3,0],[-3,3],[0,-3],[0,3],[3,0]]}
            
        ### 侍 = [6, 7, 31, 32]
        if self.piecetype == "侍":
            self.potential = {1:[[-1,-1],[-1,0],[-1,1],[1,0]], 2:[[-2,-2],[-2,0],[-2,2],[2,0]], 3:[[-3,-3],[-3,0],[-3,3],[3,0]]}
        ### 槍 = [8, 9, 10, 33, 34, 35]
        if self.piecetype == "槍":
            self.potential = {1:[[-1,-1],[-1,0],[-1,1],[1,0],[-2,0]], 2:[[-2,-2],[-3,0],[-2,2],[2,0]], 3:[[-3,-3],[-4,0],[-3,3],[3,0]]}

        ### 馬 = [11, 12, 36, 37]
        if self.piecetype == "馬":
            self.potential = {1:[[-2,0],[-1,0],[0,-1],[0,1],[1,0],[2,0]], 2:[[-3,0],[0,-2],[0,2],[3,0]], 3:[[-4,0],[0,-3],[0,3],[4,0]]}
        ### 忍 = [13, 14, 38, 39]
        if self.piecetype == "忍":
            self.potential = {1:[[-2,-2],[-2,2],[-1,-1],[-1,1],[1,-1],[1,1],[2,-2],[2,2]], 2:[[-3,-3],[-3,3],[3,-3],[3,3]], 3:[[-4,-4],[-4,4],[4,-4],[4,4]]}
        ### 砦 = [15, 16, 40, 41]
        if self.piecetype == "砦":
            self.potential = {1:[[-1,0],[0,-1],[0,1],[1,-1],[1,1]], 2:[[-2,0],[0,-2],[0,2],[2,-2],[2,2]], 3:[[-3,0],[0,-3],[0,3],[3,-3],[3,3]]}
        ### 兵 [17,18,19,20,42,43,44,45]
        if self.piecetype == "兵":
            self.potential = {1:[[1,0],[-1,0]],2:[[2,0],[-2,0]],3:[[3,0],[-3,0]]}
        ### 砲
        if self.piecetype == "砲":
            self.potential = {1:[[-3,0],[0,-1],[0,1],[1,0]], 2:[[-4,0],[0,-2],[0,2],[2,0]], 3:[[-5,0],[0,-3],[0,3],[3,0]]}
        ### 弓
        if self.piecetype == "弓":
            self.potential = {1:[[-2,-1],[-2,0],[-2,1],[1,0]], 2:[[-3,-2],[-3,0],[-3,2],[2,0]], 3:[[-4,-3],[-4,0],[-4,3],[3,0]]}
        ### 筒
        if self.piecetype == "筒":
            self.potential = {1:[[-2,0],[1,-1],[1,1]], 2:[[-3,0],[2,-2],[2,2]], 3:[[-4,0],[3,-3],[3,3]]}
        ### 謀
        if self.piecetype == "謀":
            self.potential = {1:[[-1,-1],[-1,1],[1,0]], 2:[[-2,-2],[-2,2],[2,0]], 3:[[-3,-3],[-3,3],[3,0]]}

        ### 相手駒のみ移動範囲の向きを変える
        if self.pieceID > 25:
            for i in self.potential:
                j = []
                for k in self.potential[i]:
                    j.append(list(map(lambda x:x * -1, k)))
                self.potential[i] = j

    def state_hand(self):
        return "hand"

    def state_board(self):
        return "board"

    def state_taken(self):
        return "taken"

    def state_ban(self):
        return "ban"

    def level(self):
        try:
            return self.location[2]
        except:
            return 0
