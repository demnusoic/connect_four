# --------------------------
# connect_four.py
# Date Created: 9/22/18
# Author: Nick Leyson
# Create a game of connect four using turtle graphics
# --------------------------

from turtle import *

class ConnectFourTurtles:
    """Initiate a game of connect four using turtle graphics."""
    def __init__(self, rows=6, columns=7, space_size=50):
        """ Create a grid of turtles of size rows x columns.
            rows(int): number of rows in the grid
            columns(int): number of columns in the grid
            space size(int): the size of each space in the grid in pixels
        """
        # Create a screen and set it to a variable
        self.screen = Screen()
        # Calculate size of grid and set it to variables
        self.grid_size_x = columns*space_size
        self.grid_size_y = rows*space_size
        # Set origin to top left of the grid. The grid will be centered in the canvas.
        self.x_orig = ((-1)*self.grid_size_x/2)
        self.y_orig = self.grid_size_y/2
        # set the dimensions of the grid to variables
        self.rows = rows
        self.columns = columns
        self.space_size = space_size
        self.x_bound_left = self.x_orig
        self.x_bound_right = self.x_orig+self.grid_size_x
        self.y_bound_top = self.y_orig
        self.y_bound_bottom = self.y_orig-self.grid_size_y

        # check corners of grid box
        # Turtle().setpos(self.x_orig, self.y_orig)
        # Turtle().setpos(self.x_bound_right, self.y_bound_top)
        # Turtle().setpos(self.x_bound_right, self.y_bound_bottom)
        # Turtle().setpos(self.x_orig, self.y_bound_bottom)

        # Set the space fill color to blue initially
        self.space_color = 'blue'
        # create a list to hold the grid turtles in the form
        # [
        #   [ConnectTurtle(0,0), ConnectTurtle(0,1)],
        #   [ConnectTurtle(1,0), ConnectTurtle(1,1)]
        # ]
        # to be accessed by using self.connect_turtles[row number][column number]
        self.connect_turtles = []
        # Bind onclick method to the screen
        self.screen.onclick(self.space_clicked)
        self.create_grid()

    def create_grid(self):
        "Create the turtles and set them to their position in the grid."
        for row_num in range(0,self.rows):
            row = []
            for column in range(0, self.columns):
                # Create a turtle, set the row and column attributes
                # set stretch factor to desired pixel size / 22
                # (the default size + padding) source: https://stackoverflow.com/questions/25712856/python-turtle-size-in-pixels
                stretch = self.space_size/22
                # Turn off animation
                self.screen.tracer(0)
                current_turtle = ConnectTurtle(row_num, column, stretch)
                # Set it to its row/column on the canvas
                x_pos = (self.space_size/2)+self.x_orig+(self.space_size*column)
                y_pos = (self.y_orig-(row_num*self.space_size))-(self.space_size/2)
                current_turtle.setpos(x_pos, y_pos)
                # Turn animation back on
                self.screen.tracer(1)
                row.append(current_turtle)
            self.connect_turtles.append(row)

    def space_clicked(self, x, y):
        """ Fill a clicked column with the current color and check for victory conditions.
            x: The x coord of the click event
            y: The y coord of the click event
        """
        # If x or y are outside grid area, do nothing.
        # Add 1px dead space to right bound to avoid a column index error at very edge
        if x < self.x_bound_left or x > self.x_bound_right-1 or y < self.y_bound_bottom or y > self.y_bound_top:
            return False
        # Calculate which column was clicked
        column_clicked = int(abs((self.x_orig-x)/self.space_size))
        # print(self.x_orig, x, self.space_size, (self.x_orig-x)/self.space_size, column_clicked)
        # If column is not filled, fill lowest available space with current color
        # Create a decrementor starting at the last/bottom index/row of the grid
        row_num = len(self.connect_turtles)-1
        while row_num >= 0:
            current_turtle = self.connect_turtles[row_num][column_clicked]
            # If an empty space is found fill it, check for victory conditions
            # and switch the current color
            if current_turtle.filled == False:
                current_turtle.filled = True
                current_turtle.fillcolor(self.space_color)
                # Check win before switching color,
                # if four in a row are found then current color is the victor
                self.check_win(current_turtle)
                self.switch_color()
                return True
            row_num -= 1
        # If the column is full, do nothing
        return False

    def switch_color(self):
        "Switch the current fill color between red and blue."
        self.space_color = 'blue' if (self.space_color == 'red') else 'red'

    def check_win(self, last_filled_turtle):
        """ Check if the current color has four spaces filled in a row in
            any direction from the last filled turtle.
            last_filled_turtle: The last turtle that was filled with a color
        """
        # Gather color matched turtles for each direction, N_S = North to South, etc.
        in_a_row = {
            "N_S" : [last_filled_turtle],
            "E_W" : [last_filled_turtle],
            "NW_SE" : [last_filled_turtle],
            "SW_NE" : [last_filled_turtle]
        }
        # Check surrounding directions for same color
        # Get the connected turtles of the same color found downwards,
        # collect them in the list for the north/south orientation
        self.get_connected(last_filled_turtle, 'd', in_a_row["N_S"])
        # Repeat for other directions. Since pieces are added on top, omit upwards direction
        self.get_connected(last_filled_turtle, 'r', in_a_row["E_W"])
        self.get_connected(last_filled_turtle, 'l', in_a_row["E_W"])
        self.get_connected(last_filled_turtle, 'dr', in_a_row["NW_SE"])
        self.get_connected(last_filled_turtle, 'ul', in_a_row["NW_SE"])
        self.get_connected(last_filled_turtle, 'ur', in_a_row["SW_NE"])
        self.get_connected(last_filled_turtle, 'dl', in_a_row["SW_NE"])
        # If any direction has four or more matches, declare current color
        # the winner and end the game.
        for direction in in_a_row:
            if len(in_a_row[direction]) >= 4:
                # End the game
                self.declare_winner(in_a_row[direction])

    def get_connected(self, grid_turtle, direction, turtle_collector):
        """ If the turtle in direction is the same color as the given turtle
            check subsequent turtles in that direction until a different color is found.
            Add the turtles to the turtle_collector list reference.
            grid_turtle: The origin turtle to check from
            direction: The direction in the grid to check from grid_turtle
            turtle_collector: A list to collect the found turtles
        """
        next_turtle = self.next_turtle(grid_turtle, direction)
        if next_turtle != grid_turtle and grid_turtle.fillcolor() == next_turtle.fillcolor():
            # Continue until a different colored turtle is found or the grid ends
            turtle_collector.append(next_turtle)
            self.get_connected(next_turtle, direction, turtle_collector)

    def next_turtle(self, grid_turtle, direction):
        """ Get the next turtle by spatial direction (U,D,L,R,UR,DR,UL,DL)
            Return the next turtle or the given turtle if index is outside of the grid.
            grid_turtle: The origin turtle to check from
            direction: The direction in the grid to check from grid_turtle
        """
        # Visually, row 0, col 0, is in the upper left corner
        # to move right/left, add/subtract the column
        # to move up/down, subtract/add the row
        row_num = grid_turtle.row
        column = grid_turtle.column
        try:
            if direction.lower() == 'u':
                if row_num == 0:
                    # Prevent negative indices
                    raise IndexError
                return self.connect_turtles[row_num-1][column]
            elif direction.lower() == 'd':
                return self.connect_turtles[row_num+1][column]
            elif direction.lower() == 'l':
                if column == 0:
                    raise IndexError
                return self.connect_turtles[row_num][column-1]
            elif direction.lower() == 'r':
                return self.connect_turtles[row_num][column+1]
            elif direction.lower() == 'ur':
                if row_num == 0:
                    raise IndexError
                return self.connect_turtles[row_num-1][column+1]
            elif direction.lower() == 'dr':
                return self.connect_turtles[row_num+1][column+1]
            elif direction.lower() == 'ul':
                if column == 0 or row_num == 0:
                    raise IndexError
                return self.connect_turtles[row_num-1][column-1]
            elif direction.lower() == 'dl':
                if column == 0:
                    raise IndexError
                return self.connect_turtles[row_num+1][column-1]
        except IndexError as e:
            return grid_turtle

    def declare_winner(self, winning_turtles):
        """ Print an end of game message declaring the winner.
            winning_turtles: A list of the connected turtles that caused the game to end
        """
        # Unbind onclick to prevent further input.
        self.screen.onclick(None)
        # Highlight the row of turtles that ended the game
        for winning_turtle in winning_turtles:
            winning_turtle.highlight()
        marquee_turtle = Turtle()
        self.screen.tracer(0)
        marquee_turtle.up()
        marquee_turtle.shape('turtle')
        marquee_turtle.setpos(0, self.y_bound_bottom-72)
        self.screen.tracer(1)
        marquee_turtle.write(
            self.space_color.capitalize()+" Wins",
            move=True,
            font=("Arial", 24, "bold")
        )
        self.screen.exitonclick()

class ConnectTurtle(Turtle):
    "A turtle to be used in a game of connect four"
    def __init__(self, row=None, column=None, size=3.5):
        """ Initialize using the parent initializer, add custom default options and attributes.
            row: The row number in the game grid where the turtle is located
            column: The column number in the game grid where the turtle is located
            size: The size of the turtle as a multiplier of the default size
        """
        # Use the Turtle initializer
        super().__init__()
        # set the location in the grid to variables
        self.row = row
        self.column = column
        self.size = size
        # set the initial appearance of the turtle
        self.shape("circle")
        # Allow resizing the turtle, and set the size of the spaces
        self.resizemode(rmode="user")
        self.turtlesize(size, size, 2.5)
        # Prevent turtle from drawing lines
        self.up()
        # Make fill color white
        self.fillcolor("#ffffff")
        # Create a variable to check if the turtle space has been filled
        self.filled = False

    def highlight(self):
        "Set the turtle outline to a highlighted color"
        self.turtlesize(self.size, self.size, 5)
        self.pencolor('green')

def main():
    ConnectFourTurtles()
    done()

if __name__ == '__main__':
    main()
