import math
from utils import *
import pygame

WIN = pygame.display.set_mode((WIDTH + RIGHT_TOOLBAR_WIDTH, HEIGHT))
pygame.display.set_caption("Pyaint")
STATE = "COLOR"
Change = False

DRAW_CLICKED = False    #used for rendering shapes when draw is clicked
DOTTED = False  #tells if dotted button is clicked or not

def init_grid(rows, columns, color):
    grid = []

    for i in range(rows):
        grid.append([])
        for _ in range(columns):    #use _ when variable is not required
            grid[i].append(color)
    return grid

def draw_grid(win, grid):
    for i, row in enumerate(grid):
        for j, pixel in enumerate(row):
            pygame.draw.rect(win, pixel, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

    if DRAW_GRID_LINES:
        for i in range(ROWS + 1):
            pygame.draw.line(win, SILVER, (0, i * PIXEL_SIZE), (WIDTH, i * PIXEL_SIZE))
        for i in range(COLS + 1):
            pygame.draw.line(win, SILVER, (i * PIXEL_SIZE, 0), (i * PIXEL_SIZE, HEIGHT - TOOLBAR_HEIGHT))

def draw_mouse_position_text(win):
    pos = pygame.mouse.get_pos()
    pos_font = get_font(MOUSE_POSITION_TEXT_SIZE)
    try:
        row, col = get_row_col_from_pos(pos)
        text_surface = pos_font.render(str(row) + ", " + str(col), 1, BLACK)
        win.blit(text_surface, (5 , HEIGHT - TOOLBAR_HEIGHT))
    except IndexError:
        for button in buttons:
            if not button.hover(pos):
                continue
            if button.text == "Clear":
                text_surface = pos_font.render("Clear Everything", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.text == "Erase":
                text_surface = pos_font.render("Erase", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "FillBucket":
                text_surface = pos_font.render("Fill Bucket", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Brush":
                text_surface = pos_font.render("Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.name == "Change":
                text_surface = pos_font.render("Swap Toolbar", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            r,g,b = button.color
            text_surface = pos_font.render("( " + str(r) + ", " + str(g) + ", " + str(b) + " )", 1, BLACK)
            
            win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
        
        for button in brush_widths:
            if not button.hover(pos):
                continue
            if button.width == size_small:
                text_surface = pos_font.render("Small-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_medium:
                text_surface = pos_font.render("Medium-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break
            if button.width == size_large:
                text_surface = pos_font.render("Large-Sized Brush", 1, BLACK)
                win.blit(text_surface, (10 , HEIGHT - TOOLBAR_HEIGHT))
                break    

def draw(win, grid, buttons):
    win.fill(BG_COLOR)
    draw_grid(win, grid)

    for button in buttons:
        button.draw(win)

    draw_brush_widths(win)
    draw_mouse_position_text(win)
    pygame.display.update()


def draw_brush_widths(win):
    brush_widths = [
        Button(rtb_x - size_small/2, 480, size_small, size_small, drawing_color, None, None, "ellipse"),    
        Button(rtb_x - size_medium/2, 510, size_medium, size_medium, drawing_color, None, None, "ellipse") , 
        Button(rtb_x - size_large/2, 550, size_large, size_large, drawing_color, None, None, "ellipse")  
    ]
    for button in brush_widths:
        button.draw(win)
        # Set border colour
        border_color = BLACK
        if button.color == BLACK:
            border_color = GRAY
        else:
            border_color = BLACK
        # Set border width
        border_width = 2
        if ((BRUSH_SIZE == 1 and button.width == size_small) or (BRUSH_SIZE == 2 and button.width == size_medium) or (BRUSH_SIZE == 3 and button.width == size_large)): 
            border_width = 4
        else:
            border_width = 2
        # Draw border
        pygame.draw.ellipse(win, border_color, (button.x, button.y, button.width, button.height), border_width) #border

def get_row_col_from_pos(pos):
    x, y = pos
    row = y // PIXEL_SIZE
    col = x // PIXEL_SIZE

    if row >= ROWS:
        raise IndexError
    if col >= ROWS:
        raise IndexError
    return row, col

def draw_arc():
    
    arc_width = 5
    radius = 50
    pos = pygame.mouse.get_pos()
    x, y = get_row_col_from_pos(pos)
    center_point = (x,y)
    
    

    # Clear the screen
    

    # Draw the arc using the center point, radius, start angle, and end angle
    pygame.draw.arc(WIN, BLACK, (center_point[0]-radius + 50 , center_point[1]-radius + 50, radius, radius), 30, 70, arc_width)

    # Update the display
    pygame.display.flip()
    
    

def draw_line(start, end):
    
    """
    x1, y1 = start
    x2, y2 = end
    x2, y2 = (x2-50), (y2-40)
    print(x1 , y1)
    print(x2, y2)

    # Calculate the slope of the line
    slope = (y2 - y1) / (x2 - x1)

    # Iterate over the range of x values from start to end
    for x in range(x1, x2+1):
        # Calculate the y value for the current x value
        y = slope * (x - x1) + y1
        # Convert the floating point y value to an integer
        y = int(y)
        
        #grid[x][y] = drawing_color
    """
    
    
    
    pygame.draw.line(WIN, BLACK, start, end, 6)
    
    pygame.display.flip()

def get_solid_bspline_coordinates(X,Y):
    list= []
    for i in range(4):
        list.append((X + i, Y - 7 - i))
        list.append((X - i, Y - 7 + i))
    list.append((X,Y))
    for i in range(4):
        list.append((X + i, Y + 7 - i))
        list.append((X - i, Y + 7 + i))
    for i in range(4):
        list.append((X - i, Y - i))
        list.append((X + i, Y + i))
    return list

def get_dotted_bspline_coordinates(X,Y):
    list= []
    for i in range(0,4,2):
        list.append((X + i, Y - 7 - i))
        list.append((X - i, Y - 7 + i))
    list.append((X,Y))
    for i in range(0,4,2):
        list.append((X + i, Y + 7 - i))
        list.append((X - i, Y + 7 + i))
    for i in range(0,4,2):
        list.append((X - i, Y - i))
        list.append((X + i, Y + i))
    return list
    
def draw_bspline():
    pos = pygame.mouse.get_pos()
    x, y = get_row_col_from_pos(pos)
    if DOTTED:
        coordinates = get_dotted_bspline_coordinates(x,y)
    else:
        coordinates = get_solid_bspline_coordinates(x,y)

    for i in coordinates:
            x, y = i
            grid[x][y] = drawing_color
            
    


def draw_arc(row,col,radius):
    if DOTTED:
        grid[row][col]=drawing_color
        for i in range(radius-1):
            if(i%2!=0):
                grid[row-i][col+i]=drawing_color
            x=row-i
            y=col+i
        grid[x][y+1]=drawing_color
        for i in range(3):
            if(i%2!=0):
                grid[x+i][y+1+i]=drawing_color
            
        for i in range(3,6):
            if(i%2!=0):
                grid[x+i][y+4]=drawing_color
        grid[x+6][y+3]=drawing_color
        grid[x+7][y+2]=drawing_color    
        for i in range(radius):
            if(i%2==0):
                grid[row][col+i]=drawing_color
            
    else:
        grid[row][col]=drawing_color
        for i in range(radius-1):
            grid[row-i][col+i]=drawing_color
            x=row-i
            y=col+i
        grid[x][y+1]=drawing_color
        for i in range(3):
            grid[x+i][y+1+i]=drawing_color
        for i in range(3,6):
             grid[x+i][y+4]=drawing_color
        grid[x+6][y+3]=drawing_color
        grid[x+7][y+2]=drawing_color    
        for i in range(radius):
            grid[row][col+i]=drawing_color  
    

def paint_using_brush(row, col, size):
    if BRUSH_SIZE == 1:
        grid[row][col] = drawing_color
    else: #for values greater than 1        
        r = row-BRUSH_SIZE+1
        c = col-BRUSH_SIZE+1
        
        for i in range(BRUSH_SIZE*2-1):
            for j in range(BRUSH_SIZE*2-1):
                if r+i<0 or c+j<0 or r+i>=ROWS or c+j>=COLS:
                    continue
                grid[r+i][c+j] = drawing_color         

def get_heart_coordinates(X,Y):
    list = []
    for i in range(3):
        list.append((X - i, Y - i))
        list.append((X - i, Y + i))
        list.append((X-3,Y-3-i))
        list.append((X - 3, Y + 3 + i))

    for i in range(2):
        list.append((X - 2 + i, Y - 6 - i))
        list.append((X - 2 + i, Y + 6 + i))
        list.append((X + i, Y - 7 ))
        list.append((X + i, Y + 7 ))

    for i in range(7):
        list.append((X + 2 + i, Y - 6 + i))
        list.append((X + 2 + i, Y + 6 - i))

    return list

def get_dotted_heart_coordinates(X,Y):
    list = []
    for i in range(3):
        #list.append((X - i, Y - i))
        list.append((X - i, Y + i))

    for i in range(3):
        list.append((X - 3, Y + 3 + i))

    for i in range(2):
        list.append((X - 2 + i, Y + 6 + i))

    for i in range(2):
        list.append((X + i, Y + 7))

    for i in range(7):
        list.append((X + 2 + i, Y + 6 - i))

    for i in range(1,7):
        list.append((X + 8 - i, Y - i))

    for i in range(2):
        list.append((X + 1 - i, Y - 7))

    for i in range(2):
        list.append((X - 1 - i, Y - 7 + i))

    for i in range(3):
        list.append((X - 3, Y - 5 + i))

    for i in range(2):
        list.append((X - 2 + i, Y - 2 + i))




    return list


def draw_heart():
    radius = 5
    pos = pygame.mouse.get_pos()
    print(pos)
    dotted = True
    x, y = get_row_col_from_pos(pos)
    if DOTTED:
         coordinates = get_dotted_heart_coordinates(x,y)
         for i in range(0,len(coordinates),2):
             x, y = coordinates[i]
             grid[x][y] = drawing_color
    else:
        coordinates = get_heart_coordinates(x, y)
        for i in coordinates:
            x,y = i
            grid[x][y] = drawing_color
            
            
def get_circle_coordinates(X,Y,radius):
    list= []
    for i in range(5):
        list.append((X-5,Y-2+i))
        list.append((X+5,Y-2+i))

    for i in range(3):
        list.append((X-2-i,Y-5+i))
        list.append((X - 2 - i, Y + 5 - i))
        list.append((X + 4 - i, Y - 3 - i))
        list.append((X + 4 - i, Y + 3 + i))

    for i in range(3):
        list.append((X-1+i,Y-5))
        list.append((X-1+i, Y+5))
    return list

def get_dotted_circle_coordinates(X,Y):
    list = []
    for i in range(5):
        list.append((X - 5, Y - 2 + i))

    for i in range(3):
        list.append((X - 2 - i, Y + 5 - i))

    for i in range(3):
       list.append((X - 1 + i, Y + 5))

    for i in range(3):
        list.append((X + 4 - i, Y + 3 + i))

    for i in range(5):
        list.append((X + 5, Y - 2 + i))

    for i in range(3):
        list.append((X + 4 - i, Y - 3 - i))

    for i in range(3):
        list.append((X - 1 + i, Y - 5))

    for i in range(3):
        list.append((X - 2 - i, Y - 5 + i))

    return list

def draw_circle():
    radius = 20
    pos = pygame.mouse.get_pos()
    
    
    x, y = get_row_col_from_pos(pos)
    if DOTTED:
        
         coordinates = get_dotted_circle_coordinates(x,y)
         for i in range(0,len(coordinates),2):
             x, y = coordinates[i]
             grid[x][y] = drawing_color
    else:
        """
        pygame.draw.circle(WIN, BLACK, pos, radius)
        
        pygame.display.flip()
        
        """
        coordinates = get_circle_coordinates(x, y, radius)
        for i in coordinates:
            x, y = i
            grid[x][y] = drawing_color
            
# Checks whether the coordinated are within the canvas
def inBounds(row, col):
    if row < 0 or col < 0:
        return 0
    if row >= ROWS or col >= COLS:
        return 0
    return 1

def fill_bucket(row, col, color):
   
  # Visiting array
  vis = [[0 for i in range(101)] for j in range(101)]
     
  # Creating queue for bfs
  obj = []
     
  # Pushing pair of {x, y}
  obj.append([row, col])
     
  # Marking {x, y} as visited
  vis[row][col] = 1
     
  # Until queue is empty
  while len(obj) > 0:
     
    # Extracting front pair
    coord = obj[0]
    x = coord[0]
    y = coord[1]
    preColor = grid[x][y]
   
    grid[x][y] = color
       
    # Popping front pair of queue
    obj.pop(0)
   
    # For Upside Pixel or Cell
    if inBounds(x + 1, y) == 1 and vis[x + 1][y] == 0 and grid[x + 1][y] == preColor:
      obj.append([x + 1, y])
      vis[x + 1][y] = 1
       
    # For Downside Pixel or Cell
    if inBounds(x - 1, y) == 1 and vis[x - 1][y] == 0 and grid[x - 1][y] == preColor:
      obj.append([x - 1, y])
      vis[x - 1][y] = 1
       
    # For Right side Pixel or Cell
    if inBounds(x, y + 1) == 1 and vis[x][y + 1] == 0 and grid[x][y + 1] == preColor:
      obj.append([x, y + 1])
      vis[x][y + 1] = 1
       
    # For Left side Pixel or Cell
    if inBounds(x, y - 1) == 1 and vis[x][y - 1] == 0 and grid[x][y - 1] == preColor:
      obj.append([x, y - 1])
      vis[x][y - 1] = 1


run = True

clock = pygame.time.Clock()
grid = init_grid(ROWS, COLS, BG_COLOR)
drawing_color = BLACK

button_width = 40
button_height = 40
button_y_top_row = HEIGHT - TOOLBAR_HEIGHT/2  - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT/2   + 1
button_space = 42

size_small = 25
size_medium = 35
size_large = 50

rtb_x = WIDTH + RIGHT_TOOLBAR_WIDTH/2
brush_widths = [
    Button(rtb_x - size_small/2, 480, size_small, size_small, drawing_color, None, "ellipse"),    
    Button(rtb_x - size_medium/2, 510, size_medium, size_medium, drawing_color, None, "ellipse") , 
    Button(rtb_x - size_large/2, 550, size_large, size_large, drawing_color, None, "ellipse")  
]

button_y_top_row = HEIGHT - TOOLBAR_HEIGHT/2  - button_height - 1
button_y_bot_row = HEIGHT - TOOLBAR_HEIGHT/2   + 1
button_space = 42


# Adding Buttons
buttons = []

for i in range(int(len(COLORS)/2 - 2)):
    buttons.append( Button(100 + button_space * i + 35, button_y_top_row, button_width, button_height, COLORS[i]) )

for i in range(int(len(COLORS)/2 - 2)):
    buttons.append( Button(100 + button_space * i + 35, button_y_bot_row, button_width, button_height, COLORS[i + int(len(COLORS)/2)]) )

#Right toolbar buttonst
# need to add change toolbar button.
    """
for i in range(10):
    if i == 0:
        buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,name="Change"))#Change toolbar buttons
    else: 
        buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,"B"+str(i-1), BLACK))#append tools
    """

buttons.append(Button(WIDTH - button_space + 35, button_y_top_row, button_width, button_height, WHITE, "Erase", BLACK))  # Erase Button
buttons.append(Button(WIDTH - button_space + 35, button_y_bot_row, button_width, button_height, WHITE, "Clear", BLACK))  # Clear Button
buttons.append(Button(WIDTH - 3*button_space + 5 + 35, button_y_top_row,button_width-5, button_height-5, name = "FillBucket",image_url="assets/paint-bucket.png")) #FillBucket
buttons.append(Button(WIDTH - 3*button_space + 45 +35, button_y_top_row,button_width-5, button_height-5, name = "Brush",image_url="assets/paint-brush.png")) #Brush

if(DRAW_CLICKED == False):
    buttons.append(Button(WIDTH - 3*button_space - 25 , button_y_top_row, button_width, button_height, WHITE,"DRAW", BLACK, name= "Draw")) 

buttons.append(Button(620, 400,button_width-5, button_height-5, name = "Line",image_url="assets/line.png")) # Line
buttons.append(Button(620, 340,button_width-5, button_height-5, name = "Curve",image_url="assets/curve.png")) # Curve


buttons.append(Button(75 , button_y_top_row, button_width, button_height, WHITE, "---", BLACK, name="Dotted")) 
buttons.append(Button(75 , button_y_bot_row, button_width, button_height, WHITE, name = 'thin')) 

draw_button = Button(5, HEIGHT - TOOLBAR_HEIGHT/2 - 30, 60, 60, drawing_color)
buttons.append(draw_button)

pos1 = [0,0]
mouse_down = False



while run:
    clock.tick(FPS) #limiting FPS to 60 or any other value

    for event in pygame.event.get():
        if event.type == pygame.QUIT:   #if user closed the program
            run = False
        
        if pygame.mouse.get_pressed()[0]:
            pos = pygame.mouse.get_pos()

            try:
                row, col = get_row_col_from_pos(pos)
                
                if STATE == "ARC":
                    draw_arc(row,col,15)
                
                if STATE == "B-spline":
                    draw_bspline()
                    
                if STATE == "LINE":

                    print("State: " + STATE)
                    pos1 = pos
                    STATE = "LINE2"
                    pygame.event.wait()
                    
                
                if STATE == "LINE2":
                    print("State: " + STATE)
                    
                    pos = pygame.mouse.get_pos()
                    draw_line(pos1, pos)

                if STATE == "HEART":
                    draw_heart()
                    
                if STATE == "CIRCLE":
                    draw_circle()
                    
                if STATE == "COLOR":
                    paint_using_brush(row, col, BRUSH_SIZE)

                elif STATE == "FILL":
                    fill_bucket(row, col, drawing_color)
                    

            except IndexError:
                for button in buttons:
                    if not button.clicked(pos):
                        continue
                    if button.text == "Clear":
                        grid = init_grid(ROWS, COLS, BG_COLOR)
                        drawing_color = BLACK
                        draw_button.color = drawing_color
                        STATE = "COLOR"
                        draw(WIN, grid, buttons)
                        break

                    if button.name == "FillBucket":                        
                        STATE = "FILL"
                        break
                    
                    if button.name == "Change":
                        Change = not Change
                        for i in range(10):
                            if i == 0:
                                buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,name="Change"))
                            else:
                                if Change == False:  
                                    buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,"B"+str(i-1), BLACK))
                                if Change == True:
                                   buttons.append(Button(HEIGHT - 2*button_width,(i*button_height)+5,button_width,button_height,WHITE,"C"+str(i-1), BLACK))
                        break
                    
                    if button.name == "Dotted":
                        DOTTED = not DOTTED
                        break
                    
                    if button.name == "Draw":
                        
                        buttons.append(Button(WIDTH - 3*button_space - 35 , button_y_bot_row,button_width-5, button_height-5, name = "Circle",image_url="assets/circle.png")) #Circle
                        buttons.append(Button(WIDTH - 3*button_space + 35 , button_y_bot_row,button_width-5, button_height-5, name = "Heart",image_url="assets/heart.png")) #Heart
                        break
                    
                    if button.name == "Curve":
                        
                        buttons.append(Button(620, 280,button_width-5, button_height-5, name = "Arc",image_url="assets/arc.png")) # 
                        buttons.append(Button(620, 220,button_width-5, button_height-5, name = "Bezier",image_url="assets/bezier.png")) 
                        buttons.append(Button(620, 160,button_width-5, button_height-5, name = "B-spline",image_url="assets/b-spline.png"))
                        break
                    
                    if button.name == "Arc":
                        STATE = "ARC"
                        break
                    
                    if button.name == "Circle":
                        STATE = "CIRCLE"
                        break
                    
                    if button.name == "Heart":
                        STATE = "HEART"
                        break
                    
                    if button.name == "Line":
                        STATE = "LINE"
                        break
                    
                    if button.name == "B-spline":
                        STATE = "B-spline"
                        break
                     
                    if button.name == "Brush":
                        STATE = "COLOR"
                        break
                    
                    drawing_color = button.color
                    draw_button.color = drawing_color
                    
                    break
                
                for button in brush_widths:
                    if not button.clicked(pos):
                        continue
                    #set brush width
                    if button.width == size_small:
                        BRUSH_SIZE = 1
                    elif button.width == size_medium:
                        BRUSH_SIZE = 2
                    elif button.width == size_large:
                        BRUSH_SIZE = 3

                    STATE = "COLOR"
        
    draw(WIN, grid, buttons)
    
pygame.quit()
