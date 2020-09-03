from math import inf as infinity
from random import choice
import platform
import time
from os import system
HUMAN = -1
AI = +1
board = [[0, 0, 0],[0, 0, 0],[0, 0, 0]]
def evaluate(state):
    if wins(state,AI):
        score=+1
    elif wins(state,HUMAN):
        score=-1
    else:
        score=0
    return score
def wins(state, player):
    win_state = [[state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],]
    if [player,player,player] in win_state:
        return True
    else:
        return False
def game_over(state):
    return wins(state, HUMAN) or wins(state,AI)
def empty_cells(state):
    cells=[]
    for x,r in enumerate(state):
        for y,c in enumerate(r):
            if c==0:
                cells.append([x,y])
    return cells
def valid_move(x, y):
    if [x,y] in empty_cells(board):
        return True
    else:
        return False
def set_move(x, y, player):
    if valid_move(x,y):
        board[x][y]=player
        return True
    else:
        return False
def minimax(state, depth, player):
    if player==AI:
        best=[-1,-1,-infinity]
    else:
        best=[-1,-1,infinity]
    if depth==0 or game_over(state):
        score=evaluate(state)
        return [-1,-1,score]
    for cell in empty_cells(state):
        x,y=cell[0],cell[1]
        state[x][y]=player
        score=minimax(state,depth-1,-player)
        state[x][y]=0
        score[0],score[1]=x,y
        if player==AI:
            if score[2]>best[2]:
                best=score
        else:
            if score[2]<best[2]:
                best=score
    return best
def clean():
    osname=platform.system().lower()
    if 'windows' in osname:
        system('cls')
    else:
        system('clear')
def render(state, c_choice, h_choice):
    chars={+1:c_choice,-1:h_choice,0:' '}
    sl='-----------------'
    print('\n'+sl)
    for r in state:
        for c in r:
            sy=chars[c]
            print(f'| {sy} |',end='')
        print('\n'+sl)
def ai_turn(c_choice, h_choice):
    depth=len(empty_cells(board))
    if depth==0 or game_over(board):
        return
    clean()
    render(board,c_choice,h_choice)
    print('AI move')
    if depth==9:
        x=choice([0,1,2])
        y=choice([0,1,2])
    else:
        move=minimax(board,depth,AI)
        x,y=move[0],move[1]
    set_move(x,y,AI)
    time.sleep(1)
def human_turn(c_choice, h_choice):
    depth=len(empty_cells(board))
    if depth==0 or game_over(board):
        return
    move=-1
    moves={1:[0,0],2:[0,1],3:[0,2],4:[1,0],5:[1,1],6:[1,2],7:[2,0],8:[2,1],9:[2,2]}
    render(board,c_choice,h_choice)
    print('Human Turn')
    while move<1 or move>9:
        try:
            move=int(input('choose a cell 1-9\n'))
            cord=moves[move]
            can=set_move(cord[0],cord[1],HUMAN)
            if not can:
                print('wrong move')
                move=-1
        except (EOFError,KeyboardInterrupt):
            print('FINISH')
            exit()
        except(KeyError,ValueError):
            print(' Wrong choice')
def main():
    clean()
    h_choice=''
    c_choice=''
    frst=''
    while h_choice !='X' and h_choice!='O':
        try:
            h_choice=input('choose X or O \n').upper()
        except (EOFError,KeyboardInterrupt):
            print('FINISH')
            exit()
        except(KeyError,ValueError):
            print(' Wrong choice')
    if h_choice=='X':
        c_choice='O'
    else:
        c_choice='X'
    clean()
    while frst!='Y' and frst!='N':
        try:
            frst=input('IF you wanna go frst enter Y else enter N\n').upper()
        except (EOFError,KeyboardInterrupt):
            print('FINISH')
            exit()
        except(KeyError,ValueError):
            print(' Wrong choice')
    while len(empty_cells(board))>0 and not game_over(board):
        if frst=='N':
            ai_turn(c_choice,h_choice)
            frst=''
        human_turn(c_choice,h_choice)
        ai_turn(c_choice,h_choice)
    if wins(board, HUMAN):
        clean()
        print(f'Human turn [{h_choice}]')
        render(board, c_choice, h_choice)
        print('YOU WIN!')
    elif wins(board, AI):
        clean()
        print(f'Computer turn [{c_choice}]')
        render(board, c_choice, h_choice)
        print('YOU LOSE!')
    else:
        clean()
        render(board, c_choice, h_choice)
        print('DRAW!')
    exit()
if __name__ == '__main__':
    main()
