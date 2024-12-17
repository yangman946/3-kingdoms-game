# use DFS to create a solution
# Minimax search???

from main import logic

class Solution:
    def __init__(self, grid):
        self.MovesToPlay = []
        self.logic = logic()
        self.grid = grid
        
    def moveLogic(self):
        bestscore = -10000
        bestmove = []

        moves = self.getAllLegalMoves(self.grid)

        for move in moves:
            for m in move[1]:
                print(moves)
                newGrid = self.logic.makeMove(self.grid, m, move[0])
                score = self.MinMax(newGrid, 0)
                self.logic.undoMove()

                if score > bestscore:
                    bestscore = score
                    bestmove = move
                

        self.MovesToPlay.append(bestmove)
        return self.MovesToPlay

    def getAllLegalMoves(self, grid):
        print(grid)
        moves = []
        for i in range(1, 11):
            ind = grid.index(i)
            legalMoves = self.logic.legalMoves(grid, ind)


            if True in legalMoves:
                moves.append([ind, legalMoves])
        return moves

    def MinMax(self, grid, depth): # recursion?
        
        # first get root indicies of all pieces
        # next find all possible legal moves for pieces
        moves = self.getAllLegalMoves(grid) # WHY IS IT STILL PLAYING ILLEGAL MOVES????
        if len(moves) == 0:
            return -10000
        if self.logic.checkWin(grid):
            return 10000
        
        bestScore = -10000

        for move in moves:
            for m in move[1]:
                newGrid = self.logic.makeMove(grid, m, move[0])
                score = self.MinMax(newGrid, depth+1)
                self.logic.undoMove()
                bestScore = max(score, bestScore)
        
        print(f"{depth}: bestscore - {bestScore}")
    
        # for each legal move, play the move and evaluate next position
        # recursion
        # unmake the move
        # determine score
        return bestScore


        # will return array of tuple [Piece, index of legal move]
grid = [1, 2, 2, 3,
        1, 2, 2, 3,
        4, 5, 5, 6,
        4, 0, 0, 6,
        7, 8, 9, 10]
sol = Solution(grid=grid)
m = sol.moveLogic()
print(m)