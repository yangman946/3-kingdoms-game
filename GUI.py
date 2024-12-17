import pygame

from main import logic

class GUI:
    def __init__(self):
        pygame.init()
        self.width = 576
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill((0, 0, 0))
        
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0

        
        self.grid = [1, 2, 2, 3,
                     1, 2, 2, 3,
                     4, 5, 5, 6,
                     4, 0, 0, 6,
                     7, 8, 9, 10]
        

        #self.grid = [1, 2, 2, 3, 1, 2, 2, 3, 5, 5, 9, 6, 0, 4, 8, 6, 0, 4, 7, 10]
        #self.grid = [1, 6, 10, 3, 1, 6, 7, 3, 5, 5, 2, 2, 9, 4, 2, 2, 8, 4, 0, 0]
        
        self.counts = [0, 2, 4, 2, 2, 2, 2, 1, 1, 1, 1]
        
        # wood, black, white, red
        self.colors = {
            "wood":(144, 90, 56), 
            "black": (0, 0, 0), 
            "white": (200, 200, 200), 
            "red": (255, 0, 0)
            }
        
        self.logic = logic()

        self.render = False # trigger when rendering legal moves
        self.index = 0
        self.moves = []
        self.location = []
        self.padding = 20

    def run(self):
        while self.running:
            # poll for events
            self.screen.fill((0, 0, 0))
            self.drawBlocks()

            if self.render:
                self.drawLegalMoves(self.index, self.moves)
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                p = pygame.key.get_pressed()
                if p[pygame.K_u]:
                    self.undo()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseX, mouseY = pygame.mouse.get_pos()
                    self.translate(mouseX, mouseY)
            pygame.display.update()

    def drawLegalMoves(self, index, legalmoves):
        row, col = self.logic.index2rowcol(index)
        x = col * self.width/4
        y = row * self.height/5
        #print(x, y)

        piece = self.grid[index]
        width, height = self.logic.getDimensions(piece)

        self.location.clear()
        for i, move in enumerate(legalmoves):
            if move:
                if i == 0: # up
                    pygame.draw.polygon(self.screen, self.colors['white'], ((x+self.padding,y-self.padding),(x+(self.width/8 * width),y-self.height/10),(x+(self.width/4 * width) - self.padding,y-self.padding)))
                    self.location.append([x, y, x+(self.width/4 * width), y-self.height/10, i])
                elif i == 1: #down
                    pygame.draw.polygon(self.screen, self.colors['white'], ((x+self.padding,y+(self.height/5) * height +self.padding),(x+(self.width/8 * width),y+(self.height/5) * height + self.height/10),(x+(self.width/4 * width) - self.padding,y+(self.height/5) * height +self.padding)))
                    self.location.append([x, y+(self.height/5) * height + self.height/10, x+(self.width/4 * width), y+(self.height/5) * height, i])
                elif i == 2: # left
                    pygame.draw.polygon(self.screen, self.colors['white'], ((x-self.padding,y+self.padding),(x-self.width/8,y + self.height/10 * height),(x - self.padding, y+(self.height/5) * height - self.padding)))
                    self.location.append([x-self.width/8, y+(self.height/5) * height, x, y, i])
                elif i == 3: # right
                    pygame.draw.polygon(self.screen, self.colors['white'], ((x+(self.width/4 * width) + self.padding,y+self.padding),(x+(self.width/4 * width) +self.width/8,y + self.height/10 * height),(x+(self.width/4 * width) + self.padding, y+(self.height/5) * height - self.padding)))
                    self.location.append([x+(self.width/4 * width), y+(self.height/5) * height, x+(self.width/4 * width) +self.width/8, y, i])
        pygame.display.flip()
        
    def undo(self):
        if not self.render:
            g = self.logic.undoMove()
            if g != None:
                self.grid = g

    def drawBlocks(self, indexAnim = 0):
        i = 0
        count = [0, 2, 4, 2, 2, 2, 2, 1, 1, 1, 1]
        
        for y in range(0, self.height, int(self.height/5)):
            for x in range(0, self.width, int(self.width/4)):
                rect = pygame.Rect(x, y, self.width/4, self.height/5)

                if self.counts[self.grid[i]] == 1:
                    pygame.draw.rect(self.screen, self.colors["wood"], rect)
                    pygame.draw.rect(self.screen, self.colors["black"], rect, 1)
                    pygame.draw.circle(self.screen, self.colors["red"], (x + self.width/8, y + self.height/10), 20)
                if self.counts[self.grid[i]] == 2:
                    if count[self.grid[i]] == 2:
                        
                    
                        if self.grid[i] == 5:
                            rect = pygame.Rect(x, y, self.width/4 * 2, self.height/5)
                            pygame.draw.rect(self.screen, self.colors["wood"], rect)
                            pygame.draw.rect(self.screen, self.colors["black"], rect, 1)
                            pygame.draw.circle(self.screen, self.colors["black"], (x + self.width/4, y + self.height/10), 20)
                        else:
                            rect = pygame.Rect(x, y, self.width/4, self.height/5 * 2)
                            pygame.draw.rect(self.screen, self.colors["wood"], rect)
                            pygame.draw.rect(self.screen, self.colors["black"], rect, 1)
                            pygame.draw.circle(self.screen, self.colors["black"], (x + self.width/8, y + self.height/5), 20)
                        
                        count[self.grid[i]] -= 1

                if self.counts[self.grid[i]] == 4:
                    if count[self.grid[i]] == 4:
                        rect = pygame.Rect(x, y, self.width/4 * 2, self.height/5 * 2)
                        pygame.draw.rect(self.screen, self.colors["wood"], rect)
                        pygame.draw.rect(self.screen, self.colors["black"], rect, 1)
                        pygame.draw.circle(self.screen, self.colors["white"], (x + self.width/4, y + self.height/5), 20)
                        count[self.grid[i]] -= 1
                    
                i += 1




    def translate(self, cursor_x, cursor_y):

        if self.render == True: # check if clicking on legal moves
            makeMove = False
            move = 0
            
            for i in self.location:
                print(i)
                print(cursor_x, cursor_y)
                if i[0] <= cursor_x <= i[2]:
                    if i[3] <= cursor_y <= i[1]:
                        makeMove = True
                        move = i[4]
                        break

            if makeMove:
                print(f"MOVE {move} CHOSEN for {self.index}")
                # MAKE MOVE
                self.grid = self.logic.makeMove(self.grid, move, self.index) # animate???
                print(self.grid)
                if self.logic.checkWin(self.grid):
                    print("GAME WON!")
                    pass

            self.render = False
            self.index = 0
            self.moves = []
            self.location = []
        else:
            
            # otherwise identify what piece is clicked 
            print(cursor_x, cursor_y)
            x = int(cursor_x/self.width * 4)
            y = int(cursor_y/self.height * 5)


            print(x,y) # identified row/col

            
            id = self.logic.colrow2index(x,y)
            
            print(self.grid[id]) # identified piece
            if self.grid[id] == 0:
                return

            ind = self.grid.index(self.grid[id])

            print(ind)

            moves = self.logic.legalMoves(self.grid, ind)

            print(moves) # computed legal moves

            if len(moves) > 0:
                self.render = True
                self.moves = moves
                self.index = ind
            pass


    
g = GUI()
g.run()