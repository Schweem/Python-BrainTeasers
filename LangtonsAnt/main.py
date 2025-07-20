import os
import time

def create_map(width: int, height: int) -> list:
    tiles = []
    for i in range(height):
        tiles.append([0] * width)
    
    #print(tiles)
    return tiles
        
def render_map(current_map: list) -> None:
    for i in range(len(current_map)):
        print(current_map[i])
        
        #for j in range(len(current_map[i])):
            #print(current_map[i][j])
        
def spawn_ant(map_state):
    map_width = len(map_state)
    map_height = len(map_state[0])
    
    if map_width and map_height != 0:
        spawn_x = map_width // 2
        spawn_y = map_height // 2
        
        map_state[spawn_x][spawn_y] = 2
        #render_map(map_state)
        
    return map_state
        
def decide_next_state(map_state):
    pass
    

def main():
    #create_map(9,9)
    #render_map(create_map(9,9))
    
    width, height = 60, 60
    steps : int = 12000
    directions = [(0, 1), (-1, 0), (0, -1), (1, 0)]

    
    #print(ant_pos)
    position = create_map(width, height)
    ant_pos = [width // 2, height // 2]
    facing = 0
    #render_map(position)
    
    for i in range(steps):
        if 0 < ant_pos[0] < height and 0 <= ant_pos[1] < width:
            current_pos = position[ant_pos[0]][ant_pos[1]]
            
            if current_pos == 0:
                position[ant_pos[0]][ant_pos[1]] = 1
                facing = (facing + 1) % len(directions)
                
                #print('\n')
                #render_map(position)
            else:
                position[ant_pos[0]][ant_pos[1]] = 0
                facing = (facing - 1) % len(directions)
    
                
                #print('\n')
                #render_map(position)
                
            direction_x, direction_y = directions[facing]
            ant_pos[0] += direction_x
            ant_pos[1] += direction_y
            
        else:
            break
        
        os.system('cls' if os.name == 'nt' else 'clear')
        render_map(position)
        time.sleep(0.1)
        
        

if __name__ == "__main__":
    main()