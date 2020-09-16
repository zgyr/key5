# -*- coding: utf-8 -*-
'''
Input method concept for devices with 5 buttons.

## Usage

import key5

key5.ternary('Hello, world!')

# Use left and right arrow keys for navigation, down arrow for delete previous
character, up arrow to enter character input mode.

or

key5.roll('Hello, world!')

# And just select a character from the roll,
confirm the input with the enter key.
'''
import keyboard
import importlib


def ternary(string=''):
    '''
    Accepts a string for editing.

    |Hello, world!  [\\x00][N|0]
    ^     ^            ^   ^ ^
    |     |            |   | |
    |     Text string  |   | Ternary character code.
    |                  |   |
    |                  |   Current mode ([N]avigation / [E]dit).
    |                  |
    |                  Current character.
    |
    Cursor position.

    # Navigation mode:
        left arrow  - move cursor left
        right arrow - move cursor right
        up arrow    - switch to edit mode
        down arrow  - delete previous character
        enter       - finish editing and return the string

    # Edit mode:
        left arrow  - remove the last digit / switch to navigation mode
        up arrow    - add '0' digit
        right arrow - add '1' digit
        down arrow  - add '2' digit
        enter       - add symbol to string and switch to navigation mode
    '''
    cur = 0
    num = '0'
    mode = 'N'
    code = 0
    display = ' ' * 20
    last_len = 0

    keyboard.read_event()
    while True:
        last_len = len(display)
        print(' ' * last_len, end='\r')
        code = int(num, 3)
        code = min(code, 1114111)
        display = repr(string[:cur] +
                       '\u2588' +
                       string[cur:] +
                       '  [%s][%s|%s]' % (chr(code), mode, num))
        print(display[1:-1], end='\r')
        event = keyboard.read_event(True)
        if event.event_type != 'up':
            continue
        key = event.name
        if mode == 'E':
            if key == 'up' and num != '0':
                num += '0'
            elif key == 'right':
                num += '1'
            elif key == 'down':
                num += '2'
            elif key == 'left':
                if len(num) != 1:
                    num = num[:-1]
                else:
                    num = '0'
                    mode = 'N'
            elif key == 'enter':
                string = string[:cur] + chr(code) + string[cur:]
                num = '0'
                code = 0
                cur += 1
        else:
            if key == 'up':
                mode = 'E'
            elif key == 'down' and cur > 0:
                string = string[:cur - 1] + string[cur:]
                cur -= 1
            elif key == 'right':
                cur = min(len(string), cur + 1)
            elif key == 'left':
                cur = max(0, cur - 1)
            elif key == 'enter':
                print(' ' * last_len, end='\r')
                keyboard.send('esc')
                return string


def roll(string='', cfg='key5.layout'):
    '''
    Accepts a string for editing. Can be set the layout.

    Left/right arrows - navigate the string.
    Up/down - character selection.
    Enter - add character/complete editing.
    '''
    keyboard.read_event()
    layout = importlib.import_module(cfg)
    while True:
        c_bias = layout.bias_x[layout.pos_y]
        c_pos = layout.pos_x + c_bias
        if layout.pos_y == layout.bias_y:
            layout.display = repr(string[:layout.cur]
                                  + '\u2588'
                                  + string[layout.cur:])
            print(' ' * max(layout.last_len, layout.max_len), end='\r')
            print(layout.display[1:-1], end='\r')
            layout.last_len = len(layout.display)
        else:
            layout.display = (' '.join(layout.char_map[layout.pos_y][:c_pos]) +
                              '>' + layout.char_map[layout.pos_y][c_pos] + '<' +
                              ' '.join(layout.char_map[layout.pos_y][c_pos+1:]))
            print(' ' * layout.max_len, end='\r')
            print(layout.display.center(layout.max_len), end='\r')

        event = keyboard.read_event(True)
        if event.event_type != 'up':
            continue
        key = event.name
        if key == 'down':
            layout.pos_y = min(layout.pos_y + 1, len(layout.char_map) - 1)
            layout.pos_x = min(layout.pos_x, len(layout.char_map[layout.pos_y])
                                                 - layout.bias_x[layout.pos_y]
                                                 - 1)
            layout.pos_x = max(layout.pos_x, -layout.bias_x[layout.pos_y])
        elif key == 'up':
            layout.pos_y = max(layout.pos_y - 1, 0)

            layout.pos_x = min(layout.pos_x, len(layout.char_map[layout.pos_y])
                                                 - layout.bias_x[layout.pos_y]
                                                 - 1)
            layout.pos_x = max(layout.pos_x, -layout.bias_x[layout.pos_y])
        elif key == 'left':
            if layout.pos_y == layout.bias_y:
                layout.cur = max(0, layout.cur - 1)
            else:
                layout.pos_x = max(layout.pos_x - 1, -c_bias)
        elif key == 'right':
            if layout.pos_y == layout.bias_y:
                layout.cur = min(len(string), layout.cur + 1)
            else:
                layout.pos_x = min(layout.pos_x + 1,
                                   len(layout.char_map[layout.pos_y])-c_bias-1)
        elif key == 'enter':
            if layout.pos_y == layout.bias_y:
                return string
            char = layout.char_map[layout.pos_y][c_pos]
            layout.pos_y = layout.bias_y
            layout.pos_x = 0
            if char == 'Tab':
                char = '\t'
            elif char == 'SHFT':
                char = ''
                layout.shift_state = not layout.shift_state
            elif char == 'BS':
                char = ''
                string = string[:max(layout.cur - 1, 0)] + string[layout.cur:]
                layout.cur = max(layout.cur - 1, 0)
            elif char == 'Enter':
                char = '\n'
            elif char == 'DEL':
                char = ''
                string = string[:layout.cur] + string[layout.cur + 1:]
            elif char == 'CL':
                char = ''
                layout.caps_state = not layout.caps_state

            if len(char) == 1:
                if layout.shift_state ^ layout.caps_state:
                    char = char.upper()
                layout.shift_state = False
                string = string[:layout.cur] + char + string[layout.cur:]
                layout.cur += 1
