import pygame
import time
from queue import PriorityQueue

def heuristicCost(currNode, goalNode):
    currNodeY, currNodeX = currNode
    goalNodeY, goalNodeX = goalNode
    return max(abs(currNodeX - goalNodeX), abs(currNodeY - goalNodeY))

def aStar(draw, maze, start, goal):

    # to get final A* path
    def aStarFinalPath(cameFrom, currNode, draw):
        while currNode in cameFrom:
            currNode = cameFrom[currNode]
            currNode.makePath()
            draw()

    count = 0 # for - what time did node come
    visitedCount = 0
    frontier = PriorityQueue()  # for get H cost Ascendant order
    frontier.put((0, count, start))  # 0 - A* Score
    cameFrom = {}
    gScore = {node: float("inf") for row in maze for node in row} # gScore - actual cost , 'inf' - infinity
    gScore[start] = 0
    AStarScore = {node: float("inf") for row in maze for node in row}  #A* Score = actual cost + H cost
    AStarScore[start] = heuristicCost(start.getPosition(), goal.getPosition())
    frontierList = {start}  # frontier variable is priority queue. Therefor we can not look what are the elements.
    while not frontier.empty():

        # For popup window close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        currNode = frontier.get()[2]  # node value eke index eka 2
        frontierList.remove(currNode)
        visitedCount += 1
        if currNode == goal:
            aStarFinalPath(cameFrom, goal, draw)
            start.makeStart()
            goal.makeGoal()
            return visitedCount - 1, True
        for neighbor in currNode.neighbors:
            tempGScore = gScore[currNode] + 1
            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = currNode
                gScore[neighbor] = tempGScore
                AStarScore[neighbor] = tempGScore + heuristicCost(neighbor.getPosition(), goal.getPosition())
                if neighbor not in frontierList:  # That's why created frontier list for check at this moment
                    count += 1
                    frontier.put((AStarScore[neighbor], count, neighbor))
                    frontierList.add(neighbor)
                    neighbor.makeOpen()
        goal.makeGoal()
        draw()
        time.sleep(0.5)
        if currNode != start:
            currNode.makeClose()
    return 0, False