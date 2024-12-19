# main file for game logic
'''
        self.grid = [1, 2, 2, 3,
                     1, 2, 2, 3,
                     4, 5, 5, 6,
                     4, 0, 0, 6,
                     7, 8, 9, 10]
'''
class logic:
    def __init__(self):
        self.counts = [0, 2, 4, 2, 2, 2, 2, 1, 1, 1, 1]
        self.dimension = [[0, 0], [1, 2], [2, 2], [1, 2], [1, 2], [2, 1], [1, 2], [1, 1], [1, 1], [1, 1], [1, 1]]
        self.grids = []
        

    def legalMoves(self, grid, index):
        # returns array of legal moves [u, d, l, r]
        # e.g., [False, True, False, False] <-- only legal move is down
        piece = grid[index]
        size = self.counts[piece] 

        #return [True, True, True, True] # debug

        if size == 1:
            return [self.checkAbove(grid, [index]), self.checkbelow(grid, [index]), self.checkleft(grid, [index]), self.checkright(grid, [index])]
        elif size == 2:
            if piece == 5:
                return [self.checkAbove(grid, [index, index+1]), self.checkbelow(grid, [index, index+1]), self.checkleft(grid, [index]), self.checkright(grid, [index+1])]
            else:
                return [self.checkAbove(grid, [index]), self.checkbelow(grid, [index+4]), self.checkleft(grid, [index, index+4]), self.checkright(grid, [index, index+4])]
        elif size == 4:
            return [self.checkAbove(grid, [index, index+1]), self.checkbelow(grid, [index+4, index+5]), self.checkleft(grid, [index, index+4]), self.checkright(grid, [index+1, index+5])]


    

    def makeMove(self, grid, move, index):
        # returns new grid with move made
        piece = grid[index]
        x, y = self.getDimensions(piece)

        
        if move == 0: # up
            for e in range(y):
                for i in range(x): 
                    grid[index + (4*e) + i] = 0 # current selection
                    grid[index + (4*e) + i-4] = piece 
        elif move == 1: # down
            for e in range(y-1, -1, -1):
                for i in range(x): 
                    grid[index + (4*e) + i] = 0 # current selection
                    grid[index + (4*e) + i+4] = piece 
        elif move == 2: # left
            for e in range(y):
                for i in range(x): 
                    grid[index + (4*e) + i] = 0 # current selection
                    grid[index + (4*e) + i-1] = piece 
        elif move == 3: # right  
            for e in range(y):
                for i in range(x-1, -1, -1):                
                    grid[index + (4*e) + i] = 0 # current selection
                    grid[index + (4*e) + i+1] = piece               


        self.grids.append(list(grid).copy())


        return grid
        

    def checkWin(self, grid):
        return (2 in grid[-4:])

    def undoMove(self):
        # undo move
        #print(self.grids)
        if len(self.grids) > 1:

            self.grids.pop()
            return self.grids[-1]
        return None
        

    def checkAbove(self, grid, indices):
        for i in indices:
            if i - 4 < 0: # out of bounds
                return False
            elif grid[i-4] != 0: # piece is blocking
                return False
        return True
    
    def checkbelow(self, grid, indices):
        for i in indices:
            if i + 4 >= len(grid): # out of bounds
                return False
            elif grid[i+4] != 0: # piece is blocking
                return False
        return True
    
    def checkleft(self, grid, indices):
        for i in indices:
            if i - 1 < 0: # out of bounds
                return False
            elif i in [0, 4, 8, 12, 16]: # on left edge
                return False
            elif grid[i-1] != 0: # piece is blocking
                return False
        
        return True

    def checkright(self, grid, indices):
        for i in indices:
            if i + 1 >= len(grid):
                return False
            elif i in [3, 7, 11, 15, 19]: # on right edge
                return False
            elif grid[i+1] != 0: # piece is blocking
                return False
            
        return True
    
    ## HELPER FUNCTIONS

    def index2rowcol(self, index):
        row = int(index/4)
        col = index - row * 4

        return [row, col]
    
    def colrow2index(self, col, row):
        return row * 4 + col # row/col to index

    def getDimensions(self, piece):
        return self.dimension[piece]
    
    
    def isLastMove(self, grid):
        # checks if the current grid has been recently played
        if len(self.grids) < 3:
            return False
        return self.grids[-3] == grid
        
    

