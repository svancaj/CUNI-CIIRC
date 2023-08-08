class GridMap:
	def __init__(self, file: str):
		self.x_size = None
		self.y_size = None
		self.numVertices = None
		self.map = None
		self.map_file = file
		self.ID_to_coords = dict()
		
	def getNeighboursCoords(self, vertex: tuple[int,int]) -> list:
		(x,y) = vertex
		if x == -1 or y == -1:
			return []
		neighbourList = [(-1,-1),(-1,-1),(-1,-1),(-1,-1)] 
		if(x > 0) and self.map[y][x-1] != -1:
			neighbourList[3] = (x-1,y)
		if(x < self.x_size-1) and self.map[y][x+1] != -1:
			neighbourList[1] = (x+1,y)
		if(y > 0) and self.map[y-1][x] != -1:
			neighbourList[0] = (x,y-1)
		if(y < self.y_size-1) and self.map[y+1][x] != -1:
			neighbourList[2] = (x,y+1)
		return neighbourList
	
	def getNeighboursCoordsShort(self, vertex: tuple[int,int]) -> list:
		neighbourList = self.getNeighboursCoords(vertex)
		return [(x,y) for (x,y) in neighbourList if x >= 0]

	def getNeighboursIDs(self, vertexID: int) -> list:
		(x,y) = self.getCoords(vertexID)
		coordList = self.getNeighboursCoords((x,y))
		return [self.map[y][x] if x >= 0 else -1 for (x,y) in coordList]
	
	def getNeighboursIDsShort(self, vertexID: int) -> list:
		neighbourList = self.getNeighboursIDs(vertexID)
		return [v for v in neighbourList if v >= 0]
	
	def getCoords(self, vertexID: int) -> tuple[int, int]:
		if (vertexID in self.ID_to_coords):
			return self.ID_to_coords[vertexID]
		return (-1,-1)

def getMap(filePath: str, map_file: str) -> GridMap:
	map = GridMap(map_file)
	if filePath == None: 
		filePath = "./instances/maps/" + map_file
	with open(filePath, 'r') as reader:
		reader.readline() # Reads type of file. At present no need for it to be stored.
		map.y_size = int(reader.readline().split()[1])
		map.x_size = int(reader.readline().split()[1])
		reader.readline()   # reads the line "map"

		map.map = [[0 for x in range(map.x_size)] for y in range(map.y_size)] # initialise array filled with zeroes

		map.numVertices = 0 # vertex ids for enumeration in array
		for y in range(map.y_size):
			line = reader.readline()
			for pos in range(map.x_size):
				if line[pos] != '.':	# '.' is empty space and everything else is an obstacle
					map.map[y][pos] = -1 # obstacle
				else:
					map.map[y][pos] = map.numVertices
					map.ID_to_coords[map.numVertices] = (pos,y)
					map.numVertices += 1
	return map



