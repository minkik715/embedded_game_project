import time
import math
import random
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

#color
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0 )
# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
disp.image(image)

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0, 0, width, height), outline=0, fill=0)
button_outline = "#FFFFFF"
button_fill = "#FF00FF"
basic_color = "#002aff"
fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
# SET
x1 = random.randint(0, 180)
size = random.randint(20, 60)
x2 = x1 + size
y1 = 0
y2 = y1 + size
B_color = "#ff0011"
I_color = basic_color
A_color = basic_color
E_color = basic_color
tmp = 100
color_list = [B_color, I_color, A_color, E_color]


def random_location():
    return random.randint(1, 4)

def set_up_user_loc(ball_x1,ball_x2,ball_y1,ball_y2):
    return ball_x1, ball_x2, ball_y1, ball_y2
def remove_screen():
    draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
    disp.image(image)


def game_end(score):
    draw.text((20, 20), "Game Over", font=fnt, fill=basic_color)
    draw.text((20, 60), "Score:", font=fnt, fill=basic_color)
    draw.text((150, 60), str(score), font=fnt, fill=basic_color)
    disp.image(image)
    time.sleep(3)
    remove_screen()


def crash_ball(x1, x2, y1, y2, ball_x1, ball_x2, ball_y1, ball_y2, score):
    cent_x = (x1+x2)/2
    cent_y = (y1+y2)/2
    ball_cent_x = (ball_x1 + ball_x2)/2
    ball_cent_y = (ball_y1 + ball_x2)/2
    x_r = cent_x - x1
    ball_x_r = ball_cent_x - ball_x1
    length = math.sqrt(((cent_x-ball_cent_x)**2+(cent_y-ball_cent_y)**2))
    if(length <= x_r+ball_x_r):
        time.sleep(1)
        return score	
    else:
        return -1


def falling_ball_mv(x1, x2, y1, y2, speed, loc, score):
    if loc == 1 and y1 <= 250:
        y1 = y1 + speed
        y2 = y2 + speed
    elif loc == 2 and x1 <= 250:
        x1 = x1 + speed
        x2 = x2 + speed
    elif loc == 3 and y2 >= -10:
        y1 = y1 - speed
        y2 = y2 - speed
    elif loc == 4 and x2 >= -10:
        x1 = x1 - speed
        x2 = x2 - speed
    else:
        score += 10
        loc = random_location()
        if loc == 1:
            size = random.randint(20, 40)
            y1 = 0
            y2 = y1 + size
            x1 = random.randint(0, 200)
            x2 = x1 + size
        if loc == 2:
            size = random.randint(20, 40)
            y1 = random.randint(0, 200)
            y2 = y1 + size
            x1 = 0
            x2 = x1 + size
        if loc == 3:
            size = random.randint(20, 40)
            y1 = 240 - size
            y2 = 240
            x1 = random.randint(0, 200)
            x2 = x1 + size
        if loc == 4:
            size = random.randint(20, 40)
            y1 = random.randint(0, 200)
            y2 = y1 + size
            x1 = 240 - size
            x2 = 240
    return x1, x2, y1, y2, loc, score


def control_userball(ball_x1, ball_x2, ball_y1, ball_y2, speed):
    if not button_L.value:
        ball_x1 -= speed
        ball_x2 -= speed
    if not button_R.value:
        ball_x1 += speed
        ball_x2 += speed
    if not button_U.value:
        ball_y1 -= speed
        ball_y2 -= speed
    if not button_D.value:
        ball_y1 += speed
        ball_y2 += speed
    return ball_x1, ball_x2, ball_y1, ball_y2


def game_begin_inter(x1, x2, y1, y2, speed, name):
    ball_x1,ball_x2,ball_y1,ball_y2 = set_up_user_loc(110, 130, 210, 230)

    draw.text((30, 50), name, font=fnt, fill=basic_color)
    disp.image(image)
    time.sleep(2)
    score = 0
    while (True):
        rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
        draw.ellipse((x1, y1, x2, y2), outline=button_outline, fill=rcolor)
        draw.ellipse((ball_x1, ball_y1, ball_x2, ball_y2), outline=button_outline, fill=basic_color)
        disp.image(image)
        check = crash_ball(x1, x2, y1, y1, ball_x1, ball_x2, ball_y1, ball_y2, score)
        if (check >= 0):
            return check
        ball_x1, ball_x2, ball_y1, ball_y2 = control_userball(ball_x1, ball_x2, ball_y1, ball_y2, 10)
        if y1 <= 250:
            y1 = y1 + speed
            y2 = y2 + speed
        else:
            score += 10
            size = random.randint(20, 40)
            y1 = 0
            y2 = y1 + size
            x1 = random.randint(0, 200)
            x2 = x1 + size
        remove_screen()
        time.sleep(0.01)


def game_advance(x1, x2, y1, y2, speed, name):

    ball_x1, ball_x2, ball_y1, ball_y2 = set_up_user_loc(110, 130, 210, 230)

    draw.text((30, 50), name, font=fnt, fill=basic_color)
    disp.image(image)
    time.sleep(2)
    score = 0
    loc = 1
    while (True):
        rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
        draw.ellipse((x1, y1, x2, y2), outline=button_outline, fill=rcolor)
        draw.ellipse((ball_x1, ball_y1, ball_x2, ball_y2), outline=button_outline, fill=basic_color)
        disp.image(image)
        check = crash_ball(x1, x2, y1, y1, ball_x1, ball_x2, ball_y1, ball_y2, score)
        if check >= 0:
            return check
        ball_x1, ball_x2, ball_y1, ball_y2 = control_userball(ball_x1, ball_x2, ball_y1, ball_y2, 10)
        x1, x2, y1, y2, loc, score = falling_ball_mv(x1, x2, y1, y2, speed, loc, score)
        remove_screen()
        time.sleep(0.01)


def game_expert(x1, x2, y1, y2, speed, name):
    ball_x1, ball_x2, ball_y1, ball_y2 = set_up_user_loc(110, 130, 210, 230)
    x3,x4,y3,y4 = set_up_user_loc(0, 40, 0, 40)
    draw.text((30, 50), name, font=fnt, fill=basic_color)
    disp.image(image)
    time.sleep(2)
    score = 0
    loc = 1
    loc2 = 1
    while (True):
        rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
        draw.ellipse((x1, y1, x2, y2), outline=button_outline, fill=rcolor)
        draw.ellipse((x3, y3, x4, y4), outline=button_outline, fill=rcolor)
        draw.ellipse((ball_x1, ball_y1, ball_x2, ball_y2), outline=button_outline, fill=basic_color)
        disp.image(image)
        check = crash_ball(x1, x2, y1, y1, ball_x1, ball_x2, ball_y1, ball_y2, score)
        check2 = crash_ball(x3, x4, y3, y4, ball_x1, ball_x2, ball_y1, ball_y2, score)

        if (check >= 0):
            return check
        if (check2 >= 0):
            return check2
        ball_x1, ball_x2, ball_y1, ball_y2 = control_userball(ball_x1, ball_x2, ball_y1, ball_y2, 10)
        x1, x2, y1, y2, loc, score = falling_ball_mv(x1, x2, y1, y2, speed, loc, score)
        x3, x4, y3, y4, loc2, score = falling_ball_mv(x3, x4, y3, y4, speed, loc2, score)
        remove_screen()
        time.sleep(0.01)


def intro(B_color, I_color, A_color, E_color):
    draw.text((20, 20), "Welcome", font=fnt, fill="#ff6f00")
    draw.text((20, 50), "Avoid balls", font=fnt, fill="#00b3ff")
    draw.text((20, 80), "Beginner", font=fnt, fill=B_color)
    draw.text((20, 110), "Intermediate ", font=fnt, fill=I_color)
    draw.text((20, 140), "Advanced ", font=fnt, fill=A_color)
    draw.text((20, 170), "Expert", font=fnt, fill=E_color)


# main
while True:
    intro(color_list[0], color_list[1], color_list[2], color_list[3])
    disp.image(image)
    if not button_U.value:
        color = color_list[tmp % 4]
        color_list[tmp % 4] = color_list[(tmp - 1) % 4]
        color_list[(tmp - 1) % 4] = color
        tmp = tmp - 1

    if not button_D.value:
        color = color_list[tmp % 4]
        color_list[tmp % 4] = color_list[(tmp + 1) % 4]
        color_list[(tmp + 1) % 4] = color
        tmp = tmp + 1
    if not button_A.value:
        remove_screen()
        if (tmp % 4 == 0):
            name = "Beginner_Ver"
            score = game_begin_inter(x1, x2, y1, y2, 20, name)
            game_end(score)
            remove_screen()
        if (tmp % 4 == 1):
            name = "Inter_Ver"
            score = game_begin_inter(x1, x2, y1, y2, 40, name)
            game_end(score)
            remove_screen()
        if (tmp % 4 == 2):
            name = "Advance_Ver"
            score = game_advance(x1, x2, y1, y2, 50, name)
            game_end(score)
            remove_screen()
        if (tmp % 4 == 3):
            name = "Expert_Ver"
            score = game_expert(x1, x2, y1, y2, 50, name)
            game_end(score)
            remove_screen()
		







