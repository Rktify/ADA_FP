import pygame
from tkinter import messagebox, Tk
import sys
import tracemalloc
import time
import math
from random import randint
from .. import Redirect

def main():
    width, height = 600, 600
    columns, rows = 30, 30
    window = pygame.display.set_mode((width, height))

    pixelwidth = width // columns
    pixelheight = height // rows

    grid = []
    queue, closedqueue = [], []
    pathing = []

    class Box:
        def __init__ (self, i, j):
            self.x = i
            self.y = j
            self.f, self.g, self.h = 0, 0, 0
            self.obstacle = False
            self.start = False
            self.end = False
            self.obstaclestatus = False
            self.next = False
            self.visited = False
            self.neighbours = []
            self.path = None
            

        def draw(self, win, color):
            pygame.draw.rect(win, color, (self.x * pixelwidth, self.y * pixelheight, pixelwidth - 2, pixelheight - 2))

        def set_neighbours(self):
            if self.x > 0:
                self.neighbours.append(grid[self.x - 1][self.y])
            if self.x < columns - 1:
                self.neighbours.append(grid[self.x + 1][self.y])
            if self.y > 0:
                self.neighbours.append(grid[self.x][self.y - 1])
            if self.y < rows - 1:
                self.neighbours.append(grid[self.x][self.y + 1])
            
            if self.x < columns - 1 and self.y < rows - 1:
                self.neighbours.append(grid[self.x+1][self.y+1])
            if self.x < columns - 1 and self.y > 0:
                self.neighbours.append(grid[self.x+1][self.y-1])
            if self.x > 0 and self.y < rows - 1:
                self.neighbours.append(grid[self.x-1][self.y+1])
            if self.x > 0 and self.y > 0:
                self.neighbours.append(grid[self.x-1][self.y-1])

    for i in range(columns):
        arr = []
        for j in range(rows):
            arr.append(Box(i, j))
        grid.append(arr)

    for i in range(columns):
        for j in range(rows):
            grid[i][j].set_neighbours()

    def heuristics(a, b):
        return math.sqrt((a.x - b.x)**2 + abs(a.y - b.y)**2)

    def main2():
        global elapsed, memory
        search = False
        endboxstatus = False
        startboxstatus = False
        searching = True
        endzone = None
        finish = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    Redirect.goMenu()
                elif event.type == pygame.MOUSEMOTION:
                    x = pygame.mouse.get_pos()[0]
                    y = pygame.mouse.get_pos()[1]
                    i = x // pixelwidth
                    j = y // pixelheight
                    if event.buttons[0] and not grid[i][j].obstaclestatus and not startboxstatus:
                        start_box = grid[i][j]
                        start_box.start = True
                        startboxstatus = True
                        grid[i][j].visited = True
                        queue.append(grid[i][j])
                    if event.buttons[0] and endboxstatus and startboxstatus and not finish:
                        grid[i][j].obstacle = True
                        grid[i][j].obstaclestatus = True
                    if event.buttons[2] and not endboxstatus and not grid[i][j].obstaclestatus:
                        endzone = grid[i][j]
                        endzone.end = True
                        endboxstatus = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE and searching and not finish:
                        for i in range(columns):
                            for j in range(rows):
                                box = grid[i][j]
                                if box.obstacle:
                                    box.obstacle = False
                                    box.obstaclestatus = False
                    if event.key == pygame.K_SPACE and endboxstatus and not finish:
                        for i in range(columns):
                            for j in range(rows):
                                box = grid[i][j]
                                if box.end:
                                    box.end = False
                                    endboxstatus = False
                    if event.key == pygame.K_r:
                        for i in range(columns):
                            for j in range(rows):
                                box = grid[i][j]
                                box.obstacle = False
                                box.obstaclestatus = False
                                box.end = False
                                box.next = False
                                box.visited = False
                                box.start = False
                                box.path = None
                                endboxstatus = False
                                startboxstatus = False
                                finish = False
                                searching = True
                                search = False
                                queue.clear()
                                pathing.clear()
                                closedqueue.clear()

                    if event.key == pygame.K_v:
                        for i in range(columns):
                            for j in range(rows):
                                box = grid[i][j]
                                if randint(0, 100) < 40:
                                    if box != start_box and box != endzone:
                                        box.obstacle = True
                                        box.obstaclestatus = True

                if event.type == pygame.KEYDOWN and endboxstatus:
                    if event.key == pygame.K_RETURN:
                        timestart = time.time()
                        search = True
            if search:
                tracemalloc.start()
                if len(queue) > 0 and searching:
                    win = 0
                    for i in range(len(queue)):
                        if queue[i].f < queue[win].f:
                            win = i
                    currentpixel = queue[win]
                    if currentpixel == endzone:
                        temp = currentpixel
                        while temp.path:
                            pathing.append(temp.path)
                            temp = temp.path
                        if not finish:
                            finish = True
                        elif finish:
                            continue
                    if finish == False:
                        queue.remove(currentpixel)
                        closedqueue.append(currentpixel)
                        for i in currentpixel.neighbours:
                            if i in closedqueue or i.obstacle:
                                continue
                            tempG = currentpixel.g + 1

                            newPath = False
                            if i in queue:
                                if tempG < i.g:
                                    i.g = tempG
                                    newPath = True
                            else:
                                i.g = tempG
                                newPath = True
                                queue.append(i)
                            if newPath:
                                i.h = heuristics(i, endzone)
                                i.f = i.g + i.h
                                i.path = currentpixel
                                i.next = True
                else:
                    if searching:
                        Tk().wm_withdraw()
                        messagebox.showinfo("pls", "NO PATH!!!!!!!!!!!!")
                        searching = False
                        finish = True

            if finish:
                search = False
                timeend = time.time()
                elapsed = timeend - timestart
                currentmemory, memorypeak = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                queue.clear()
                Tk().wm_withdraw()
                messagebox.showinfo("Time and memory", f"Time: %.2fs  | Memory: {memorypeak} bytes" % elapsed)

                finish = False

            window.fill((0, 0, 0))

            for i in range(columns):
                for j in range(rows):
                    box = grid[i][j]
                    box.draw(window, (221, 221, 221))
                    if box.next:
                        box.draw(window, (0, 0, 255))
                    if box in closedqueue:
                        box.draw(window, (0, 200, 0))
                    if box.start and not box.end:
                        box.draw(window, (0, 200, 200))
                    if box.obstacle and not box.start and not box.end:
                        box.draw(window, (255, 255, 0))
                    if box in pathing:
                        box.draw(window, (0, 0, 0))
                    if box.end and not box.start:
                        box.draw(window, (255, 0, 0))

            pygame.display.flip()
            pygame.display.set_caption("A* Algorithm Visualization")
    main2()