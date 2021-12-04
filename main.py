# simple version - the ship positions cannot be changed from the user console
# no Player class
# use of array to store and access the 2 game boards throughout the game

class GameBoard(object):

    def __init__(self, width, height, battleships):
        self.width = width
        self.height = height
        self.battleships = battleships
        self.shots = []

    # Takes in a tuple that is the shot's location, not the Shot object
    def take_shot(self, shot_location):
        hit_battleship = None
        is_hit = False
        for b in self.battleships:
            # the position of the ship that was hit
            idx = b.body_index(shot_location)
            if idx != None:
                is_hit = True
                b.hits[idx] = True
                hit_battleship = b
                break
        self.shots.append(Shot(shot_location, is_hit))
        return hit_battleship

    def is_game_over(self):
        return all([b.is_destroyed() for b in self.battleships])
                                  
class Shot(object):
    
    def __init__(self, location, is_hit):
        self.location = location
        self.is_hit = is_hit

class Battleship(object):

    @staticmethod
    def build(head, length, dir):
        body = []
        x_incr = 0
        y_incr = 0
        if dir == "N":
            y_incr = -1
        elif dir == "S":
            y_incr = 1
        elif dir == "E":
            x_incr = 1
        else:
            x_incr = -1
        for i in range(length):
            body.append((head[0] + i * x_incr, head[1] + i * y_incr))
        return Battleship(body)

    def __init__(self, body):
        self.body = body
        self.hits = [False] * len(body)

    def body_index(self, location):
        try:
            return self.body.index(location)
        except ValueError:
            return None
    
    def is_destroyed(self):
        return all([sq for sq in self.hits])

def render(game_board, show_battleships=False):
    width = game_board.width
    height = game_board.height
    top_bottom = "+" + "-" * width + "+"
    print(top_bottom)
    
    # Construct empty board
    board = []
    for _ in range(width):
        board.append([None for _ in range(height)])
    
    # Show battleships only when the flag is set to True
    if show_battleships:
        # Add in battleships
        for b in game_board.battleships:
            for x, y in b.body:
                board[x][y] = "O"

    # Add in shots
    for sh in game_board.shots:
        x, y = sh.location
        if sh.is_hit:
            board[x][y] = "X"
        else:
            board[x][y] = "*"
    
    # Print the battleships
    for y in range(height):
        row = []
        for x in range(width):
            row.append(board[x][y] or " ")
        print("|" + "".join(row) + "|")

    print(top_bottom)

def announce(event_type, metadata={}):
    if event_type == "turn":
        print(metadata["player"] + "'s turn")
    elif event_type == "board":
        print(metadata["player"] + "'s board:")
    elif event_type == "win":
        print("=== " + metadata["player"] + "has won the game!!" + " ===")
    elif event_type == "miss":
        print(metadata["player"] + " MISSED!")
    elif event_type == "hit":
        print(metadata["player"] + " HIT A BATTLESHIP!")
    elif event_type == "destroyed":
        print(metadata["player"] + " DESTROYED A BATTLESHIP!")


if __name__ == "__main__":

    players = []
    players.append(input("Player 1: ")) 
    players.append(input("Player 2: ")) 

    ships1 = [
        Battleship.build((0, 0), 5, "E"),
        Battleship.build((2, 3), 4, "S"),
    ]

    ships2 = [
        Battleship.build((5, 5), 3, "E"),
        Battleship.build((2, 2), 4, "S"),
    ]

    game_boards = [
        GameBoard(10, 10, ships1),
        GameBoard(10, 10, ships2),
    ]

    # To keep track of player
    attack_idx = 0

    while True:
        defence_idx = 1 - attack_idx

        announce("turn", {"player": players[attack_idx]})
        inp = input("Coordinates for attack: ")
        x_str, y_str = inp.split(",")
        x = int(x_str)
        y = int(y_str)

        hit_battleship = game_boards[defence_idx].take_shot((x, y))
        if hit_battleship == None:
            announce("miss", {"player": players[attack_idx]})
        elif hit_battleship.is_destroyed():
            announce("destroyed", {"player": players[attack_idx]})
        else:
            announce("hit", {"player": players[attack_idx]})
        render(game_boards[defence_idx])

        if game_boards[defence_idx].is_game_over():
            announce("win", {"player": players[attack_idx]})
            exit(0)
        
        # Switch player
        attack_idx = defence_idx

# def render(width, height, shots):
#     top_bottom = "+" + "-" * width + "+"
#     print(top_bottom)

#     shots_set = set(shots)
#     for y in range(height):
#         row = []
#         for x in range(width):
#             if(x,y) in shots_set:
#                 ch = "X"
#             else:
#                 ch = " "
#             row.append(ch)
#         print("|"+ "".join(row) +"|")
#     print(top_bottom)

# def render_battleships(width, height, battleships):
#     top_bottom = "+" + "-" * width + "+"
#     print(top_bottom)

#     board = []
#     for _ in range(width):
#         board.append([None for _ in range(height)])

#     for ship in battleships:
#         for x, y in ship.body:
#             board[x][y] = "O"

#     for y in range(height):
#         row = []
#         for x in range(width):
#             row.append(board[x][y] or " ")
#         print("|" + "".join(row) + "|")

#     print(top_bottom)