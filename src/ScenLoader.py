class Agent:
	def __init__(self, x_start, y_start, x_goal, y_goal):
		self.x_start = int(x_start)
		self.y_start = int(y_start)
		self.x_goal = int(x_goal)
		self.y_goal = int(y_goal)

def getAgents(filePath: str) -> list:
	with open(filePath, 'r') as reader:
		line = reader.readline() # ignore first line of file
		agents = [] # list of all agents in scenario
	
		while (True):
			line = reader.readline()
			if (not line):
				break
			words = line.split() # list of data read from line in format not-important-reference *.map-file x-size-map y-size-map x-start y-start x-goal y-goal not-important
			agents.append(Agent(words[4], words[5], words[6], words[7]))
			map_file = words[1]
	return map_file, agents
