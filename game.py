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
# SET
x1 = random.randint(0, 180)
size = random.randint(20,60)
x2 = x1+size
y1 = 0
y2 = y1 + size
B_color = "#FF00FF"
I_color = udlr_fill
A_color = udlr_fill
E_color = udlr_fill
tmp = 100
color_list = [B_color, I_color, A_color, E_color]



def remove_screen():
	draw.rectangle((0, 0, width, height), outline=0, fill=(0, 0, 0))
	disp.image(image)


	

def game_end(score):
	draw.text((20, 20), "Game Over", font=fnt, fill=udlr_fill)
	draw.text((20, 60), "Score:", font=fnt, fill=udlr_fill)
	draw.text((150, 60), str(score), font=fnt, fill=udlr_fill)
	disp.image(image)
	time.sleep(4)
	remove_screen()
	
	
	
def game_begin_inter(x1,x2,y1,y2,speed,name):
	ball_x1 = 110
	ball_x2 = 130
	ball_y1 = 210
	ball_y2 = 230
	draw.text((30, 50), name, font=fnt, fill=udlr_fill)
	disp.image(image)
	time.sleep(2)
	score = 0
	while(True):
		rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
		draw.ellipse((x1, y1, x2, y2), outline=button_outline, fill=rcolor)
		draw.ellipse((ball_x1, ball_y1, ball_x2, ball_y2), outline=button_outline, fill=udlr_fill)
		disp.image(image)
		#1
		if(x2 >= ball_x1 and x2 <= ball_x2 and y2 >= ball_y1 and y2 <= ball_y2):
			time.sleep(1)
			return score
 		#3
		if(x1 <= ball_x2 and x1 >= ball_x1 and y2 >= ball_y1 and y2 <= ball_y2):
			time.sleep(1)
			return score
		#2
		if(x1 >= ball_x1 and x2 <= ball_x2 and y2 >= ball_y1 and y2 <= ball_y2):
			time.sleep(1)
			return score
		#4
		if(y1 >= ball_y1 and y2 <= ball_y2 and x2 >= ball_x1 and x2 <= ball_x2):
			time.sleep(1)
			return score
		#5
		if(y1 <= ball_y2 and y1 >= ball_y1 and x2 >= ball_x1 and x2 <= ball_x2):
			time.sleep(1)
			return score
		#6
		if(x1 >= ball_x1 and x2 <= ball_x2 and y1 <= ball_y2 and y1 >= ball_y1):
			time.sleep(1)
			return score
		#7
		if(x1 <= ball_x2 and x1 >= ball_x1 and  y1 <= ball_y2 and y1 >= ball_y1):
			time.sleep(1)
			return score
		#8
		if(y1 >= ball_y1 and y2 <= ball_y2 and x1 <= ball_x2 and x1 >= ball_x1):
			time.sleep(1)
			return score
		#9
		if(y1 >= ball_y1 and y2 <= ball_y2 and x1 >= ball_x1 and x2 <= ball_x2):
			time.sleep(1)
			return score
		
		if not button_L.value:
			ball_x1 -= 20
			ball_x2 -= 20
		if not button_R.value:
			ball_x1 += 20
			ball_x2 += 20
		if not button_U.value:
			ball_y1 -= 20
			ball_y2 -= 20
		if not button_D.value:
			ball_y1 += 20
			ball_y2 += 20
		if y1 <= 250:
			y1 = y1 +speed
			y2 = y2 +speed
		else:
			score += 10
			size = random.randint(20,40)
			y1 = 0
			y2 = y1+size
			x1 = random.randint(0,220)
			x2 = x1+size
		remove_screen()
		time.sleep(0.01)

def game_advance(x1,x2,y1,y2,speed,name):
	ball_x1 = 110
	ball_x2 = 130
	ball_y1 = 110
	ball_y2 = 130
	draw.text((30, 50), name, font=fnt, fill=udlr_fill)
	disp.image(image)
	time.sleep(2)
	score = 0
	loc = 1
	while(True):
		rcolor = tuple(int(x * 255) for x in hsv_to_rgb(random.random(), 1, 1))
		draw.ellipse((x1, y1, x2, y2), outline=button_outline, fill=rcolor)
		draw.ellipse((ball_x1, ball_y1, ball_x2, ball_y2), outline=button_outline, fill=udlr_fill)
		disp.image(image)
		#1
		if(x2 >= ball_x1 and x2 <= ball_x2 and y2 >= ball_y1 and y2 <= ball_y2):
			time.sleep(1)
			return score
 		#3
		if(x1 <= ball_x2 and x1 >= ball_x1 and y2 >= ball_y1 and y2 <= ball_y2):
			time.sleep(1)
			return score
		#2
		if(x1 >= ball_x1 and x2 <= ball_x2 and y2 >= ball_y1 and y2 <= ball_y2):
			time.sleep(1)
			return score
		#4
		if(y1 >= ball_y1 and y2 <= ball_y2 and x2 >= ball_x1 and x2 <= ball_x2):
			time.sleep(1)
			return score
		#5
		if(y1 <= ball_y2 and y1 >= ball_y1 and x2 >= ball_x1 and x2 <= ball_x2):
			time.sleep(1)
			return score
		#6
		if(x1 >= ball_x1 and x2 <= ball_x2 and y1 <= ball_y2 and y1 >= ball_y1):
			time.sleep(1)
			return score
		#7
		if(x1 <= ball_x2 and x1 >= ball_x1 and  y1 <= ball_y2 and y1 >= ball_y1):
			time.sleep(1)
			return score
		#8
		if(y1 >= ball_y1 and y2 <= ball_y2 and x1 <= ball_x2 and x1 >= ball_x1):
			time.sleep(1)
			return score
		#9
		if(y1 >= ball_y1 and y2 <= ball_y2 and x1 >= ball_x1 and x2 <= ball_x2):
			time.sleep(1)
			return score
		
		if not button_L.value:
			ball_x1 -= 20
			ball_x2 -= 20
		if not button_R.value:
			ball_x1 += 20
			ball_x2 += 20
		if not button_U.value:
			ball_y1 -= 20
			ball_y2 -= 20
		if not button_D.value:
			ball_y1 += 20
			ball_y2 += 20
		if loc == 1 and y1 <= 250:
			y1 = y1 +speed
			y2 = y2 +speed
		elif loc ==2 and x1 <= 250:
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
				size = random.randint(20,40)
				y1 = 0
				y2 = y1+size
				x1 = random.randint(0,200)
				x2 = x1+size
			if loc == 2:
				size = random.randint(20,40)
				y1 = random.randint(0,200)
				y2 = y1+size
				x1 = 0
				x2 = x1+size			
			if loc == 3:
				size = random.randint(20,40)
				y1 = 240 - size
				y2 = 240
				x1 = random.randint(0,200)
				x2 = x1+size
			if loc == 4:
				size = random.randint(20,40)
				y1 = random.randint(0,200)
				y2 = y1+size
				x1 = 240-size
				x2 = 240
		remove_screen()
		time.sleep(0.01)

	
	
	
	
def intro(B_color, I_color , A_color , E_color):
	draw.text((20, 20), "Welcome", font=fnt, fill=udlr_fill)
	draw.text((20, 50), "Avoid balls", font=fnt, fill=udlr_fill)
	draw.text((20, 80), "Beginner", font=fnt, fill=B_color)
	draw.text((20, 110), "Intermediate ", font=fnt, fill=I_color)
	draw.text((20, 140), "Advanced ", font=fnt, fill=A_color)
	draw.text((20, 170), "Expert", font=fnt, fill=E_color)
	
	
	
# main
while True:
	intro(color_list[0], color_list[1] , color_list[2] , color_list[3])
	disp.image(image)
	if not button_U.value:
		color = color_list[tmp%4]
		color_list[tmp % 4] = color_list[(tmp-1)%4]
		color_list[(tmp-1)%4] = color
		tmp = tmp - 1

	if not button_D.value:
		color = color_list[tmp % 4]
		color_list[tmp % 4] = color_list[(tmp+1) % 4]
		color_list[(tmp+1) % 4] = color
		tmp = tmp + 1
	if not button_A.value:
		remove_screen()
		if(tmp%4 == 0):
			name = "Beginner_Ver"
			score = game_begin_inter(x1,x2,y1,y2,20,name)
			game_end(score)
			remove_screen()
		if(tmp%4 == 1):
			name = "Inter_Ver"
			score = game_begin_inter(x1,x2,y1,y2,60,name)
			game_end(score)
			remove_screen()
		if(tmp%4 == 2):
			name = "Advance_Ver"
			score = game_advance(x1,x2,y1,y2,40,name)
			game_end(score)
			remove_screen()
		if(tmp%4 == 3):
			name = "Expert_Ver"
			score = game_begin_inter(x1,x2,y1,y2,60,name)
			game_end(score)
			remove_screen()
		







