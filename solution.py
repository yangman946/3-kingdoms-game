# use DFS to create a solution
# Minimax search???

from main import logic
import random

class Solution:
    def __init__(self, grid):
        self.logic = logic()
        self.grid = grid
        self.gridsequence = []
        self.moveshistory = []
        self.depth = 7
        
    def moveLogic(self, grid): # output the collection of grids
        self.grid = grid
        bestgrid = []
        bestscore = -10000

        moves = self.getAllLegalMoves(self.grid) # get first set of legal moves
        #print(f"moves: {moves}")
        random.shuffle(moves)
        #print(f"random: {moves}")

        for move in moves: # move each legal move

            #print(moves)
            #print(f"playing move {move[0]}")

            # make the move
            newGrid = self.logic.makeMove(self.grid.copy(), move[1].index(True), move[0]) # grid, move to make, index to move
            score = self.recursion(newGrid, self.depth) # depth of 10? evaluate the grid
            self.logic.undoMove()

            if score > bestscore:
                bestscore = score
                bestgrid = newGrid
            
        self.gridsequence.append(bestgrid.copy()) # only append when a good move is certain
        #result = self.gridsequence[::-1] #ignore for now
        #result[-1] = self.grid
                
        print(f"FINAL: bestscore - {bestscore}")
        print(f"bestgrid {bestgrid}")
        self.moveshistory.append(bestgrid.copy())

        #self.MovesToPlay.append(bestmove)
        return bestgrid.copy()

    def getAllLegalMoves(self, grid):
        #print(grid)
        moves = []
        for i in range(1, 11):

            ind = grid.index(i)


            legalMoves = self.logic.legalMoves(grid, ind)


            if True in legalMoves:
                moves.append([ind, legalMoves])

        
        return moves

    def recursion(self, grid, depth): # recursion? each depth
        
        # first get root indicies of all pieces
        # next find all possible legal moves for pieces
        #bestgrid = []
            
        moves = self.getAllLegalMoves(grid) # WHY IS IT STILL PLAYING ILLEGAL MOVES????
        random.shuffle(moves)
        if len(moves) == 0: # dead end is always a lose
            return -10000
        
        if grid in self.moveshistory[-10:]: # if repetition
            return self.moveshistory[-10:].index(grid) * -100
        
        if self.logic.checkWin(grid): # if win achieved
            return 10000
        

        if depth == 0: # if we ran out of depth
            score = grid.index(2)
            return score * 10 # maybe check how close we were to winning (dist to bottom?)
        

        bestScore = -10000 

        #print(moves)

        for move in moves:

            #print(f"playing move {move[0]}:{move[1]}:{move[1].index(True)}")
            newGrid = self.logic.makeMove(grid.copy(), move[1].index(True), move[0])
            score = self.recursion(newGrid, depth-1)
            self.logic.undoMove() # undo the move

            if score > bestScore:
                bestScore = score
                #bestgrid = newGrid # we have a new best grid

        #self.gridsequence.append(bestgrid.copy()) # should we make this move?
        
        
        #print(f"{depth}: bestscore - {bestScore}")
    
        # for each legal move, play the move and evaluate next position
        # recursion
        # unmake the move
        # determine score
        return bestScore

        # will return array of tuple [Piece, index of legal move]


if __name__ == "__main__":

    grid = [1, 2, 2, 3,
            1, 2, 2, 3,
            4, 5, 5, 6,
            4, 0, 0, 6,
            7, 8, 9, 10]
    sol = Solution(grid=grid)
    m = sol.moveLogic()
    print(m)