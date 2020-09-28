'''
positions are represented as strings!!
moves are numbers 1-9
x goes first

Each square:
_ 0
x 1
o 2
xx 3
xo 4
oo 5
xox 6
oxo 7

Each board:
double ex: 0 - none used, 1 - x used, 2 - o used, 3 - both used

Moves:
[0]-[8] for board position
[i, j] to do two moves and use double
'''



def printBoard(str):
    j = 0
    for i in range(3):
        print(str[j], '|', str[j + 1], '|', str[j + 2])
        j = j + 3

'''Board object
list of squares, each square would be smth like xox or oo
turn
double

hash the board object just like our current implementation.'''

class Board:
    def __init__(self):
        self.x_double = True
        self.o_double = True
        self.squares = ['']*9
        self.turn = 'x'
    
    def __eq__(self, other):
        return self.x_double == other.x_double and self.o_double == other.o_double and self.squares == other.squares and self.turn == other.turn

    def copy(self):
        b = Board()
        b.squares = self.squares[:]
        b.x_double = self.x_double
        b.o_double = self.o_double
        b.turn = self.turn
        return b

    def __hash__(self):
        print('hello!')
        s = [0]*12
        for i in range(9):
            curr = self.squares[i]
            if curr == '':
                s[i] = 0
            elif curr == 'x':
                s[i] = 1
            elif curr == 'o':
                s[i] = 2
            elif curr == 'xx' or curr == 'oxx':
                s[i] = 3
            elif curr == 'ox':
                s[i] = 4
            elif curr == 'oo' or curr == 'oox':
                s[i] = 5
            # elif curr == 'oxx':
            #     s[i] = 6
            # elif curr == 'oox':
            #     s[i] = 7
        s[9] = int(self.o_double)
        s[10] = int(self.x_double)
        if self.turn == 'x':
            s[11] = 0
        else:
            s[11] = 1
        return int(''.join([str(i) for i in s]))
    

def DoMove(position, move):  # returns new position
    # def findTurn(str): # RETURNS WHOSE TURN IT IS
    #     count_x = 0
    #     count_o = 0
    #     for i in range(9):
    #         if str[i] == '1' or str[i] == '4' or str[i] == '7':
    #             count_x += 1
    #         elif str[i] == '3' or str[i] == '6':
    #             count_x += 2
    #         if str[i] == '2' or str[i] == '4' or str[i] == '6':
    #             count_o += 1
    #         elif str[i] == '5' or str[i] == '7':
    #             count_o += 2
    #     if str[9] == '1' or str[9] == '3':
    #         count_x -= 1
    #     if str[9] == '2' or str[9] == '3':
    #         count_o -= 1
    #     if count_x == count_o:
    #         return 0
    #     else:
    #         return 1
    s = position.copy()
    s.squares[move[0]] = ''.join(sorted(s.turn + s.squares[move[0]]))
    if len(move) == 2:
        s.squares[move[1]] = ''.join(sorted(s.turn + s.squares[move[1]]))
    if s.turn == 'x':
        s.turn = 'o'
        if len(move) == 2:
            s.x_double = False
    else:
        s.turn = 'x' 
        if len(move) == 2:
            s.o_double = False   
    return s

def GenerateMoves(position):  # return set of moves
    moves = []
    b = Board()
    s = position.squares
    for i in range(9): # gets all single moves
        if s[i] == '' or s[i] == 'x' or s[i] == 'o' or s[i] == 'ox':
            moves.append([i])
            if (position.turn == 'x' and position.x_double) or (position.turn == 'o' and position.o_double):
                t = s[:]
                t[i] = ''.join(sorted(t[i] + position.turn))
                for j in range(i,9): # checks all potential double moves
                    if t[j] == '' or t[j] == 'x' or t[j] == 'o' or t[j] == 'ox':
                        moves.append([i,j])
    return moves


def PrimitiveValue(position):  # returns win, tie, lose, not primitive
    def checkLose(a, b, c):  # returns player if those three match, if not returns nothing
        x_owns_a = position.squares[a] == 'xx' or position.squares[a] == 'oxx'
        x_owns_b = position.squares[b] == 'xx' or position.squares[b] == 'oxx'
        x_owns_c = position.squares[c] == 'xx' or position.squares[c] == 'oxx'
        o_owns_a = position.squares[a] == 'oo' or position.squares[a] == 'oox'
        o_owns_b = position.squares[b] == 'oo' or position.squares[b] == 'oox'
        o_owns_c = position.squares[c] == 'oo' or position.squares[c] == 'oox'
        if (x_owns_a and x_owns_b and x_owns_c) or (o_owns_a and o_owns_b and o_owns_c):
            return True
        return False
    if checkLose(0, 1, 2) or checkLose(3, 4, 5) or checkLose(6, 7, 8) or checkLose(0, 3, 6) or checkLose(1, 4, 7) or checkLose(2, 5, 8) or checkLose(0, 4, 8) or checkLose(2, 4, 6):
        return "lose"
    s = position.squares
    full = (s.count('oo')+ s.count('xx')+ s.count('oxx')+ s.count('oox')) == 9  # none are blank count 
    if full:
        return "tie"
    return "not_primitive"


def symmetries(p):
    sym = ['2 1 0 5 4 3 8 7 6', '8 5 2 7 4 1 6 3 0', '0 3 6 1 4 7 2 5 8', '6 7 8 3 4 5 0 1 2', '6 3 0 7 4 1 8 5 2',
           '8 7 6 5 4 3 2 1 0', '2 5 8 1 4 7 0 3 6']
    r = []
    for s in sym:
        d = list(map(int, s.split(' ')))
        board = p[d[0]] + p[d[1]] + p[d[2]] + p[d[3]] + p[d[4]] + p[d[5]] + p[d[6]] + p[d[7]] + p[d[8]]
        if board not in r:
            r.append(board)
    return r


def FullSolve(position, WORM=False):  # returns win, tie, lose
    cache = {}  # string "xoxo_ox" --> [win/tie/lose, remote]

    # hash --> [value, remote]
    def memoizedSolve(position):
        if len(cache)%10000 == 0:
            print(len(cache))
            # print(position.squares)
        if not WORM:
            if position in cache:
                return cache[position]
        else:
            for s in symmetries(position):
                if s in cache:
                    return cache[s]
        prim = PrimitiveValue(position)
        if prim != "not_primitive":
            cache[position] = [prim, 0]
            return [prim, 0]
        else:
            results = []
            for m in GenerateMoves(position):
                newPosition = DoMove(position, m)
                m = memoizedSolve(newPosition)
                results.append([m[0], m[1]])
            solutions = [r[0] for r in results]
            remoteness = [r[1] for r in results]
            if "lose" in solutions:
                value = ["win", min([r[1] for r in results if r[0] == "lose"]) + 1]
            elif all([p == "win" for p in solutions]):
                value = ["lose", max(remoteness) + 1]
            elif 'tie' in solutions:
                value = ["tie", max(remoteness) + 1]
            cache[position] = value
            return value

    return memoizedSolve(position), cache


def Solve(position, WORM=False):
    a, b = FullSolve(position, WORM)
    return a[0]


def Cache(position, WORM=False):
    a, b = FullSolve(position, WORM)
    b[position] = a
    return b


# def test():
#     b = "_" * 9
#     x= 0
#     while x <= 9:
#         printBoard(b)
#         x = int(input())
#         b = DoMove(b, x)
#         print('primitive:', PrimitiveValue(b))
#         print('moves: ', GenerateMoves(b))
#         print('solve: ', Solve(b))

def homefun2():
    b = Board()
    c = Cache(b)
    lose, win, tie, plose, pwin, ptie = 0, 0, 0, 0, 0, 0
    for key in c:
        if c[key][0] == 'lose':
            lose += 1
        elif c[key][0] == 'win':
            win += 1
        elif c[key][0] == 'tie':
            tie += 1
    for key in c:
        if PrimitiveValue(key) == "lose":
            plose += 1
        if PrimitiveValue(key) == "win":
            pwin += 1
        if PrimitiveValue(key) == "tie":
            ptie += 1

    print('Lose: ', lose, '(' + str(plose) + ' primitive)')
    print('Win: ', win, '(' + str(pwin) + ' primitive)')
    print('Tie: ', tie, '(' + str(ptie) + ' primitive)')
    print('Total: ', len(c), '(' + str(ptie + pwin + plose) + ' primitive)')


# homefun2()


def homefun3(WORM=False):
    b = "_" * 9
    c = Cache(b, WORM)
    r = {}  # remote: [win, lose, tie, total]
    print('{:<8}{:<9}{:<9}{:<9}{:<9}'.format('Remote', 'Win', 'Lose', 'Tie', 'Total'))
    print('---------------------------------------------')
    for key in c:
        value = c[key][0]
        remote = c[key][1]
        if remote not in r:
            r[remote] = [0, 0, 0, 0]
        if value == 'win':
            r[remote][0] += 1
        elif value == 'lose':
            r[remote][1] += 1
        else:
            r[remote][2] += 1
        r[remote][3] += 1
    for key in sorted(r.keys(), reverse=True):
        print('{:<8}{:<9}{:<9}{:<9}{:<9}'.format(key, r[key][0], r[key][1], r[key][2], r[key][3]))
    print('------------------------------------------')
    win_count = len([c[k] for k in c if c[k][0] == 'win'])
    lose_count = len([c[k] for k in c if c[k][0] == 'lose'])
    tie_count = len([c[k] for k in c if c[k][0] == 'tie'])

    print('{:<8}{:<9}{:<9}{:<9}{:<9}'.format('Total:', win_count, lose_count, tie_count,
                                             win_count + lose_count + tie_count))

# b = Board()
# print(DoMove(b, [0, 8]).squares)

# homefun3(True)
# homefun3()