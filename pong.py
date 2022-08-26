import tkinter as tk
import random

# setting base Tk widget
root = tk.Tk()
root.resizable(False, False)
root.title("Pong")
root.configure(bg='black')
root.iconphoto(False, tk.PhotoImage(file='pong.png'))

# finding the center of the screen
screen_w = root.winfo_screenwidth()
screen_h = root.winfo_screenheight()
canvas_w = 1280
canvas_h = 720
center_x = int(screen_w/2 - canvas_w / 2)
center_y = int(screen_h/2 - canvas_h / 2)
root.geometry(f'{canvas_w}x{canvas_h}+{center_x}+{center_y}')

# canvas
cv = tk.Canvas(root, width=canvas_w, height=canvas_h)
cv.configure(bg="black")

# paddles
paddle_l = cv.create_rectangle(20, 320, 30, 390, outline='#000000', fill='#ffffff')
paddle_r = cv.create_rectangle(1250, 320, 1260, 390, outline='#000000', fill='#ffffff')

# middle line
midline1 = cv.create_rectangle(canvas_w/2-5, 25, canvas_w/2+5, 85, outline='#000000', fill='#ffffff')
midline2 = cv.create_rectangle(canvas_w/2-5, 125, canvas_w/2+5, 185, outline='#000000', fill='#ffffff')
midline3 = cv.create_rectangle(canvas_w/2-5, 225, canvas_w/2+5, 285, outline='#000000', fill='#ffffff')
midline4 = cv.create_rectangle(canvas_w/2-5, 325, canvas_w/2+5, 385, outline='#000000', fill='#ffffff')
midline5 = cv.create_rectangle(canvas_w/2-5, 425, canvas_w/2+5, 485, outline='#000000', fill='#ffffff')
midline6 = cv.create_rectangle(canvas_w/2-5, 525, canvas_w/2+5, 585, outline='#000000', fill='#ffffff')
midline7 = cv.create_rectangle(canvas_w/2-5, 625, canvas_w/2+5, 685, outline='#000000', fill='#ffffff')

# score trackers
score_left = tk.Label(text='0', bg='#000000', fg='#ffffff', font=('Helvetica', 30))
score_right = tk.Label(text='0', bg='#000000', fg='#ffffff', font=('Helvetica', 30))
score_left.place(relx=0.43, rely=0.1)
score_right.place(relx=0.55, rely=0.1)

# ball
ball = cv.create_rectangle(canvas_w/2-10, canvas_h/2-10, canvas_w/2+10, canvas_h/2+10, outline='#000000', fill='#696969')

cv.pack()

# movement of the paddles
def detectMoveKeys():

	# left paddle
	root.bind('w', leftUp)
	root.bind('s', leftDown)
	
	# right paddle
	root.bind('i', rightUp)
	root.bind('k', rightDown)
	if end == False:
		root.after(200, detectMoveKeys)

def leftUp(self):
	cv.move(paddle_l, 0, -10)
def leftDown(self):
	cv.move(paddle_l, 0, 10)
def rightUp(self):
	cv.move(paddle_r, 0, -10)
def rightDown(self):
	cv.move(paddle_r, 0, 10)

def ballMovement():
	global x, y	

    # checking if the ball touched the bottom side of the window
	if cv.coords(ball)[1]+10 == canvas_h:
		y = y * (0-1)

	# checking if the ball touched the top side of the window
	if cv.coords(ball)[1] == 0:
		y = y * (0-1)

	pos = cv.coords(ball)
	if paddle_l in cv.find_overlapping(pos[0], pos[1], pos[2], pos[3]):
		x = x * (0-1)
	if paddle_r in cv.find_overlapping(pos[0], pos[1], pos[2], pos[3]):
		x = x * (0-1)

	cv.move(ball, x, y)
	cv.pack()
	
	if end == False:
		root.after(35, ballMovement) 

def outOfBounds():
	global num_l, num_r, ball, dirx, diry, x, y

    # checking if the ball is out of bounds on the left side
	if cv.coords(ball)[0] < 30:
		num_r += 1
		score_right['text'] = str(num_r)
		
		# setting the ball to the original position and setting the direction
		cv.coords(ball, canvas_w/2-10, canvas_h/2-10, canvas_w/2+10, canvas_h/2+10)
		cv.pack()
		dirx = random.randint(0, 1)
		diry = random.randint(0, 1)
		if dirx == 0 and diry == 0:
			x = -10
			y = -10
		if dirx == 0 and diry == 1:
			x = -10
			y = 10
		if dirx == 1 and diry == 0:
			x = 10
			y = -10
		if dirx == 1 and diry == 1:
			x = 10
			y = 10

    # checking if the ball is out of bounds on the right side
	if cv.coords(ball)[2] > 1250:
		num_l += 1
		score_left['text'] = str(num_l)
	
		# setting the ball to the original position and setting the direction
		cv.coords(ball, canvas_w/2-10, canvas_h/2-10, canvas_w/2+10, canvas_h/2+10)
		cv.pack()
		dirx = random.randint(0, 1)
		diry = random.randint(0, 1)
		if dirx == 0 and diry == 0:
			x = -10
			y = -10
		if dirx == 0 and diry == 1:
			x = -10
			y = 10
		if dirx == 1 and diry == 0:
			x = 10
			y = -10
		if dirx == 1 and diry == 1:
			x = 10
			y = 10

	# making sure the paddles don't go out of the screen
	if cv.coords(paddle_l)[1] <= 0: 
		cv.coords(paddle_l, 20, 10, 30, 80)

	if cv.coords(paddle_l)[3] >= canvas_h:
		cv.coords(paddle_l, 20, 640, 30, 710)

	if cv.coords(paddle_r)[1] <= 0:
		cv.coords(paddle_r, 1250, 10, 1260, 80)

	if cv.coords(paddle_r)[3] >= canvas_h:
		cv.coords(paddle_r, 1250, 640, 1260, 710)

	if end == False:
		root.after(200, outOfBounds)

# checking if the game should end
def endGame():
	global end, ball, paddle_l, paddle_r

    # deleting the label and settings objects back to original positions
	def r_won_destroy():
		r_won.destroy()
		cv.coords(ball, canvas_w/2-10, canvas_h/2-10, canvas_w/2+10, canvas_h/2+10)
		cv.coords(paddle_l, 20, 320, 30, 390)
		cv.coords(paddle_r, 1250, 320, 1260, 390)
		score_right['text'] = '0'
		score_left['text'] = '0'

    # checking if the right score is 10, if yes, the game ends
	if score_right['text'] == '10':
		r_won = tk.Label(text='Right won,\nthe game will\nrestart in 3 sec.', bg='black', fg='white', font=('Helvetica', 50), padx=20, pady=20)
		r_won.place(relx=0.3, rely=0.4)
		end = True
		cv.itemconfig('all', fill='black')
		score_left['text'] = ''
		score_right['text'] = ''
		root.after(3000, main)
		root.after(3000, r_won_destroy)

    # deleting the label and settings objects back to original positions
	def l_won_destroy():
		l_won.destroy()
		cv.coords(ball, canvas_w/2-10, canvas_h/2-10, canvas_w/2+10, canvas_h/2+10)
		cv.coords(paddle_l, 20, 320, 30, 390)
		cv.coords(paddle_r, 1250, 320, 1260, 390)
		score_right['text'] = '0'
		score_left['text'] = '0'

    # checking if the left score is 10, if yes, the game ends
	if score_left['text'] == '10':
		l_won = tk.Label(text='Left won,\nthe game will\nrestart in 3 sec.', bg='black', fg='white', font=('Helvetica', 50), padx=20, pady=20)
		l_won.place(relx=0.3, rely=0.4)
		end = True
		cv.itemconfig('all', fill='black')
		score_left['text'] = ''
		score_right['text'] = ''
		root.after(3000, main)
		root.after(3000, l_won_destroy)

	if end == False:
		root.after(200, endGame)

def main():
	# initializing variables
	global x, y, end, num_l, num_r
	end = False
	num_l = 0
	num_r = 0
	x = 0
	y = 0
	dirx = random.randint(0, 1)
	diry = random.randint(0, 1)
	cv.itemconfig('all', fill='white')
	cv.itemconfig(ball, fill='#696969')

	# setting the starting diretion of the ball
	if dirx == 0 and diry == 0:
		x = -10
		y = -10
	if dirx == 0 and diry == 1:
		x = -10
		y = 10
	if dirx == 1 and diry == 0:
		x = 10
		y = -10
	if dirx == 1 and diry == 1:
		x = 10
		y = 10

	# calling other functions
	detectMoveKeys()
	ballMovement()
	outOfBounds()
	endGame()

# calling the main function
main()

# starting mainloop for the main window object
root.mainloop()
