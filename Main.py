from asyncio import sleep
import random

def ValidatedPlayerInput():
    """
    Ensures that input coordinates are valid integers,
     are within the list boundaries, and have not been entered before.
    """
    while True:
        try:
            # Input playerShot with an offset to account for zero-based indexing
            x = int(input("X: "))-1
            y = int(input("Y: "))-1
            
            # Must be within list boundaries
            assert (x < 5 and x >= 0) and (y < 5 and y >= 0)
            # Must not have been entered before
            assert not playerShots[x][y]
        except:
            print("Those coordinates are invalid or already entered. Try again!")
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
    # Create global variables
    global playerShips
    global AIShips
    global playerShots
    global AIShots
    global shotsFired

    # Initialize global variables
    shotsFired = 0
    for i in range(5):
        # TODO: Optimize system so that it requires fewer multi-dimensional lists.
        playerShips = [[False for j in range(5)] for j in range(5)]
        AIShips = [[False for j in range(5)] for j in range(5)]
        playerShots = [[0 for j in range(5)] for j in range(5)]
        AIShots = [[0 for j in range(5)] for j in range(5)]

    print("Welcome to 2-player Battleships!")

    # Store validated player ship coordinates
    # TODO: Add multiple ships with varying dimensions.
    print("Player 1 enter coordinates for your ship.")
    playerShip = ValidatedPlayerInput()
    playerShips[playerShip[0]][playerShip[1]] = True

    # Generate random AI ship coordinates
    sleep(0.5)
    print("Player 2 entered coordinates for their ship.")
    AIShips[random.randint(0, 4)][random.randint(0, 4)] = True

    print("Game is starting...")
    
    # Execute main game loop.
    while True:
        # Increase total shot count
        shotsFired += 1

        print("Player 1 enter coordinates to fire upon.")
        # Get validated player shot coordinates
        playerShot = ValidatedPlayerInput()
            
        # Check if the player hit a ship and draw a visual grid of previous shots
        if AIShips[playerShot[0]][playerShot[1]]:
            playerShots[playerShot[0]][playerShot[1]] = 2
            DrawVisualGrid(playerShots)
            print("Hit! You have sunk player 2's ship.")
            # TODO: Determine if all of the AI ships have sunk.
            print("Player 1 wins!")
            break
        else:
            playerShots[playerShot[0]][playerShot[1]] = 1
            DrawVisualGrid(playerShots)
            print("Miss... switching players.")

        # Increase total shot count
        shotsFired += 1
        
        # Generate random AI attempt coordinates
        sleep(1)
        AIShot = [random.randint(0, 4), random.randint(0, 4)]
        
        # Check if the AI hit a ship and draw a visual grid of previous shots
        if playerShips[AIShot[0]][AIShot[1]]:
            AIShots[AIShot[0]][AIShot[1]] = 2
            DrawVisualGrid(AIShots)
            print("Hit! Player 2 has sunk your ship.")
            # TODO: Determine if all of the player ships have sunk.
            print("Player 2 wins!")
            break
        else:
            AIShots[AIShot[0]][AIShot[1]] = 1
            DrawVisualGrid(AIShots)
            print("Player 2 missed... switching players.")

    # Executes when the game ends
    print("Total shots fired:", shotsFired)
    sleep(2)

# Execute main() function
if __name__=="__main__":
    main()