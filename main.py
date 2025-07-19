import time
import random
from display import render_board, clear_screen

def dead_state(height: int, width: int) -> list:
    board_state: list = []
    
    for i in range(height):
        board_state.append([0]*width)
            
    return board_state

def random_state(height: int, width:int) -> list:
    board_state: list = dead_state(height, width)
    
    for row in range (len(board_state)):
        for item in range(len(board_state[row])):
            
            random_number : float = random.random()
            board_state[row][item] = 0 if random_number >= 0.5 else 1
                
    return board_state

def next_board_state(initial_state):
    height = len(initial_state)
    width = len(initial_state[0])
    
    new_state = dead_state(width, height)
    
    adjacent_tiles = [
        (-1,-1), (-1,0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]
    
    for row in range(height):
        for item in range(width):
            current_value = initial_state[row][item]
            neighbor_count : int = 0
            
            for x,y in adjacent_tiles:
                r, c = row + x, item + y
                if (0 <= r < height and 0 <= c < width):
                    if initial_state[r][c] == 1:
                        neighbor_count += 1
                    else:
                        neighbor_count += 0
                    
            if current_value == 1: # alive
                if (neighbor_count < 2 or neighbor_count > 3):
                    new_state[row][item] = 0
                else:
                    new_state[row][item] = 1
                            
            else: # dead
                if (neighbor_count == 3):
                    new_state[row][item] = 1
        
    return new_state              
    
            
def main():        
    clear_screen()
    state = random_state(20,20)
    
    while True:
        render_board(state)
        state = next_board_state(state)
        time.sleep(0.1)
    
if __name__ == "__main__":
    main()