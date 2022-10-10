# pylint: disable=bad-indentation
#!/usr/bin/python

# Important to note: The second player seems to have a significant advantage when testing for wins

import sys
import json
import socket

space_vec = []

# to keep track of open spaces
def init_board():
  # all spaces empty to start
  for i in range(8):
    for j in range(8):
      space_vec.append((i,j))

  # remove the first four taken spaces
  space_vec.remove((3,3))
  space_vec.remove((3,4))
  space_vec.remove((4,3))
  space_vec.remove((4,4))

# traverse the board to find the space that the opponent moved upon
def find_and_remove_opponent(board):
  for i in range(8):
    for j in range(8):
      if(board[i][j] != 0 and (i,j) in space_vec):
        space_vec.remove((i,j))

# function checks for 'sandwiched' other player tokens
def valid_opt(player, other, move, board, i , j):
  move_x = move[0]
  move_y = move[1]

  possible = 0
  count_i = i
  count_j = j

  # while within bounds and the tokens traversed are the other players', add to count and continue
  while(-1 < move_x + count_i < 8 and -1 < move_y + count_j < 8 and board[move_x + count_i][move_y + count_j] == other) :
    count_i += 1 * i
    count_j += 1 * j
    possible += 1
  
  # if the final chip is within bounds and is also a player chip, a sucessful move can be made, return point total
  if (-1 < move_x + count_i < 8 and -1 < move_y + count_j < 8 and board[move_x + count_i][move_y + count_j] == player):
    return possible

  return 0

def valid(player, move, board):
  # find player token designations
  other = 1
  if player == 1:
    other = 2
  
  move_count = 0

  # traverse in cardinal directions
  move_count += valid_opt(player, other, move, board, 1 , 0)
  move_count += valid_opt(player, other, move, board, 0 , 1)
  move_count += valid_opt(player, other, move, board, -1 , 0)
  move_count += valid_opt(player, other, move, board, 0, -1)

  # traverse diagonally
  move_count += valid_opt(player, other, move, board, 1 , 1)
  move_count += valid_opt(player, other, move, board, -1 , -1)
  move_count += valid_opt(player, other, move, board, -1 , 1)
  move_count += valid_opt(player, other, move, board, 1, -1)

  # summation of all traversals is the point total for a chip placement
  return move_count


def get_move(player, board):
  top_move = (-1,-1)
  top_count = 0

  # for each unoccupied square, find the highest possible point total per move
  for i in range(len(space_vec)):
    move_count = valid(player, (space_vec[i][0], space_vec[i][1]), board)
    if move_count:
      if move_count >= top_count:
        top_count = move_count
        top_move = (space_vec[i][0], space_vec[i][1])

  # remove the move from the vector and return
  if top_move != (-1,-1):
    space_vec.remove(top_move)
    return [top_move[0], top_move[1]]
  else:
    return []

def prepare_response(move):
  response = '{}\n'.format(move).encode()
  print('sending {!r}'.format(response))
  return response

if __name__ == "__main__":
  port = int(sys.argv[1]) if (len(sys.argv) > 1 and sys.argv[1]) else 1337
  host = sys.argv[2] if (len(sys.argv) > 2 and sys.argv[2]) else socket.gethostname()

  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    sock.connect((host, port))
    init_board()
    while True:
      data = sock.recv(1024)
      if not data:
        print('connection to server closed')
        break
      json_data = json.loads(str(data.decode('UTF-8')))
      board = json_data['board']
      maxTurnTime = json_data['maxTurnTime']
      player = json_data['player']
      print(player, maxTurnTime, board)
      find_and_remove_opponent(board)
      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
