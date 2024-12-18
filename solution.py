# use DFS to create a solution
# Minimax search???

from main import logic
import heapq

class state:
    def __init__(self, grid, parent=None, move=None):
        self.grid = grid
        self.parent = parent
        self.move = move

class Solution:
    def __init__(self, grid):
        self.logic = logic()
        self.grid = grid
        self.gridsequence = []
        
    def moveLogic(self): # uses DFS algorithm - slow and takes god knows how long
        open_set = []


        initialState = state(self.grid)
        stack = [initialState]
        visited = set()
        
        while len(stack) > 0:
            currentstate = stack.pop()
            visited.add(currentstate.grid)
            if self.logic.checkWin(currentstate.grid):
                return self.construct_solution_path(currentstate)
            moves = self.getAllLegalMoves(currentstate.grid) # get first set of legal moves
            for move in moves:
                #print(move)
                nextGrid = self.logic.makeMove(currentstate.grid.copy(), move[1].index(True), move[0]) # grid, move to make, index to move
                #print(nextGrid)
                nextState = state(nextGrid.copy())
                if nextState not in visited:
                    nextState.parent = currentstate
                    stack.append(nextState)
            #print(stack)
                

        return None


    def construct_solution_path(self, state):
        path = []
        current_state = state
        while current_state is not None:
            path.append(current_state)
            current_state = current_state.parent
        path.reverse()
        return path


    def getAllLegalMoves(self, grid):
        #print(grid)
        moves = []
        for i in range(1, 11):

            ind = grid.index(i)


            legalMoves = self.logic.legalMoves(grid, ind)


            if True in legalMoves:
                moves.append([ind, legalMoves])

        #print(moves)
        return moves


grid = [1, 2, 2, 3,
        1, 2, 2, 3,
        4, 5, 5, 6,
        4, 0, 0, 6,
        7, 8, 9, 10]
sol = Solution(grid=grid)
m = sol.moveLogic()
print(m)