from asyncio import sleep
import random

player_ships = []
ai_ships = []
player_shots = []
ai_shots = []
shots_fired = []

def validated_player_input():
    """
    Ensures that input coordinates are valid integers,
     are within the list boundaries, and have not been entered before.
    """
    while True:
        try:
            # Input _s with an offset to account for zero-based indexing
            x = int(input("X: "))-1
            y = int(input("Y: "))-1

            # Must be within list boundaries
            assert (x < 5 and x >= 0) and (y < 5 and y >= 0)
            # Must not have been entered before
            assert not player_shots[x][y]
        except TypeError:
            print("Those coordinates are invalid. Try again!")
        except AssertionError:
            print("You have already entered those coordinates. Try again!")
        else:
            # Stop looping if coordinates are valid
            break
    return [x, y]

def draw_visual_grid(target_list):
    """
    Draws a grid in the console that displays all hits,
    misses, and blanks within the input list.
    """
    for y in range(5):
        row_symbols = ''
        for x in range(5):
            # Print 'X' for hits, 'M' for misses, and '-' for everything else
            if target_list[x][y] == 2:
                row_symbols += 'X'
            elif target_list[x][y] == 1:
                row_symbols += 'M'
            else:
                row_symbols += '-'
        # Print each row of symbols
        print(row_symbols)

def main():
    # Create global variables
    global player_ships
    global ai_ships
    global player_shots
    global ai_shots
    global shots_fired

    # Initialize global variables
    shots_fired = 0
    for i in range(5):
        # TODO: Optimize system so that it requires fewer multi-dimensional lists.
        player_ships = [[False for j in range(5)] for j in range(5)]
        ai_ships = [[False for j in range(5)] for j in range(5)]
        _s = [[0 for j in range(5)] for j in range(5)]
        ai_shots = [[0 for j in range(5)] for j in range(5)]

    print("Welcome to 2-player Battleships!")

    # Store validated player ship coordinates
    # TODO: Add multiple ships with varying dimensions.
    print("Player 1 enter coordinates for your ship.")
    player_ship = validated_player_input()
    player_ships[player_ship[0]][player_ship[1]] = True

    # Generate random ai ship coordinates
    sleep(0.5)
    print("Player 2 entered coordinates for their ship.")
    ai_ships[random.randint(0, 4)][random.randint(0, 4)] = True

    print("Game is starting...")

    # Execute main game loop.
    while True:
        # Increase total shot count
        shots_fired += 1

        print("Player 1 enter coordinates to fire upon.")
        # Get validated player shot coordinates
        player_shot = validated_player_input()

        # Check if the player hit a ship and draw a visual grid of previous shots
        if ai_ships[_s[0]][_s[1]]:
            player_shots[player_shot[0]][player_shot[1]] = 2
            draw_visual_grid(player_shots)
            print("Hit! You have sunk player 2's ship.")
            # TODO: Determine if all of the ai ships have sunk.
            print("Player 1 wins!")
            break
        else:
            player_shots[player_shot[0]][player_shot[1]] = 1
            draw_visual_grid(player_shots)
            print("Miss... switching players.")

        # Increase total shot count
        shots_fired += 1

        # Generate random ai attempt coordinates
        sleep(1)
        ai_shot = [random.randint(0, 4), random.randint(0, 4)]

        # Check if the ai hit a ship and draw a visual grid of previous shots
        if player_ships[ai_shot[0]][ai_shot[1]]:
            ai_shots[ai_shot[0]][ai_shot[1]] = 2
            draw_visual_grid(ai_shots)
            print("Hit! Player 2 has sunk your ship.")
            # TODO: Determine if all of the player ships have sunk.
            print("Player 2 wins!")
            break
        else:
            ai_shots[ai_shot[0]][ai_shot[1]] = 1
            draw_visual_grid(ai_shots)
            print("Player 2 missed... switching players.")

    # Executes when the game ends
    print("Total shots fired:", shots_fired)
    sleep(2)

# Execute main() function
if __name__=="__main__":
    main()
