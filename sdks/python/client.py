# pylint: disable=bad-indentation
#!/usr/bin/python

import sys
import json
import socket

space_vec = []

# to keep track of open spaces
def init_board(board):
    # all spaces empty to start
    for i in range(8):
      for j in range(8):
        space_vec.append({i,j})

    # remove the first four taken spaces
    space_vec.remove({3,3})
    space_vec.remove({3,4})
    space_vec.remove({4,3})
    space_vec.remove({4,4})

def valid(move, board):
  # 1 piece in some direction? -1<x<7 - > check the directions
  # search for black piece at end
  # sum the point total - return
  # 0 for invalid


def get_move(player, board):
  top_move = {-1,-1}
  top_count = 0
  for i in range(len(space_vec)):
    if valid(space_vec[i][0], space_vec[i][1]):
      move_count = points(space_vec[i][0], space_vec[i][1])
      if move_count > top_count:
        top_count = move_count
        top_move = {space_vec[i][0], space_vec[i][1]}

  if top_move != 0:
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

      move = get_move(player, board)
      response = prepare_response(move)
      sock.sendall(response)
  finally:
    sock.close()
