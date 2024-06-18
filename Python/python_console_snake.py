from pynput import keyboard
import random
import time
import os


def main():
    direction = [-1, 0] # up
    running = True
    direction_changed = False
    
    WIDTH = 20
    HEIGHT = 20

    x_pos = int(9)
    y_pos = int(2)
    
    # Function to handle key press events
    # Optimized to only to avoid snake changing directon towards itself
    def on_press(key):
        nonlocal direction, direction_changed, running
        if direction_changed:
            return  # Ignore key press if direction already changed in this iteration

        try:
            if key.char == 'w':
                if direction != [0, 1]:  # Can only change to up if not currently going down
                    direction = [0, -1]  # Change to up
                    direction_changed = True
            elif key.char == 's':
                if direction != [0, -1]:  # Can only change to down if not currently going up
                    direction = [0, 1]   # Change to down
                    direction_changed = True
            elif key.char == 'a':
                if direction != [1, 0]:  # Can only change to left if not currently going right
                    direction = [-1, 0]  # Change to left
                    direction_changed = True
            elif key.char == 'd':
                if direction != [-1, 0]:  # Can only change to right if not currently going left
                    direction = [1, 0]   # Change to right
                    direction_changed = True
        except AttributeError:
            if key == keyboard.Key.esc:
                running = False
    
    # Start listening for key presses
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    

    def generate_fruit(tail):
        while True:
            x_fruit = random.randint(0, WIDTH - 1)
            y_fruit = random.randint(0, HEIGHT - 1)
            if [x_fruit, y_fruit] not in tail and [x_fruit, y_fruit] != [x_pos, y_pos]:
                return x_fruit, y_fruit

    score = 0
    tail = []
    x_fruit, y_fruit = generate_fruit(tail)

    # Main game loop
    while running:
        direction_changed = False

        # Move the snake
        x_pos = (x_pos + direction[0]) % WIDTH
        y_pos = (y_pos + direction[1]) % HEIGHT

        # Check if the snake eats the fruit
        if x_pos == x_fruit and y_pos == y_fruit:
            score += 1
            print(f"Score: {score}")
            x_fruit, y_fruit = generate_fruit(tail)
        else:
            # Remove the tail segment if the snake doesn't eat the fruit
            if len(tail) > score:
                tail.pop(0)

        # Check if snake collides with itself
        if [x_pos, y_pos] in tail:
            print(f"Game Over! Your score was: {score}")
            running = False
            continue

        # Add current position to the tail
        tail.append([x_pos, y_pos])

        # Update the board
        board = [[" . "] * WIDTH for _ in range(HEIGHT)]
        board[y_pos][x_pos] = "[ ]"
        board[y_fruit][x_fruit] = " ♥ "
        for t in tail:
            board[t[1]][t[0]] = "[ ]"

        # Clear the console
        os.system('cls' if os.name == 'nt' else 'clear')

        # Print the board
        for row in board:
            print("".join(row))
        print("____________________________________________________________")

        time.sleep(0.1)

    listener.stop()

if __name__ == "__main__":
    main()
