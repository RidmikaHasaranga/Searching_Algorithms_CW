import pygame
import time

def dfs(draw, start, goal):
    explored = [start]
    frontier = [start]
    visited = []
    dfsPath = {}
    while len(frontier) > 0:

        # For popup window close button
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        currNode = frontier.pop()
        visited.append(currNode)
        if currNode == goal:

            # to get final DFS path
            cell = goal
            while cell != start:
                node = dfsPath[cell]
                node.makePath()
                cell = node
                draw()

            goal.makeGoal()
            start.makeStart()
            return len(visited), True

        for neighbor in reversed(currNode.neighbors):# node class array - curr_node.neighbors
            if neighbor not in explored:
                frontier.append(neighbor)
                explored.append(neighbor)
                dfsPath[neighbor] = currNode
                neighbor.makeOpen()
        if currNode != start:
            currNode.makeClose()
        goal.makeGoal() # explore karan yana kota yellow wena nisa
        draw()
        time.sleep(0.5)
    return len(visited), False