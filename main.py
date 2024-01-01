import random

class worldGeneration:
   def __init__(self, height, width, rules):
       self.length = height
       self.width = width
       self.rules = rules
       self.grid = []
       for y in range(height):
           self.grid.append([])
           for x in range(width):
               self.grid[y].append(0)
       self.grid[4][8] =  (136, 187, 247)
       for i in range(10):
           self.grow()
       for i in range(10):
           self.set()
       print("done")

   def displayGrid(self):
       for row in self.grid:
           print(row)

   def grow(self):
       for y in range(len(self.grid) - 1):
           for x in range(len(self.grid[0]) - 1):
               point = self.grid[y][x]
               for y1 in range(y - 1, y + 2):
                   for x1 in range(x - 1, x + 2):
                       if 0 <= y1 < len(self.grid) and 0 <= x1 < len(self.grid[0]) and self.grid[y][x] != 0 and self.grid[y1][x1] == 0:
                           pointRule = self.rules[point]
                           self.grid[y1][x1] = pointRule[random.randint(0, len(pointRule) - 1)]

   def set(self):
       for y in range(len(self.grid) - 1):
           for x in range(len(self.grid[0]) - 1):
               point = self.grid[y][x]
               aroundCount = {(29,70,117):0,(65, 89, 117):0,(136, 187, 247):0}
               aroundCount[point] = -1
               for y1 in range(y - 1, y + 3):
                   for x1 in range(x - 1, x + 3):
                       if 0 <= y1 < len(self.grid) and 0 <= x1 < len(self.grid[0]) and self.grid[y][x] != 0:
                           aroundCount[self.grid[y1][x1]] +=1
               maxVal = max(aroundCount, key=lambda key: aroundCount[key])
               if aroundCount[maxVal] > 7 or aroundCount[self.grid[y][x]] == 0:
                   self.grid[y][x] = maxVal

   def reduce(self,reduceFactor):
       newX ,newY = 0,0
       self.length //= reduceFactor
       self.width //= reduceFactor
       newGrid = []
       for y in range(self.length):
           newGrid.append([])
           for x in range(self.width):
               newGrid[y].append(0)

       for y in range(reduceFactor//2,len(self.grid) - 1,reduceFactor):
           for x in range(reduceFactor//2,len(self.grid[0]) - 1,reduceFactor):
               aroundCount = {(29,70,117):0,(65, 89, 117):0,(136, 187, 247):0}
               temp = reduceFactor//2
               for y1 in range(y - temp, y + temp):
                   for x1 in range(x - temp, x + temp):
                       if 0 <= y1 < len(self.grid) and 0 <= x1 < len(self.grid[0]) and (y1 != y or x1 != x):
                           aroundCount[self.grid[y1][x1]] += 1
               maxVal = max(aroundCount, key=lambda key: aroundCount[key])
               self.grid[y][x] = maxVal
               newGrid[newY][newX] = maxVal
               newX+=1
           newX=0
           newY+=1


       return newGrid

   def shade(self):
       newGrid = []
       for y in range(self.length):
           newGrid.append([])
           for x in range(self.width):
               newGrid[y].append(0)

       for y in range(len(self.grid) - 1):
           for x in range( len(self.grid[0]) - 1):
               aroundCount = {(29,70,117):0,(65, 89, 117):0,(136, 187, 247):0}
               for y1 in range(y - 1, y + +2):
                   for x1 in range(x - 1, x + 2):
                       if 0 <= y1 < len(self.grid) and 0 <= x1 < len(self.grid[0]) and (y1 != y or x1 != x):
                           aroundCount[self.grid[y1][x1]] += 1

               newValue = [0, 0, 0]
               amountValues = [0, 0, 0]
               divideBy = 0
               for colour in aroundCount.keys():
                   divideBy += aroundCount[colour]
                   newValue[0] += colour[0] * aroundCount[colour]
                   amountValues[0] += colour[0]
                   newValue[1] += colour[1] * aroundCount[colour]
                   amountValues[1] += colour[1]
                   newValue[2] += colour[2] * aroundCount[colour]
                   amountValues[2] += colour[2]
               newValue[0] /= divideBy
               newValue[1] /= divideBy
               newValue[2] /= divideBy

               newGrid[y][x] = tuple(newValue)
       return newGrid

{(29,70,117):0,(65, 89, 117):0,(136, 187, 247):0}

rules = {
   (29,70,117): [(29,70,117),(65, 89, 117)],
   (65, 89, 117): [(65, 89, 117),(136, 187, 247)],
   (136, 187, 247): [(29,70,117),(136, 187, 247)],
}

g = worldGeneration(400, 600, rules)

import pygame

CELL_SIZE = 10




g.grid = g.reduce(10)
array = g.grid
array = g.shade()



rows = len(array)
cols = len(array[0])

pygame.init()

window_width = cols * CELL_SIZE
window_height = rows * CELL_SIZE

window = pygame.display.set_mode((window_width, window_height))

running = True
while running:
   for event in pygame.event.get():
       if event.type == pygame.QUIT:
           running = False

   # Draw the array on the window
   for row in range(rows):
       for col in range(cols):
           cell_value = array[row][col]
           color = cell_value

           x = col * CELL_SIZE
           y = row * CELL_SIZE

           pygame.draw.rect(window, color, (x, y, CELL_SIZE, CELL_SIZE))

   pygame.display.flip()

pygame.quit()

