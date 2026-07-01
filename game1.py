import curses
import random

WIDTH = 40
HEIGHT = 20

KEY_UP = curses.KEY_UP
KEY_DOWN = curses.KEY_DOWN
KEY_LEFT = curses.KEY_LEFT
KEY_RIGHT = curses.KEY_RIGHT


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    snake = [(HEIGHT // 2, WIDTH // 2 + i) for i in range(3)][::-1]
    direction = KEY_RIGHT
    food = place_food(snake)
    score = 0

    while True:
        stdscr.clear()
        draw_border(stdscr)
        draw_food(stdscr, food)
        draw_snake(stdscr, snake)
        stdscr.addstr(0, 2, f" Score: {score} ")
        stdscr.refresh()

        key = stdscr.getch()
        if key in [KEY_UP, KEY_DOWN, KEY_LEFT, KEY_RIGHT]:
            if valid_direction_change(direction, key):
                direction = key

        head = move_head(snake[0], direction)
        if collision(head, snake):
            break
        if head == food:
            snake.insert(0, head)
            score += 1
            food = place_food(snake)
        else:
            snake.insert(0, head)
            snake.pop()

        if out_of_bounds(head):
            break

    stdscr.nodelay(False)
    stdscr.addstr(HEIGHT // 2, WIDTH // 2 - 5, " GAME OVER ")
    stdscr.addstr(HEIGHT // 2 + 1, WIDTH // 2 - 8, f" Final Score: {score} ")
    stdscr.addstr(HEIGHT // 2 + 3, WIDTH // 2 - 12, " Press any key to exit ")
    stdscr.getch()


def draw_border(stdscr):
    for x in range(WIDTH + 2):
        stdscr.addch(0, x, '#')
        stdscr.addch(HEIGHT + 1, x, '#')
    for y in range(1, HEIGHT + 1):
        stdscr.addch(y, 0, '#')
        stdscr.addch(y, WIDTH + 1, '#')


def draw_snake(stdscr, snake):
    for y, x in snake:
        stdscr.addch(y + 1, x + 1, '*')


def draw_food(stdscr, food):
    y, x = food
    stdscr.addch(y + 1, x + 1, '@')


def place_food(snake):
    positions = {(y, x) for y in range(HEIGHT) for x in range(WIDTH)}
    available = list(positions - set(snake))
    return random.choice(available)


def move_head(head, direction):
    y, x = head
    if direction == KEY_UP:
        return y - 1, x
    if direction == KEY_DOWN:
        return y + 1, x
    if direction == KEY_LEFT:
        return y, x - 1
    if direction == KEY_RIGHT:
        return y, x + 1
    return head


def collision(head, snake):
    return head in snake


def out_of_bounds(head):
    y, x = head
    return y < 0 or y >= HEIGHT or x < 0 or x >= WIDTH


def valid_direction_change(current, new):
    if current == KEY_UP and new == KEY_DOWN:
        return False
    if current == KEY_DOWN and new == KEY_UP:
        return False
    if current == KEY_LEFT and new == KEY_RIGHT:
        return False
    if current == KEY_RIGHT and new == KEY_LEFT:
        return False
    return True


if __name__ == '__main__':
    curses.wrapper(main)
