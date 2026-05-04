import os, sys, time, random, msvcrt, ctypes

def enable_ansi():
    if sys.platform == "win32":
        kernel32 = ctypes.windll.kernel32
        kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
enable_ansi()

WIDTH, HEIGHT = 30, 15
INIT_SPEED = 0.1

DIRECTIONS = {
    b'w': (-1,0), b's': (1,0), b'a': (0,-1), b'd': (0,1),
    b'W': (-1,0), b'S': (1,0), b'A': (0,-1), b'D': (0,1),
}
EXT_KEYS = {72:(-1,0), 80:(1,0), 75:(0,-1), 77:(0,1)}

def clear_screen():
    print('\033[2J\033[H', end='')

def draw_border():
    print('\033[37m+' + '-' * WIDTH + '+')
    for _ in range(HEIGHT):
        print('|' + ' ' * WIDTH + '|')
    print('+' + '-' * WIDTH + '+\033[0m')

def move_cursor(row, col):
    print(f'\033[{row+2};{col+2}H', end='')

def draw_pixel(row, col, char, color='37'):
    move_cursor(row, col)
    print(f'\033[{color}m{char}\033[0m', end='')

def game_over(score):
    clear_screen()
    print('\033[31m')
    print('=' * 34)
    print('         GAME OVER         ')
    print(f'        Your Score: {score}')
    print('=' * 34)
    print('\033[0m')
    print('Press any key to exit...')
    while msvcrt.kbhit(): msvcrt.getch()
    msvcrt.getch()

def main():
    clear_screen()
    print('Snake Game - Loading...')
    time.sleep(0.5)

    snake = [(HEIGHT//2, WIDTH//2)]
    direction = (0, 1)
    score = 0
    speed = INIT_SPEED

    def place_food():
        while True:
            food = (random.randint(0, HEIGHT-1), random.randint(0, WIDTH-1))
            if food not in snake:
                return food
    food = place_food()

    while True:
        while msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch in DIRECTIONS:
                new_dir = DIRECTIONS[ch]
                if (new_dir[0]+direction[0], new_dir[1]+direction[1]) != (0,0):
                    direction = new_dir
            elif ch == b'\xe0' or ch == b'\x00':
                code = ord(msvcrt.getch())
                if code in EXT_KEYS:
                    new_dir = EXT_KEYS[code]
                    if (new_dir[0]+direction[0], new_dir[1]+direction[1]) != (0,0):
                        direction = new_dir

        head_r, head_c = snake[-1]
        new_head = (head_r+direction[0], head_c+direction[1])

        if (new_head[0]<0 or new_head[0]>=HEIGHT or 
            new_head[1]<0 or new_head[1]>=WIDTH or 
            new_head in snake):
            break

        snake.append(new_head)
        if new_head == food:
            score += 10
            food = place_food()
            speed = max(0.03, INIT_SPEED - score*0.002)
        else:
            snake.pop(0)

        clear_screen()
        print(f'\033[36m  Score: {score}   Speed: {speed:.2f}s\033[0m')
        draw_border()
        draw_pixel(food[0], food[1], 'O', '31')
        for i, (r,c) in enumerate(snake):
            char = '#'
            color = '32' if i == len(snake)-1 else '92'
            draw_pixel(r, c, char, color)
        move_cursor(HEIGHT, 0)
        sys.stdout.flush()
        time.sleep(speed)

    game_over(score)

if __name__ == '__main__':
    main()