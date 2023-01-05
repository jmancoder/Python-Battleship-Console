import asyncio
import random

player_ships = []
ai_ships = []
player_shots = []
ai_shots = []
shots_fired = []

def validated_player_input(placing = False):
    """
    Ensures that input coordinates are valid integers,
    are within the list boundaries, and have not been entered before.
    The 'placing' parameter specifies if the coordinates are used for placing a ship.
    """
    while True:
        try:
            # Input coordinates with an offset to account for zero-based indexing
            x = int(input("X: "))-1
            y = int(input("Y: "))-1

            # Must be within list boundaries
            if(x >= 5 or x < 0) or (y >= 5 or y < 0):
                raise ValueError
            # Must not have been shot/placed before
            if placing:
                assert player_ships[x][y] == 0
            else:
                assert player_shots[x][y] == 0
        except AssertionError:
            print("You have already entered those coordinates. Try again!")
        except ValueError:
            print("Coordinates must be within the 5x5 grid. Try again!")
        except TypeError:
            print("Those coordinates are invalid. Try again!")
        else:
            # Stop looping if coordinates are valid
            break
    return [x, y]

def check_game_over(ship_list):
    """Checks if a list of ships only contains zeroes,
    which would mean that all of them are sunk.
    """
    for sublist in ship_list:
        for i in sublist:
            if i != 0:
                return False
    return True

def draw_visual_grid(hits_list):
    """
    Draws a grid in the console that displays all hits,
    misses, and blanks within the input list.
    """
    for x in range(0, 5):
        row_symbols = ''
        for y in range(0, 5):
            # Print 'X' for hits, 'M' for misses, and '-' for everything else
            if hits_list[x][y] == 2:
                row_symbols += 'X'
            elif hits_list[x][y] == 1:
                row_symbols += 'M'
            else:
                row_symbols += '-'
        # Print each row of symbols
        print(row_symbols)

def get_random_coordinates(excluded_list):
    """Generates random AI coordinates to be used for placing ships and firing.
    Like validated_player_input(), the function loops until it can find valid coordinates.
    """
    while True:
        x = random.randint(0, 4)
        y = random.randint(0, 4)
        if not excluded_list[x][y]:
            excluded_list.append((x, y))
            return [x, y]

async def main():
    # Create global variables
    global player_ships
    global ai_ships
    global player_shots
    global ai_shots
    global shots_fired

    # Initialize global variables
    shots_fired = 0

    # Store 2D lists of ship IDs
    player_ships = [[0 for i in range(5)] for j in range(5)]
    ai_ships = [[0 for i in range(5)] for j in range(5)]

    # Store a list of integers with 0 being blank, 1 being a miss, and 2 being a hit
    player_shots = [[0 for j in range(5)] for j in range(5)]
    ai_shots = [[0 for j in range(5)] for j in range(5)]

    print("Welcome to 2-player Battleships!")

    # Store three sets of validated ship coordinates
    for i in range(1, 4):
        print(f"Player 1 enter coordinates for ship {i}.")
        ship_coords = validated_player_input(True)
        player_ships[ship_coords[0]][ship_coords[1]] = i

    # Generate three sets of random ai ship coordinates
    for j in range(1, 4):
        ship_coords = get_random_coordinates(ai_ships)
        ai_ships[ship_coords[0]][ship_coords[1]] = j

    print("Player 2 entered coordinates for their ships.")
    print("Game is starting...")
    await asyncio.sleep(0.5)

    # Execute main game loop.
    while True:
        # Increase total shot count
        shots_fired += 1

        print("Player 1 enter coordinates to fire upon.")
        # Get validated player shot coordinates
        player_shot = validated_player_input()

        # Check if the player hit a ship and draw a visual grid of previous shots
        ship_id = ai_ships[player_shot[0]][player_shot[1]]
        if ship_id > 0:
            player_shots[player_shot[0]][player_shot[1]] = 2
            draw_visual_grid(player_shots)
            print("Hit!")
            if ship_id not in ai_ships:
                # If the ship sunk, then invalidate its id in the ship list
                ai_ships[player_shot[0]][player_shot[1]] = 0
                print("Player 1 sunk a ship!")
            if check_game_over(ai_ships):
                # End game if list contains only ship id 0 (all ships sunk)
                print("Player 1 wins!")
                break
        else:
            player_shots[player_shot[0]][player_shot[1]] = 1
            draw_visual_grid(player_shots)
            print("Miss... switching players.")
        
        await asyncio.sleep(0.5)

        # Increase total shot count
        shots_fired += 1

        # Generate random ai shot coordinates
        ai_shot = get_random_coordinates(ai_shots)

        # Check if the ai hit a ship and draw a visual grid of previous shots
        ship_id = player_ships[ai_shot[0]][ai_shot[1]]
        if ship_id > 0:
            ai_shots[ai_shot[0]][ai_shot[1]] = 2
            draw_visual_grid(ai_shots)
            if ship_id not in player_ships:
                # If the ship sunk, then invalidate its ID in the ship list
                player_ships[ai_shot[0]][ai_shot[1]] = 0
                print("Player 2 sunk your ship!")
            if check_game_over(player_ships):
                # End game if list contains only ship id 0 (all ships sunk)
                print("Player 2 wins!")
                break
        else:
            print("Player 2 missed... switching players.")

    # When the game ends, print total shots and delay before closing terminal
    print("Total shots fired:", shots_fired)
    await asyncio.sleep(2)

# Execute main() function
if __name__=="__main__":
    asyncio.run(main())
