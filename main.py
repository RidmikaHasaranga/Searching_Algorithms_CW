import pygame
import random

# import DFS.py and AStar.py python files
import DFS
import AStar

# instructions for running the programme
#       1.Run the main.py
#       2.After the window(maze) popup then click the space button. (to run DFS searching algorithm)
#       3.After running the DFS searching algorithm then click  the window close button.
#       4.Again the window(maze) popup then click the space button. (to run A* searching algorithm)
#       5.After running the A* searching algorithm then click  the window close button.
#       6.Searching Algorithms summary display in debug console.


# window width and height
width = 500
height = 500
window = pygame.display.set_mode((width, height))

# Define Nodes Colors
white = (255, 255, 255)  # default nodes color
red = (255, 51, 0)  # goal node
green = (0, 204, 102)  # start node
gray = (128, 128, 128)  # barrier nodes
black = (0, 0, 0)  # node lines
orange = (255, 173, 51)  # visited nodes
yellow = (255, 255, 102)  # explored nodes
blue = (0, 102, 255)  # final path nodes

# Node class for define a single node object
class Node:
    def __init__(self, row, column, width, height, totalRows):
        self.row = row
        self.column = column
        self.x = row * width
        self.y = column * height
        self.color = white
        self.neighbors = []
        self.width = width
        self.totalRows = totalRows

    def getPosition(self):  # get node position
        return self.row, self.column

    # node checking functions
    def isClosed(self):  # check visited nodes
        return self.color == orange

    def isOpen(self):  # check explored nodes
        return self.color == yellow

    def isBarrier(self):  # check barriers node
        return self.color == gray

    def isStart(self):  # check start node
        return self.color == green

    def isGoal(self):  # check goal node
        return self.color == red

    # function for changing node color
    def reset(self):
        self.color = white  # default node color

    def makeClose(self):    # visited nodes
        self.color = orange

    def makeOpen(self):     # explored nodes
        self.color = yellow

    def makeBarrier(self):   # barriers node
        self.color = gray

    def makeStart(self):      # start node
        self.color = green

    def makeGoal(self):   # goal node
        self.color = red

    def makePath(self):     # final path node
        self.color = blue

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbours(self, maze):
        self.neighbors = []     # neighbour nodes

        # Check Directions (horizontal, vertical and diagonal)
        # North West
        if self.row - 1 >= 0 and self.column - 1 >= 0 and not maze[self.row - 1][self.column - 1].isBarrier():
            self.neighbors.append(maze[self.row - 1][self.column - 1])

        # West
        if self.column - 1 >= 0 and not maze[self.row][self.column - 1].isBarrier():
            self.neighbors.append(maze[self.row][self.column - 1])

        # South West
        if self.row + 1 < self.totalRows and self.column - 1 >= 0 and not maze[self.row + 1][self.column - 1].isBarrier():
            self.neighbors.append(maze[self.row + 1][self.column - 1])

        # North
        if self.row - 1 >= 0 and not maze[self.row - 1][self.column].isBarrier():
            self.neighbors.append(maze[self.row - 1][self.column])

        # South
        if self.row + 1 < self.totalRows and not maze[self.row + 1][self.column].isBarrier():
            self.neighbors.append(maze[self.row + 1][self.column])

        # North East
        if self.row - 1 >= 0 and self.column + 1 < self.totalRows and not maze[self.row - 1][self.column + 1].isBarrier():
            self.neighbors.append(maze[self.row - 1][self.column + 1])

        # East
        if self.column + 1 < self.totalRows and not maze[self.row][self.column + 1].isBarrier():
            self.neighbors.append(maze[self.row][self.column + 1])

        # South East
        if self.row + 1 < self.totalRows and self.column + 1 < self.totalRows and not maze[self.row + 1][self.column + 1].isBarrier():
            self.neighbors.append(maze[self.row + 1][self.column + 1])

    def __lt__(self, other):   # default function
        return False

# create maze variable
def createMaze(rows, width):
    maze = []
    gap = width // rows  # Total width divided by num of rows for one node gap
    for i in range(rows):
        maze.append([])
        for j in range(rows):
            node = Node(i, j, gap, gap, rows)
            maze[i].append(node)
    return maze

def draw(window, maze, rows, width):
    window.fill(white)  # fill window with white color
    for row in maze:
        for node in row:
            node.draw(window)

    # draw node lines
    gap = width // rows  # Total width divided by num of rows for one node gap
    for i in range(rows):
        pygame.draw.line(window, black, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(window, black, (j * gap, 0), (j * gap, width))

    pygame.display.update()

# function for select Nodes randomly -- call in createPreNodes function
def getRandomCoordinates(minimumX, maximumX, minimumY, maximumY):
    xCoordinate = random.randint(minimumX, maximumX)
    yCoordinate = random.randint(minimumY, maximumY)
    return xCoordinate, yCoordinate

# select start, goal, 4 barrier nodes
def createPreNodes(maze, rows):
    startRow, startColumn = getRandomCoordinates(0, 1, 0, rows - 1)
    goalRow, goalColumn = getRandomCoordinates(rows - 2, rows - 1, 0, rows - 1)
    startNode = maze[startRow][startColumn]
    start = startNode
    start.makeStart()
    goalNode = maze[goalRow][goalColumn]
    goal = goalNode
    goal.makeGoal()
    noOfBarriers = 4
    for i in range(noOfBarriers):
        barrierColumn, barrierRow = getRandomCoordinates(0, rows - 1, 0, rows - 1)
        barrierNode = maze[barrierRow][barrierColumn]
        while True:
            if barrierNode != start and barrierNode != goal and not barrierNode.isBarrier():
                barrierNode.makeBarrier()
                break
            barrierColumn, barrierRow = getRandomCoordinates(0, rows - 1, 0, rows - 1)
            barrierNode = maze[barrierRow][barrierColumn]
    return start, goal  # when exploring nodes (to initiate start and goal nodes again)

# for rearrange Maze -- after running DFS Algo reset for A* Algo
def resetMaze(maze, start, goal):
    for row in maze:
        for node in row:
            if node.getPosition() != start and node.getPosition() != goal and not node.isBarrier():
                node.reset()
    start.makeStart()
    goal.makeGoal()
    return maze

# for run DFS and A* separately
def main(window, width):
    aStarVisitedCount = 0
    dfsVisitedCount = 0
    rows = 6

    pygame.display.set_caption("DFS Search Algorithm")
    maze = createMaze(rows, width)
    start, goal = createPreNodes(maze, rows)
    run = True
    while run:
        draw(window, maze, rows, width)

        # For popup window close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in maze:
                        for node in row:
                            node.updateNeighbours(maze)
                    dfsVisitedCount, status = DFS.dfs(lambda: draw(window, maze, rows, width), start, goal)

    pygame.display.set_caption("A* Search Algorithm")
    maze = resetMaze(maze, start, goal)
    run = True
    while run:
        draw(window, maze, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for row in maze:
                        for node in row:
                            node.updateNeighbours(maze)
                    aStarVisitedCount, status = AStar.aStar(lambda: draw(window, maze, rows, width), maze, start, goal)

    pygame.quit()
    print()
    print("\nDFS search algorithm visited: " + str(dfsVisitedCount) + " nodes (takes " + str(dfsVisitedCount) + " minute)")
    print("A* search algorithm visited:  " + str(aStarVisitedCount) + " nodes (takes " + str(aStarVisitedCount) + " minute)")

    if (aStarVisitedCount < dfsVisitedCount):
        print("\nThe A* searching algorithm saves more time than the DFS searching algorithm")
        print("Difference between A* & DFS Searching Algorithms: " + str(dfsVisitedCount - aStarVisitedCount) + " minute (1 minute for 1 node)")
    else:
        print("\nThe DFS searching algorithm saves more time than the A* searching algorithm")
        print("Difference between DFS & A* Searching Algorithms: " + str(aStarVisitedCount - dfsVisitedCount) + " minute")

# Call main function
main(window, width)
