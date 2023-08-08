from .MapLoader import GridMap
from .ScenLoader import Agent
import queue

class TEGClassic:
	def __init__(self, agents: list, map: GridMap):
		self.map = map
		self.agents = agents
		self.distFromStart = [None] * len(agents) # list of distances from start to each vertex for each agent
		self.distToGoal = [None] * len(agents) # list of distances from each vertex to goal for each agent

	def getDistancesFromStart(self, agent: int) -> list:
		v = self.map.map[self.agents[agent].y_start][self.agents[agent].x_start]
		if self.distFromStart[agent] == None:
			self.distFromStart[agent] = self.bfs(v)
		return self.distFromStart[agent]

	def getDistancesFromGoal(self, agent: int) -> list:
		v = self.map.map[self.agents[agent].y_goal][self.agents[agent].x_goal]
		if self.distToGoal[agent] == None:
			self.distToGoal[agent] = self.bfs(v)
		return self.distToGoal[agent]

	def getStartGoalDistance(self, agent: int) -> int:
		s = self.map.map[self.agents[agent].y_start][self.agents[agent].x_start]
		g = self.map.map[self.agents[agent].y_goal][self.agents[agent].x_goal]
		if self.distFromStart[agent] == None:
			self.distFromStart[agent] = self.bfs(s)
		return self.distFromStart[agent][g]

	def getMksLb(self, agent: int) -> int:
		mks = 0
		for a in range(agent):
			mks = max(mks, self.getStartGoalDistance(a))
		return mks + 1

	def getSoCLb(self, agent: int) -> int:
		soc = 0
		for a in range(agent):
			soc = soc + self.getStartGoalDistance(a) + 1
		return soc
	
	def isReachable(self, agent: int, vertex: int, t: int, maxT: int) ->bool:
		fromStart = self.getDistancesFromStart(agent)
		fromGoal = self.getDistancesFromGoal(agent)
		if (fromStart[vertex] <= t and fromGoal[vertex] < maxT-t):
			return True
		return False

	def bfs(self, s):
		distanceList = [-1] * (self.map.numVertices) # unreached vertices (all initially)
		# distance = 0	# distance from s to g
		visited = [False] * (self.map.numVertices)   # mark all vertices as not visited

		queue = []  # create queue for bfs
		
		# enqueue source node and mark is as visited
		queue.append(s)
		visited[s] = True
		distanceList[s] = 0 

		while queue:
			s = queue.pop(0)
			for i in self.map.getNeighboursIDsShort(s):
				if not visited[i]:
					queue.append(i)
					visited[i] = True
					distanceList[i] = distanceList[s] + 1

		return distanceList