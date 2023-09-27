# Arkanoid.py

# Author: Alexis Demetriou (G20970098)

# Email: ADemetriou5@uclan.ac.uk

# Description: The Arkanoid.py program demonstrates (Arkanoid) arcade game from the 1980's.
# The player controls a rectangular craft at the bottom of the screen, moving it left and right,
# to deflect a ball and eliminate a number of bricks by hitting them with the ball.
# The definition of the Ball Class is reused from the BallAsAClass.py code provided under Week03, step0304.
# The definition of the Craft Class is reused from the Exercise0202.py code provided under Week02, xtras, Exercise0202.
# The definition of the Brick Class for drawing bricks in multiple rows is reused from the NestedLoops.py code provided under Week01, step0107.
# The text that display the score (points) in the bottom left corner of the window (Score Class) and in the middle of the windows canvas is
# reused from the ShowingTextOnCanvas.py code provided under Week03, step0303.
# A new list containing a sequence of colors (as strings) to be used to fill color of the drawn bricks in each row
# is reused from the MoreMouseInputWithLists.py code provided under Week02, step0204.
# The nested-if structure is adapted from the lecture slides week 1, slide 61.

from tkinter import *
TITLE = "Arkanoid - First Capstone Project"
WIDTH, HEIGHT = 800, 600  # the width and height for the resolution
centre_x, centre_y = WIDTH // 2, HEIGHT // 2  # initialize 'centre_x' and 'centre_y' to be at the center of the window.
craft_x, craft_y = 110, 10  # the craft x and y coordinates (in pixels).
ball_speed_x, ball_speed_y = -1, -1  # the x and y ball speed (in pixels).
BALL_RADIUS = 10  # the circle radius (in pixels).
drawn_circles = []  # define a new List to hold the drawn circles.
MAX_BALLS = 5  # this is the max number of circles to keep on screen.
DELAY = 4  # delay between animations, in milliseconds
BRICKS_PART = 0.22
ROWS, COLS = 5, 17  # declaring rows and cols for bricks
SPACE_BRICK = 4  # the space between bricks
brick_w, brick_h = WIDTH / COLS, HEIGHT * BRICKS_PART / ROWS  # the brick x and y coordinates (in pixels).
bricks = []  # define a new List to hold the drawn bricks.
COLORS = ['yellow', 'orange', 'purple', 'blue', 'green']  # define a new List to hold the colors for the bricks.
color_index = 0  # index for the color
game_mode = False  # the player will be able to move the platform only during the game
start_text = []  # this will show the text before the start of the game.
# It lays out all the instructions that must be followed in order for the player to start the game.

win = Tk()  # creates a GUI window (using the tkinter library)
win.title(TITLE)  # sets window's title to 'Arkanoid - First Capstone Project' (shown in the top area)

canvas = Canvas(win, width=WIDTH, height=HEIGHT)  # link the canvas to the 'win' and set its size (in this case the full window).
canvas.config(bg='dark blue')  # sets the background color of the canvas using the 'bg' property.
canvas.pack()  # the following command ('pack') packs the widget within the host window.

start_text.append(canvas.create_text(centre_x, centre_y, text='Select game difficulty:', font=(None, 18), fill='white'))
start_text.append(canvas.create_text(centre_x, centre_y + 25, text='Default difficulty: easy', font=(None, 18), fill='white'))
start_text.append(canvas.create_text(centre_x, centre_y + 50, text='Press the "m" key for medium difficulty', font=(None, 18), fill='white'))
start_text.append(canvas.create_text(centre_x, centre_y + 75, text='Press the "h" key for hard difficulty', font=(None, 18), fill='white'))
start_text.append(canvas.create_text(centre_x, centre_y + 100, text='Press Space to start the game', font=(None, 18), fill='white'))
print("Select game difficulty:")
print("Default difficulty: easy")
print("Press the 'm' key for medium difficulty")
print("Press the 'h' key for medium difficulty")
print("Press Space to start the game")
print("Use the mouse to move the rectangle left and right in the window!")
print("Press X to exit.")
craft = canvas.create_rectangle(centre_x - craft_x // 2, HEIGHT, centre_x + craft_x // 2, HEIGHT - craft_y, fill='cyan')  # initial coordinates of the craft
score = canvas.create_text(40, HEIGHT - 25, text='0', font=(None, 18))  # initial score of the game


class Craft:  # create a craft class to update the crafting coordinates when the user moves the mouse.

    def __init__(self, craft_id, x_c,  mode):
        self.craft_id = craft_id
        self.x = x_c
        self.game_mode = mode

    def move(self, event):  # this function simply handles the mouse motion events. The mouse coordinates are extracted from the 'event' argument.
        self.x = event.x
        if self.game_mode and WIDTH - craft_x // 2 > self.x > craft_x // 2:  # check if craft is within windows resolution
            canvas.coords(self.craft_id, self.x - craft_x // 2, HEIGHT, self.x + craft_x // 2, HEIGHT - craft_y)  # updating crafting coordinates


class Ball:  # create a ball class in which the ball is animated as a red ball moving in the window.
    # When the ball collides with the craft or the brick it is repelled.
    # Also, the speed x of the ball will change depending on the place where the ball was bounced of the craft.
    # The ball will show a trace of the last five places where it moved.

    def __init__(self, x_ball, y_ball, speed_x, speed_y, radius, maximum):  # ball data
        self.x = x_ball
        self.y = y_ball
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.radius = radius
        self.max = maximum

    def move(self):
        self.x = self.x + self.speed_x  # updates the X
        self.y = self.y + self.speed_y  # updates the Y
        ball_id = canvas.create_oval(self.x - self.radius, self.y - self.radius, self.x + self.radius, self.y + self.radius, fill='red')  # draw the circle
        drawn_circles.append(ball_id)  # save ball id by adding it to the end of a List using the 'append' function.
        # The following lines of code ensure that the ball bounces back when it hits the right/left and top/bottom boundaries of the window.
        if self.x >= WIDTH - self.radius:  # when it bounces, the horizontal speed is reversed.
            self.speed_x = -abs(self.speed_x)
        if self.x <= self.radius:  # when it bounces, the horizontal speed is reversed.
            self.speed_x = abs(self.speed_x)
        if self.y <= self.radius:  # when it bounces, the vertical speed is reversed.
            self.speed_y = abs(self.speed_y)
        if c.x - craft_x // 2 <= self.x <= c.x + craft_x // 2 and self.y >= HEIGHT - (self.radius + craft_y):
            # when the ball collides with a craft, it bounces, and the vertical speed is reversed.
            # Since I lowered the value "DELAY" for the canvas.after(DELAY, animation)
            # to make the game look smoother (higher fps), when the speed of the ball x becomes -10 or 10, the speed of the ball is unplayable fast.
            # Instead of 10 and -10 for ball speed x, I put 4 and -4.
            self.speed_y = -abs(self.speed_y)
            if c.x - craft_x // 2 <= self.x < c.x + craft_x // 2 - (craft_x*4/5) and self.y >= HEIGHT - (self.radius + craft_y):
                self.speed_x = -4
                # self.speed_x = -10
            if c.x - craft_x // 2 + (craft_x*1/5) <= self.x <= c.x + craft_x // 2 - (craft_x*3/5) and self.y >= HEIGHT - (self.radius + craft_y):
                self.speed_x = -2
            if c.x - craft_x // 2 + (craft_x*2/5) <= self.x <= c.x + craft_x // 2 - (craft_x*2/5) and self.y >= HEIGHT - (self.radius + craft_y):
                self.speed_x = 0
            if c.x - craft_x // 2 + (craft_x*3/5) <= self.x <= c.x + craft_x // 2 - (craft_x*1/5) and self.y >= HEIGHT - (self.radius + craft_y):
                self.speed_x = 2
            if c.x - craft_x // 2 + (craft_x*4/5) <= self.x <= c.x + craft_x // 2 and self.y >= HEIGHT - (self.radius + craft_y):
                self.speed_x = 4
                # self.speed_x = 10
        if len(drawn_circles) > self.max:  # check whether the structure has exceeded its intended capacity.
            canvas.delete(drawn_circles.pop(0))  # the 'pop' function removes and returns the specified
        # element from the List, specifying the ball index. The 'delete' function of the Canvas takes a ball id and deletes it.


class Brick:  # create a brick class in which bricks will be drawn.
    # On each line, the bricks will have a different color.
    # This class has a function where the brick will be removed when it collides with the ball.

    def __init__(self, bricks_id):
        self.bricks = bricks_id
        self.deleted_bricks = 0

    for row in range(ROWS):  # for each row
        if color_index > len(COLORS) - 1:  # if the index moved past the last item
            color_index = 0  # then reset it to zero (first item).
        color = COLORS[color_index]  # choose a color from the COLORS
        color_index += 1  # move the index to the next value
        for col in range(COLS):  # for each col
            x_brick, y_brick = col * brick_w, row * brick_h  # making an equation to create brick x1 and y1 coordinates
            bricks.append(canvas.create_rectangle(x_brick + SPACE_BRICK, y_brick + SPACE_BRICK, x_brick + brick_w, y_brick + brick_h, fill=color, outline='black'))
            # Save bricks by adding it to the end of a List using the 'append' function.

    def brick_collide(self):  # in this function, we check if one of the bricks has collided with the ball.
        for brick in self.bricks:  # check every brick
            x1_brick, y1_brick, x2_brick, y2_brick = canvas.coords(brick)  # extract brick coordinates
            detection = False
            # check if the ball hit the bottom of the brick.
            if x1_brick <= b.x <= x2_brick and y1_brick <= b.y - BALL_RADIUS <= y2_brick and b.speed_y < 0:
                b.speed_y *= -1
                detection = True
            # check if the ball hit the top of the brick.
            if x1_brick <= b.x <= x2_brick and y1_brick <= b.y + BALL_RADIUS <= y2_brick and b.speed_y > 0:
                b.speed_y *= -1
                detection = True
            # check if the ball hit the right side of the brick.
            if x1_brick <= b.x - BALL_RADIUS <= x2_brick and y1_brick <= b.y <= y2_brick and b.speed_x < 0:
                b.speed_x *= -1
                detection = True
            # check if the ball hit the left side of the brick.
            if x1_brick <= b.x + BALL_RADIUS <= x2_brick and y1_brick <= b.y <= y2_brick and b.speed_x > 0:
                b.speed_x *= -1
                detection = True
            if detection:
                canvas.delete(brick)  # in this case the brick is removed
                self.bricks.pop(self.bricks.index(brick))
                self.deleted_bricks += 1


class Score:  # create a Score class to display the score in the text.
    # The text will be displayed in the lower left corner of the window.
    # When a brick is destroyed, the player receives +10 points.

    def __init__(self, score_text):  # score data
        self.score = score_text
        self.scored_points = 0

    def scored(self):
        self.scored_points = brick_class.deleted_bricks * 10  # assigns the deleted bricks to score by multiplying by 10 points.
        canvas.itemconfig(self.score, text=str(self.scored_points))  # the code updates the text, which shows the score.


def game_settings():
    win.bind('<m>', lambda _: difficulty_medium())  # pressing the "s" key changes the difficulty of the game (in this case it is medium difficulty).
    win.bind('<h>', lambda _: difficulty_hard())  # pressing the "d" key changes the difficulty of the game (in this case it is hard difficulty).
    win.bind('<space>', lambda _: animation())  # the game will not start until the player presses the "space" key.


def difficulty_medium():
    b.speed_x, b.speed_y = -2, -2  # the x and y ball speed for medium difficulty (in pixels).


def difficulty_hard():
    b.speed_x, b.speed_y = -3, -3  # the x and y ball speed for hard difficulty (in pixels).


def animation():
    win.unbind('<m>')
    win.unbind('<h>')
    win.unbind('<space>')
    for i in start_text:  # when the player presses Space, then all instructions are removed from windows.
        canvas.delete(i)
    c.game_mode = True
    b.move()
    brick_class.brick_collide()
    s.scored()
    win.update()
    if b.y < HEIGHT - BALL_RADIUS and s.scored_points != ROWS * COLS * 10:
        # if the ball didn't hit the ground and the ball didn't hit all the bricks, then the game continues.
        canvas.after(DELAY, animation)  # this calls this function (named 'animation') again, after waiting 'DELAY' milliseconds.
    else:  # if the ball hit the ground or the ball hit all the bricks, then the game ends.
        c.game_mode = False  # in this case the craft will not be able to move.
        if s.scored_points == ROWS * COLS * 10:  # the game stops when the ball hits all the bricks.
            canvas.create_text(centre_x, centre_y, text='YOU WIN!', fill='green', font=(None, 24))
            print("YOU WIN!")
        else:  # or when the ball hits the ground and not the craft.
            canvas.create_text(centre_x, centre_y, text='GAME OVER!', fill='red', font=(None, 24))
            print("GAME OVER!")


def on_key_press(event):  # this function is called to handle arbitrary key presses.
    if event.char == 'x' or event.char == 'X':  # handle small or capital X.
        quit()  # quit the game (windows closes)


c = Craft(craft, centre_x, game_mode)
brick_class = Brick(bricks)
b = Ball(centre_x, centre_y, ball_speed_x - brick_class.deleted_bricks, ball_speed_y - brick_class.deleted_bricks, BALL_RADIUS, MAX_BALLS)
s = Score(score)

game_settings()
win.bind('<Motion>', c.move)  # special event '<Motion>' which corresponds to the mouse movement, to the 'move' function specified above.
win.bind('<KeyPress>', on_key_press)  # '<KeyPress>' is used to handle small or capital X.
win.mainloop()  # To keep the window around, the 'win.mainloop()' call activates the window.
