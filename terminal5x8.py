import pygame
import sys
import time
import random
import os

# ---------------------------------------------------------
# CONFIG
# ---------------------------------------------------------
current_path = os.getcwd()
input_buffer = ""

COLS = 80
ROWS = 30
CELL_W = 5      # 4 pixels glyph + 1 pixel spacing
CELL_H = 8
SCALE = 3

SCREEN_W = COLS * CELL_W * SCALE
SCREEN_H = ROWS * CELL_H * SCALE

ENABLE_SCANLINES = True
ENABLE_BEZEL = True

BG = (0, 0, 64)
FG = (160, 160, 255)  # wordt niet meer direct gebruikt voor tekstkleur
CURSOR_COLOR = (255, 255, 255)

BEZEL_COLORS = {
    "green": (10, 30, 10),     # donkergroen plastic
    "amber": (40, 25, 10),     # warm bruin/oranje plastic
    "red": (40, 10, 10),       # donkerrood plastic
    "blue": (10, 10, 40),      # donkerblauw plastic
}

LED_BACKGROUNDS = {
    "green": (0, 20, 0),       # donkergroen CRT
    "amber": (20, 10, 0),      # warm donker amber CRT
    "red": (15, 0, 0),         # diep donkerrood
    "blue": (0, 0, 20),        # donkerblauw monitor
}

LED_COLORS = {
    "green": (0, 255, 80),
    "amber": (255, 180, 40),
    "red": (255, 60, 40),
    "blue": (80, 160, 255),
}

def set_color_mode(mode):
    global CURRENT_LED_COLOR, BG, CURRENT_BEZEL_COLOR
    CURRENT_LED_COLOR = LED_COLORS[mode]
    BG = LED_BACKGROUNDS[mode]
    CURRENT_BEZEL_COLOR = BEZEL_COLORS[mode]

set_color_mode("green")

pygame.init()
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Retro 5x8 Text Engine with Script Loader")
clock = pygame.time.Clock()

# ---------------------------------------------------------
# COMPLETE ASCII FONT (32–126)
# 4×8 glyphs, 5e pixel is spacing
# ---------------------------------------------------------
FONT = {

" ": ["0000","0000","0000","0000","0000","0000","0000","0000"],

"!": ["0010","0010","0010","0010","0010","0000","0010","0000"],
"\"": ["0101","0101","0000","0000","0000","0000","0000","0000"],
"#": ["0101","1111","0101","0101","1111","0101","0000","0000"],
"$": ["0010","0111","1010","0110","0101","1110","0010","0000"],
"%": ["1100","1101","0010","0100","1011","0011","0000","0000"],
"&": ["0110","1001","1010","0100","1010","1001","0110","0000"],
"'": ["0010","0010","0000","0000","0000","0000","0000","0000"],

"(": ["0010","0100","0100","0100","0100","0100","0010","0000"],
")": ["0100","0010","0010","0010","0010","0010","0100","0000"],
"*": ["0100","1110","0100","1110","0100","0000","0000","0000"],
"+": ["0000","0010","0010","1111","0010","0010","0000","0000"],
",": ["0000","0000","0000","0000","0000","0110","0010","0100"],
"-": ["0000","0000","0000","1111","0000","0000","0000","0000"],
".": ["0000","0000","0000","0000","0000","0110","0110","0000"],
"/": ["0001","0010","0010","0100","0100","1000","0000","0000"],

"0": ["0110","1001","1001","1111","1001","0110","0000","0000"],
"1": ["0010","0110","0010","0010","0010","0111","0000","0000"],
"2": ["0110","1001","0001","0010","0100","1111","0000","0000"],
"3": ["1110","0001","0110","0001","0001","1110","0000","0000"],
"4": ["0001","0011","0101","1001","1111","0001","0000","0000"],
"5": ["1111","1000","1110","0001","0001","1110","0000","0000"],
"6": ["0110","1000","1110","1001","1001","0110","0000","0000"],
"7": ["1111","0001","0010","0100","0100","0100","0000","0000"],
"8": ["0110","1001","0110","1001","1001","0110","0000","0000"],
"9": ["0110","1001","1001","0111","0001","0110","0000","0000"],

":": ["0000","0110","0110","0000","0000","0110","0110","0000"],
";": ["0000","0110","0110","0000","0000","0110","0010","0100"],
"<": ["0001","0010","0100","1000","0100","0010","0001","0000"],
"=": ["0000","1111","0000","1111","0000","0000","0000","0000"],
">": ["1000","0100","0010","0001","0010","0100","1000","0000"],
"?": ["0110","1001","0001","0010","0010","0000","0010","0000"],
"@": ["0110","1001","1011","1011","1000","0111","0000","0000"],

"A": ["0110","1001","1001","1111","1001","1001","0000","0000"],
"B": ["1110","1001","1110","1001","1001","1110","0000","0000"],
"C": ["0111","1000","1000","1000","1000","0111","0000","0000"],
"D": ["1110","1001","1001","1001","1001","1110","0000","0000"],
"E": ["1111","1000","1110","1000","1000","1111","0000","0000"],
"F": ["1111","1000","1110","1000","1000","1000","0000","0000"],
"G": ["0111","1000","1000","1011","1001","0111","0000","0000"],
"H": ["1001","1001","1111","1001","1001","1001","0000","0000"],
"I": ["0111","0010","0010","0010","0010","0111","0000","0000"],
"J": ["0001","0001","0001","1001","1001","0110","0000","0000"],
"K": ["1001","1010","1100","1010","1001","1001","0000","0000"],
"L": ["1000","1000","1000","1000","1000","1111","0000","0000"],
"M": ["1001","1111","1111","1001","1001","1001","0000","0000"],
"N": ["1001","1101","1011","1001","1001","1001","0000","0000"],
"O": ["0110","1001","1001","1001","1001","0110","0000","0000"],
"P": ["1110","1001","1110","1000","1000","1000","0000","0000"],
"Q": ["0110","1001","1001","1001","1011","0111","0000","0000"],
"R": ["1110","1001","1110","1010","1001","1001","0000","0000"],
"S": ["0111","1000","0110","0001","0001","1110","0000","0000"],
"T": ["1111","0010","0010","0010","0010","0010","0000","0000"],
"U": ["1001","1001","1001","1001","1001","0110","0000","0000"],
"V": ["1001","1001","1001","1001","0110","0010","0000","0000"],
"W": ["1001","1001","1111","1111","1001","1001","0000","0000"],
"X": ["1001","0110","0010","0010","0110","1001","0000","0000"],
"Y": ["1001","1001","0110","0010","0010","0010","0000","0000"],
"Z": ["1111","0001","0010","0100","1000","1111","0000","0000"],

"[": ["0110","0100","0100","0100","0100","0100","0110","0000"],
"\\": ["1000","0100","0100","0010","0010","0001","0000","0000"],
"]": ["0110","0010","0010","0010","0010","0010","0110","0000"],
"^": ["0010","0101","1000","0000","0000","0000","0000","0000"],
"_": ["0000","0000","0000","0000","0000","0000","1111","0000"],
"`": ["0100","0010","0000","0000","0000","0000","0000","0000"],

"a": ["0000","0110","0001","0111","1001","0111","0000","0000"],
"b": ["1000","1110","1001","1001","1001","1110","0000","0000"],
"c": ["0000","0111","1000","1000","1000","0111","0000","0000"],
"d": ["0001","0111","1001","1001","1001","0111","0000","0000"],
"e": ["0000","0110","1001","1111","1000","0111","0000","0000"],
"f": ["0011","0100","1110","0100","0100","0100","0000","0000"],
"g": ["0000","0111","1001","1001","0111","0001","0110","0000"],
"h": ["1000","1110","1001","1001","1001","1001","0000","0000"],
"i": ["0010","0000","0110","0010","0010","0111","0000","0000"],
"j": ["0001","0000","0011","0001","0001","1001","0110","0000"],
"k": ["1000","1010","1100","1010","1001","1001","0000","0000"],
"l": ["0110","0010","0010","0010","0010","0111","0000","0000"],
"m": ["0000","1101","1111","1001","1001","1001","0000","0000"],
"n": ["0000","1110","1001","1001","1001","1001","0000","0000"],
"o": ["0000","0110","1001","1001","1001","0110","0000","0000"],
"p": ["0000","1110","1001","1001","1110","1000","1000","0000"],
"q": ["0000","0111","1001","1001","0111","0001","0001","0000"],
"r": ["0000","1011","1100","1000","1000","1000","0000","0000"],
"s": ["0000","0111","1000","0110","0001","1110","0000","0000"],
"t": ["0100","0100","1110","0100","0100","0011","0000","0000"],
"u": ["0000","1001","1001","1001","1001","0111","0000","0000"],
"v": ["0000","1001","1001","1001","0110","0010","0000","0000"],
"w": ["0000","1001","1001","1111","1111","1001","0000","0000"],
"x": ["0000","1001","0110","0010","0110","1001","0000","0000"],
"y": ["0000","1001","1001","0111","0001","0110","0000","0000"],
"z": ["0000","1111","0010","0100","1000","1111","0000","0000"],

"{": ["0011","0010","0010","0110","0010","0010","0011","0000"],
"|": ["0010","0010","0010","0010","0010","0010","0010","0000"],
"}": ["1100","0100","0100","0110","0100","0100","1100","0000"],
"~": ["0000","0000","0101","1010","0000","0000","0000","0000"],

}

# ---------------------------------------------------------
# BUFFER + CURSOR
# ---------------------------------------------------------
buffer = [[" " for _ in range(COLS)] for _ in range(ROWS)]
cursor_x = 0
cursor_y = 0
cursor_visible = True
last_blink = time.time()
script_loaded = False

# ---------------------------------------------------------
# DRAW
# ---------------------------------------------------------
def vary_brightness(color, amount=20):
    r, g, b = color
    delta = random.randint(-amount, amount)
    r = max(0, min(255, r + delta))
    g = max(0, min(255, g + delta))
    b = max(0, min(255, b + delta))
    return (r, g, b)

def draw_pixel(x, y, color):
    base_x = x * SCALE
    base_y = y * SCALE

    dot_size = int(SCALE * 0.9)
    if dot_size < 1:
        dot_size = 1

    offset = (SCALE - dot_size) // 2
    cx = base_x + offset + dot_size // 2
    cy = base_y + offset + dot_size // 2

    # 1. Glow
    glow_size = int(dot_size * 2.2)
    glow_color = (*color, 40)  # alpha 40

    glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
    pygame.draw.circle(glow_surface, glow_color, (glow_size // 2, glow_size // 2), glow_size // 2)
    screen.blit(glow_surface, (cx - glow_size // 2, cy - glow_size // 2))

    # 2. Donkere uit-pixel
    off_color = (8, 8, 16)
    rect = (base_x + offset, base_y + offset, dot_size, dot_size)
    pygame.draw.rect(screen, off_color, rect, border_radius=dot_size // 2)

    # 3. Aan-pixel met variatie
    if color != BG:
        varied = vary_brightness(color, amount=18)
        pygame.draw.rect(screen, varied, rect, border_radius=dot_size // 2)


def draw_char(ch, x, y):
    if ch not in FONT:
        ch = " "
    bitmap = FONT[ch]
    for row in range(8):
        for col in range(4):
            if bitmap[row][col] == "1":
                draw_pixel(x + col, y + row, CURRENT_LED_COLOR)

def draw_cursor():
    if cursor_visible:
        for row in range(8):
            draw_pixel(cursor_x * CELL_W, cursor_y * CELL_H + row, CURSOR_COLOR)

# ---------------------------------------------------------
# SCROLLING + TEXT
# ---------------------------------------------------------
def scroll_buffer():
    global buffer, cursor_y
    for r in range(ROWS - 1):
        buffer[r] = buffer[r + 1][:]
    buffer[ROWS - 1] = [" " for _ in range(COLS)]
    cursor_y = ROWS - 1

def write_shell_text(text):
    global cursor_x, cursor_y, buffer

    for ch in text:
        if ch == "\n":
            cursor_x = 0
            cursor_y += 1
        else:
            buffer[cursor_y][cursor_x] = ch if ch in FONT else " "
            cursor_x += 1

        if cursor_x >= COLS:
            cursor_x = 0
            cursor_y += 1

        if cursor_y >= ROWS:
            scroll_buffer()
            cursor_y = ROWS - 1

def write_text_with_scrolling(text):
    global cursor_x, cursor_y, buffer

    for ch in text:
        if ch == "\n":
            cursor_x = 0
            cursor_y += 1
        else:
            buffer[cursor_y][cursor_x] = ch if ch in FONT else " "
            cursor_x += 1

        if cursor_x >= COLS:
            cursor_x = 0
            cursor_y += 1

        if cursor_y >= ROWS:
            prompt = "-- Press ENTER to continue --"
            for i, c in enumerate(prompt):
                if i < COLS:
                    buffer[ROWS - 1][i] = c

            redraw_screen()

            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        waiting = False

            buffer[ROWS - 1] = [" " for _ in range(COLS)]
            scroll_buffer()
            cursor_x = 0
            cursor_y = ROWS - 1

def load_script(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                write_text_with_scrolling(line)
    except FileNotFoundError:
        write_text_with_scrolling(f"ERROR: Script '{filename}' not found.\n")

# ---------------------------------------------------------
# REDRAW
# ---------------------------------------------------------
def redraw_screen():
    screen.fill(BG)

    for r in range(ROWS):
        for c in range(COLS):
            draw_char(buffer[r][c], c * CELL_W, r * CELL_H)

    draw_cursor()

    # --- scanlines toevoegen ---
    draw_scanlines()

    pygame.display.flip()

def draw_scanlines():
    if not ENABLE_SCANLINES:
        return

    line_color = (0, 0, 0, 40)  # transparante zwarte scanline
    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)

    # elke 2 pixels een scanline
    for y in range(0, SCREEN_H, 2):
        pygame.draw.line(overlay, line_color, (0, y), (SCREEN_W, y))

    screen.blit(overlay, (0, 0))

# ---------------------------------------------------------
# SHELL
# ---------------------------------------------------------
def handle_command(cmd):
    global current_path

    parts = cmd.strip().split()
    if len(parts) == 0:
        return

    command = parts[0]

    # --- ls ---
    if command == "ls":
        try:
            items = os.listdir(current_path)
            for item in items:
                write_shell_text(item + "\n")
        except Exception as e:
            write_shell_text(f"Error: {e}\n")

    # --- pwd ---
    elif command == "pwd":
        write_shell_text(current_path + "\n")

    # --- cd ---
    elif command == "cd":
        if len(parts) < 2:
            write_shell_text("Usage: cd <directory>\n")
        else:
            new_path = os.path.join(current_path, parts[1])
            if os.path.isdir(new_path):
                current_path = os.path.abspath(new_path)
                write_shell_text(f"Changed directory to {current_path}\n")
            else:
                write_shell_text("Directory not found.\n")

    # --- cat ---
    elif command == "cat":
        if len(parts) < 2:
            write_shell_text("Usage: cat <file>\n")
        else:
            file_path = os.path.join(current_path, parts[1])
            if os.path.isfile(file_path):
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        for line in f:
                            write_shell_text(line)
                except Exception as e:
                    write_shell_text(f"Error: {e}\n")
            else:
                write_shell_text("File not found.\n")

    # --- help ---
    elif command == "help":
        write_shell_text(
            "Available commands:\n"
            "  ls        - list directory\n"
            "  pwd       - show current directory\n"
            "  cd <dir>  - change directory\n"
            "  cat <file>- show file contents\n"
            "  help      - show this help\n"
        )

    # --- unknown ---
    else:
        write_shell_text(f"Unknown command: {command}\n")

# ---------------------------------------------------------
# MAIN LOOP
# ---------------------------------------------------------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if len(input_buffer) > 0:
                    input_buffer = input_buffer[:-1]
                    if cursor_x > 0:
                        cursor_x -= 1
                        buffer[cursor_y][cursor_x] = " "
                continue

            # ENTER = command uitvoeren
            if event.key == pygame.K_RETURN:
                write_shell_text("\n")
                handle_command(input_buffer)
                input_buffer = ""
                cursor_x = 0
                cursor_y += 1
                if cursor_y >= ROWS:
                    scroll_buffer()
                continue

            # normale tekens
            ch = event.unicode
            if ch in FONT:
                input_buffer += ch
                buffer[cursor_y][cursor_x] = ch
                cursor_x += 1
                if cursor_x >= COLS:
                    cursor_x = 0
                    cursor_y += 1
                    if cursor_y >= ROWS:
                        scroll_buffer()

    if not script_loaded:
        example_text = (
            "You awaken in a dimly lit cavern.\n"
            "Moist air clings to your skin as distant droplets echo in the dark.\n"
            "A narrow passage leads north. A crumbling stone archway lies to the east.\n"
            "\n"
            "Your adventure begins...\n\n"
        )
        write_text_with_scrolling(example_text)
        load_script("story.txt")
        script_loaded = True

    if time.time() - last_blink > 0.5:
        cursor_visible = not cursor_visible
        last_blink = time.time()

    redraw_screen()
    clock.tick(60)
