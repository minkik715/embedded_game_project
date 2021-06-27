import time
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

udlr_fill = "#00FF00"
udlr_outline = "#00FFFF"
button_fill = "#FF00FF"
button_outline = "#FFFFFF"

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

def random_location():
	return random.randint(1,4)

x1 = random.randint(0, 180)
size = random.randint(20,60)
x2 = x1+size
y1 = 0
y2 = y1 + size

def play_game(x1,x2,y1,y2,speed,level,score):
	ball_x1 = 110
	ball_x2 = 130
	ball_y1 = 210
	ball_y2 = 230
	draw.text((20, 20), "Level", font=fnt, fill=udlr_fill)
	draw.text((100, 20), str(level), font=fnt, fill=udlr_fill)
	disp.image(image)
	time.sleep(2)
	while(True):
		draw.ellipse((x1, y1, x2, y2), outline=button_outline, fill=udlr_fill)
		draw.ellipse((ball_x1, ball_y1, ball_x2, ball_y2), outline=button_outline, fill=button_fill)
		disp.image(image)
		draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
		disp.image(image)
		if(x2 > ball_x1 and x2 < ball_x2 and y2 > ball_y1):
			break
			
		if(x1 < ball_x2 and x2 > ball_x2 and y2 > ball_y1):
			break
	
		if (level == 1 and score ==200):
			return score
			
		if not button_L.value:
			ball_x1 -= 20
			ball_x2 -= 20
		if not button_R.value:
			ball_x1 += 20
			ball_x2 += 20
		if y2 <= 240:
			y1 = y1 +speed
			y2 = y2 +speed
		else:
			score += 10
			size = random.randint(20,40)
			y1 = 0
			y2 = y1+size
			x1 = random.randint(0,220)
			x2 = x1+size
	draw.text((20, 20), "Game Over", font=fnt, fill=udlr_fill)
	draw.text((40, 60), "Score:", font=fnt, fill=udlr_fill)
	draw.text((150, 60), str(score), font=fnt, fill=udlr_fill)
	disp.image(image)
	return 0
score = play_game(x1,x2,y1,y2,40,1,0) 
if(score):
   play_game(x1,x2,y1,y2,60,2,score)
	
