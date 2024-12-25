
# solution found in 10951000 iterations
# BFS (very slow but only way i got this to work)
# creates a pretty big (500mb) pickle file for backup

import pickle
import os
from main import logic
from collections import deque

class Solution:
    def __init__(self):
        self.logic = logic()
        
    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()

        with open("solution.pkl", "wb") as temp_file:
            pickle.dump(path, temp_file)
        return path


    def getAllNeighbours(self, grid):
        #print(grid)
        moves = []
        neighbours = []
        for i in range(1, 11):

            ind = grid.index(i)


            legalMoves = self.logic.legalMoves(grid, ind)


            if True in legalMoves:
                moves.append([ind, legalMoves])

        #print(moves)
        for move in moves:
            dir = [i for i, x in enumerate(move[1]) if x == True]

            for d in dir:
                neighbours.append(tuple(self.logic.makeMove(grid.copy(), d, move[0]).copy())) # index can be many!!!
            #self.logic.undoMove()
        return neighbours

    def bfs(self, start):
        # Initialize the queue with the starting node
        if os.path.exists("data.pkl"):
            with open("data.pkl", "rb") as file:
                length, queue, visited, came_from = pickle.load(file)
        else:
            length = 0
            queue = deque([tuple(start)])
        
            # Keep track of visited nodes
            visited = set()
            visited.add(tuple(start))
        
            # Keep track of the parent of each node to reconstruct the path
            came_from = {}


        while queue:
            # Dequeue the first node in the queue
            current = queue.popleft()
            
            # Debug: Print current state
            #print("Current State:", current)

            
            length += 1

            if length % 1000 == 0:
                print(f"Iteration: {length} | current state: {current}")

            if length % 1000000 == 0: # cache every 1000000
                print("saving checkpoint")
                with open("data_temp.pkl", "wb") as temp_file:
                    pickle.dump((length, queue, visited, came_from), temp_file)
                os.replace("data_temp.pkl", "data.pkl")

        
            # If the goal is reached, reconstruct the path
            if self.logic.checkWin(list(current)):
                #print("Winning State Found:", current)  # Debug
                return self.reconstruct_path(came_from, current)
            
            # Explore neighbors
            neighbors = self.getAllNeighbours(list(current))
            #print("Neighbors:", neighbors)  # Debug
            for neighbor in neighbors:
                if neighbor not in visited:
                    visited.add(neighbor)
                    came_from[neighbor] = current
                    
                    queue.append(neighbor)
                    # Debug: Print added neighbor
                    #print("Added Neighbor:", neighbor)
        
        # If we exit the loop, no solution was found
        print("No solution found.")  # Debug
        return None  # No path found

if __name__ == "__main__":

    grid = [1, 2, 2, 3,
            1, 2, 2, 3,
            4, 5, 5, 6,
            4, 0, 0, 6,
            7, 8, 9, 10]
    sol = Solution()
    m = sol.bfs(grid)
    #m = sol.getAllNeighbours(grid)
    print(m)