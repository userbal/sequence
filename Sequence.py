import random
from Cards import Cards
from Board_spaces import card_names
from colorama import Fore, Style, init
import sys
sys.path.append('F:\Sequence')
init()
#    My Global Variables
# {
Board = []
Player_1 = {'hand': [], 'color': ''}
Player_2 = {'hand': [], 'color': ''}
num_players = 0
# }

#    Creation of the Board Dictionary
# {


def create_board():
    for row in card_names:
        new_row = []
        for card in row:
            new_row.append({'name': card, 'chip': Fore.BLACK})
        Board.append(new_row)
    return Board
# }

#    Printing of the Board and its Colors
# {


def print_board():
    char = 'A'
    print('   1  2  3  4  5  6  7  8  9  10')
    print('   _____________________________')
    for row in Board:
        print(char, end='| ')
        char = chr(ord(char) + 1)
        seenW = False
        for card in row:
            color = Fore.BLACK
            if card['chip'] != Fore.BLACK:
                color = card['chip']
            if 'W' in card['name']:
                if not seenW:
                    print(color+'W ', end=' ')
                    print(Style.RESET_ALL, end='')
                    seenW = True
                else:
                    print(color+' W', end=' ')
                    print(Style.RESET_ALL, end='')
            else:
                words = card['name'].split()
                print(color + words[0][0]+words[-1][0], end=' ')
                print(Style.RESET_ALL, end='')
        print('\n')
# }

#    Shuffles the cards randomly
# {


def card_shuffle():
    shuffle = random.shuffle(Cards)
# }

#    Dealing of the cards to the players
# {


def deal():
    random_cards = random.choices(Cards, k=7)
    for card in random_cards:
        Cards.remove(card)
    return random_cards
# }
#    Drawing of the cards in order to replenish the used cards
# {


def draw(player_hand):
    random_card = random.choice(Cards)
    Cards.remove(random_card)
    player_hand.append(random_card)
# }

#    Initial input for the setup of the game
# {


def game_setup():
    while True:
        players = input("How many players want to play?: ")
        players = int(players)
        if players > -1 and players < 3:
            global num_players
            num_players = players
            break
        else:
            print("Not a valid number")
    while True:
        color = input('What color would you like to be? Green or Blue?: ')
        if 'Green' in color:
            print('You are Green!')
            Player_1['color'] = Fore.GREEN
            Player_2['color'] = Fore.BLUE
            return
        elif 'Blue' in color:
            print('You are Blue!')
            Player_1['color'] = Fore.BLUE
            Player_2['color'] = Fore.GREEN
            return
        print('Thats not a valid Color!')
# }

#    Let's the player pick where he wants to play one of his cards
#             and checks to see if it is a valid move
# {


def player_turn(playerNum):
    print('Player ' + str(playerNum) + "'s turn")
    print_board()

    if playerNum == 1:
        player = Player_1
    else:
        player = Player_2

    print('Hand:')
    print(player['hand'])

    while True:
        if num_players == 0:
            column, row = ai_turn(player)
        elif num_players == 1 and player_turn == 2:
            column, row = ai_turn(player)
        else:
            move = input(
                "Enter the coordinates for the card you'd like to place a chip on: ")
            column, row = convertMove(move)
        if isValidMove(player['hand'], row, column):
            Board[column][row]['chip'] = player['color']
            player['hand'].remove(Board[column][row]['name'])
            draw(player['hand'])
            if isGameOver(player['color']):
                print('Player ', playerNum, 'wins!')
                print_board()
                return True
            return False
        print('invalid move')
# }

#    Artificial intelligence made to take random turns for a 1 player
#       game or if you want to have 2 AI's play against eachother
# {


def ai_turn(player):
    moves = []
    for y in range(10):
        for x in range(10):
            for playerCard in player['hand']:
                if Board[y][x]['name'] == playerCard:
                    if Board[y][x]['chip'] == Fore.BLACK:
                        moves.append((y, x))

    move = random.choice(moves)
    print(move)
    return move
# }

#    Checks the validity of the move
# {


def isValidMove(hand, row, column):
    if row > 9 or row < 0 or column > 9 or column < 0:
        return False
    # make sure the space isn't occupied
    if Board[column][row]['chip'] != Fore.BLACK:
        return False

    # make sure the player has the card
    for card in hand:
        if card == Board[column][row]['name']:
            return True

    return False
# }

#    Converts the move integers that are readable for playing a card
# {


def convertMove(move):
    move = move.lower()
    column = int(move[1:])-1
    row = ord(move[0])-ord('a')
    return (row, column)
# }

#    Checks to see if either color has 5 in a row
# {


def isDiagonalSequence(color):
    # a stupid comment
    return False


def isHorizontalSequence(color):
    for row in Board:
        sequence = 0
        for card in row:
            if card['chip'] == color:
                sequence += 1
            else:
                sequence = 0

            if sequence == 5:
                print('horizontal win')
                return True

    return False


def isVerticalSequence(color):
    for x in range(10):
        sequence = 0
        for y in range(10):
            if Board[y][x]['chip'] == color:
                sequence += 1
            else:
                sequence = 0

            if sequence == 5:
                print('vertical win')
                return True
    return False
# }

#    Checks to see if the game is over
# {


def isGameOver(color):
    return isHorizontalSequence(color) or isVerticalSequence(color) or isDiagonalSequence(color)
# }

#    This function calls all the others in the correct order to play the game
# {


def main():
    create_board()
    card_shuffle()
    Player_1['hand'] = deal()
    Player_2['hand'] = deal()
    game_setup()
    # game loop
    player_num = 1
    while True:
        gameOver = player_turn(player_num)
        if gameOver:
            return
        elif player_num == 1:
            player_num = 2
        else:
            player_num = 1
# }

#    For checking current identity of Board
# {
# for space in create_board():
#    for item in space:
#        print(item)
# }


main()


# TODO diagonal
# TODO one eyed jack
# TODO two eyed jack
# TODO clean up row and column names
# TODO fix bug where sometimes ai makes infinite invalid moves
