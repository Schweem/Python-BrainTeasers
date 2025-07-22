def main():
    draw_triangle(5)

    print('\n')

    draw_pyramid(6)

    print('\n')

    draw_square(5)

def draw_triangle(height : int):
    for i in range(1, height):
        print('*' * (i))

def draw_pyramid(height : int):
    count = height // 2
    for i in range(1, height):
        if (i % 2) != 0:
            print(' ' * count + '*' * i + ' ' * count)
            count -= 1

def draw_square(height : int):
    for i in range(1, height + 1):
        print('*' * height)

if __name__ == "__main__":
    main()
