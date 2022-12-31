import random

shotsFired = 0

# TODO: Optimize system so that it requires fewer multi-dimensional lists.
playerShips = []
AIShips = []
playerShots = []
AIShots = []

# Initialize 2D coordinate grids
for i in range(5):
    boolList = [False]*5
    playerShips.append(boolList)
    AIShips.append(boolList)

    intList = [0]*5
    playerShots.append(intList)
    AIShots.append(intList)

def ValidatedPlayerInput():
    """
    Ensures that input coordinates are valid integers,
     are within the list boundaries, and have not been entered before.
    """
    while True:
        try:
            # Input x and y coords with an offset to account for zero-based indexing
            x = int(input("X: "))-1
            y = int(input("Y: "))-1
            
            # Must be within list boundaries
            assert (x < 5 and x >= 0) and (y < 5 and y >= 0)
            # Must not have been entered before
            assert not playerShots[x][y]
        except:
            print("Those coordinates are invalid! Try again.")
        else:
            # Stop looping if coordinates are valid
            break
    return [x, y]

def DrawVisualGrid(TargetList):
    """
    Draws a grid in the console that displays all hits,
    misses, and blanks within the input list.
    """
    for y in range(5):
        rowSymbols = ''
        for x in range(5):
            # Print 'X' for hits, 'M' for misses, and '-' for everything else
            if TargetList[x][y] == 2:
                rowSymbols += 'X'
            elif TargetList[x][y] == 1:
                rowSymbols += 'M'
            else:
                rowSymbols += '-'
        # Print each row of symbols
        print(rowSymbols)

def main():
    print("Welcome to 2-player Battleships!")

    # Store a global copy of the shotsFired variable
    global shotsFired

    # Store validated player ship coordinates
    # TODO: Add multiple ships with varying dimensions.
    print("Player 1 enter coordinates for your ship.")
    coords = ValidatedPlayerInput()
    playerShips[coords[0]][coords[1]] = True

    # Generate random AI ship coordinates
    print("Player 2 entered coordinates for their ship.")
    AIShips[random.randint(0, 4)][random.randint(0, 4)] = True

    print("Game is starting...")
    # Execute main game loop.
    while True:
        # Increase total shot count
        shotsFired += 1

        print("Player 1 enter coordinates to fire upon.")
        # Get validated player shot coordinates
        coords = ValidatedPlayerInput()
            
        # Check if the player hit a ship and draw a visual grid of previous shots
        if AIShips[coords[0]][coords[1]] == True:
            playerShots[coords[0]][coords[1]] = 2
            DrawVisualGrid(playerShots)
            print("Hit! You have sunk player 2's ship.")
            # TODO: Determine if all of the AI ships have sunk.
            print("Player 1 wins!")
            break
        else:
            playerShots[coords[0]][coords[1]] = 1
            DrawVisualGrid(playerShots)
            print("Miss... switching players.")

        # Increase total shot count
        shotsFired += 1
        
        # Generate random AI attempt coordinates
        shotX = random.randint(0, 5)
        shotY = random.randint(0, 5)
        
        # Check if the AI hit a ship and draw a visual grid of previous shots
        if playerShips[shotX][shotY]:
            AIShots[coords[0]][coords[1]] = 2
            DrawVisualGrid(AIShots)
            print("Hit! Player 2 has sunk your ship.")
            # TODO: Determine if all of the player ships have sunk.
            print("Player 2 wins!")
            break
        else:
            AIShots[coords[0]][coords[1]] = 1
            DrawVisualGrid(AIShots)
            print("Player 2 missed... switching players.")

    # Executes when the game ends
    print("Total shots fired:", shotsFired)

# Execute main() function
if __name__=="__main__":
    main()