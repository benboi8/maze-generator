import pygame as pg
import random
import math

pg.init()
clock = pg.time.Clock()

width, height = 800, 800
screen = pg.display.set_mode((width, height))

running = True


fps = 60


black = (0, 0, 0)
white = (255, 255, 255)
lightGray = (205, 205, 205)
darkGray = (55, 55, 55)
red = (200, 0, 0)
green = (0, 200, 0)
blue = (0, 0, 200)
orange = (255, 145, 0)
lightRed = (184, 39, 39)
lightGreen = (0, 255, 48)
lightBlue = (20, 152, 215)
pink = (204, 126, 183)
lightBlack = (45, 45, 45)
darkWhite = (215, 215, 215)


gridSize = 20
grid = []
stack = []
path = []

endReached = False
showPath = False
finished = False
start = False

def CreateGrid():
	global cols, rows, current, startPoint, endPoint
	cols = math.floor(width / gridSize)
	rows = math.floor(height / gridSize)

	for y in range(rows):
		for x in range(cols):
			grid.append(Cell(x, y, (lightBlue, (100, 100, 100), (50, 50, 50))))

	current = grid[0]
	startPoint = current
	# endPoint = grid[random.randint(1, len(grid)-1)]
	endPoint = grid[-1]


class Cell:
	def __init__(self, x, y, colors):
		self.x = x
		self.y = y
		self.walls = {
			"top": True, 
			"right": True, 
			"bottom": True, 
			"left": True
		}
		self.visited = False
		self.colors = colors
		self.numOfNeighbours = 0

	def Draw(self):
		if self in path and showPath:
			self.activeColor = self.colors[2]
		else:
			self.activeColor = self.colors[1]

		x = self.x * gridSize
		y = self.y * gridSize
		
		if self.visited:
			pg.draw.rect(screen, self.activeColor, (x, y, gridSize, gridSize))

		if self.walls["top"]:
			pg.draw.line(screen, self.colors[0], (x, y), (x + gridSize, y))
		if self.walls["right"]:
			pg.draw.line(screen, self.colors[0], (x + gridSize, y), (x + gridSize, y + gridSize))
		if self.walls["bottom"]:
			pg.draw.line(screen, self.colors[0], (x + gridSize, y + gridSize), (x, y + gridSize))
		if self.walls["left"]:
			pg.draw.line(screen, self.colors[0], (x, y + gridSize), (x, y))


	def Index(self, x, y):
		if (x < 0 or y < 0 or x > cols - 1 or y > rows - 1):
			return None
		else:
			return x + y * cols

	def CheckNeighbors(self):
		neighbours = []
		try:
			top = grid[self.Index(self.x, self.y - 1)]
		except TypeError:
			top = None
		try:
			right = grid[self.Index(self.x + 1, self.y)]
		except TypeError:
			right = None
		try:
			bottom = grid[self.Index(self.x, self.y + 1)]
		except TypeError:
			bottom = None
		try:
			left = grid[self.Index(self.x - 1, self.y)]
		except TypeError:
			left = None

		if top != None and not top.visited:
			neighbours.append(top) 
		if right != None and not right.visited:
			neighbours.append(right)
		if bottom != None and not bottom.visited:
			neighbours.append(bottom) 
		if left != None and not left.visited:
			neighbours.append(left)

		if len(neighbours) > 0:
			self.numOfNeighbours = len(neighbours) - 1
			nextNeighbour = math.floor(random.randint(0, len(neighbours)-1))
			return neighbours[nextNeighbour]
		else:
			return None

	def Update(self):
		global current, endReached, finished, moreNeighbours
		nextNeighbour = current.CheckNeighbors()
		
		if nextNeighbour != None:
			self.visited = True
			stack.append(current)
			path.append(current)

			self.RemoveWalls(current, nextNeighbour)

			current = nextNeighbour
			if path[-1] == endPoint:
				endReached = True
				path.append(endPoint)

			if endReached:
				path.pop()

		elif len(stack) > 0:
			current = stack.pop()

			if not endReached:
				path.pop()

		elif len(stack) == 0:
			finished = True

	def RemoveWalls(self, a, b):
		x = a.x - b.x
		if x == 1:
			a.walls["left"] = False
			b.walls["right"] = False
		elif x == -1:
			a.walls["right"] = False
			b.walls["left"] = False

		y = a.y - b.y
		if y == 1:
			a.walls["top"] = False
			b.walls["bottom"] = False
		elif y == -1:
			a.walls["bottom"] = False
			b.walls["top"] = False


CreateGrid()


def DrawLoop():
	screen.fill(darkGray)

	for cell in grid:
		cell.Draw()

	if not finished:
		pg.draw.rect(screen, black, (current.x * gridSize + 1, current.y * gridSize + 1, gridSize - 2, gridSize - 2))

	pg.draw.rect(screen, red, (startPoint.x * gridSize + 1, startPoint.y * gridSize + 1, gridSize - 2, gridSize - 2))
	pg.draw.rect(screen, blue, (endPoint.x * gridSize + 1, endPoint.y * gridSize + 1, gridSize - 2, gridSize - 2))

	pg.display.update()


while running:
	clock.tick_busy_loop(fps)

	for event in pg.event.get():
		if event.type == pg.QUIT:
			running = False
		if event.type == pg.KEYDOWN:
			if event.key == pg.K_ESCAPE:
				running = False

			if event.key == pg.K_SPACE:
				start = True

			if event.key == pg.K_RETURN:
				showPath = not showPath

	if start and not finished:
		current.visited = True
		current.Update()	

	DrawLoop()