import os

def render_board(board_state: list) -> None:
    print('_' * (len(board_state[0]) + 2))
    
    for row in range(len(board_state)):
        print('|', end="")
        
        for item in range(len(board_state[row])):
            if board_state[row][item] == 0:
                print(' ', end="")
            else:
                print('#', end="")
        print("|")
        
    print('-' * (len(board_state[0]) + 2))
    
def clear_screen() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')