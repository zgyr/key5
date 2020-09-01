char_map = [
    ['`', '#', '+', '*', '\\', '^', '~'],
    ['%', '[', '!', "'", '/', ']', '@'],
    ['&', '{', '?', '(', '"', ')', '=', '}', '<'],
    ['|', '$', '_', '-', ',', '.', ';', ':', '>'],
    ['8', '4', '3', '2', '0', '1', '5', '9', '6', '7'],
    ['Tab', 'SHFT', 'BS', ' ', 'Enter', 'DEL', 'CL'],
    [' '],
    ['h', 'o', 'e', 't', 'i'],
    ['m', 'r', 'a', 'n', 'd'],
    ['k', 'g', 'c', 's', 'l', 'f', 'p'],
    ['z', 'q', 'v', 'w', 'u', 'y', 'b', 'x', 'j']
    ]

# line number to start typing
bias_y = 6
# the index of central character
bias_x = [3, 3, 4, 4, 4, 3, 0, 2, 2, 3, 4]

max_len = max([len(''.join(i)) + len(i) + 1 for i in char_map])

pos_y = bias_y
pos_x = 0

shift_state = False
caps_state = False
cur = 0
display = ' ' * 20
last_len = 0