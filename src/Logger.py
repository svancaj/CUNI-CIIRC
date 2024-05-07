from .MapLoader import GridMap
from .ScenLoader import Agent

class Logger:
	def __init__(self, scenario: str, map_file: str, used_solver: str, optimized_func: str, current_agents: int, delivery = False, rotation = False):
		self.name = scenario
		self.map = map_file
		self.solver = used_solver
		self.optimized = optimized_func
		self.agents = current_agents
		self.mksLB = 0
		self.socLB = 0
		self.mksFound = 0
		self.socFound = 0
		self.pythonTime = 0
		self.clauseBuildTime = 0
		self.solverTime = 0
		self.vars = 0
		self.clauses = 0

		self.delivery = delivery
		self.rotation = rotation


	def makeOutput(self, args, agents: list, map: GridMap, plan: list, plan_file: str) -> None:

		self.getMKS(agents, map, plan)
		self.getSOC(agents, map, plan)

		# log relevant data
		log_file = "results.dat"
		sep = '\t'

		log = open(log_file, "a")

		log.write(self.name + sep +
					self.map + sep +
					self.solver + sep +
					self.optimized + sep +
					str(self.agents) + sep +
					str(self.mksLB) + sep +
					str(self.socLB) + sep +
					str(self.mksFound) + sep +
					str(self.socFound) + sep +
					str(self.pythonTime) + sep +
					str(self.clauseBuildTime) + sep +
					str(self.solverTime) + sep +
					str(self.vars) + sep +
					str(self.clauses) + sep
					)
		log.write("\n")

		log.close()

		if not args.print:
			return

		# print the plan - CIIRC
		pl = open(plan_file, "w")

		pl.write("instance=" + self.name + "\n")
		pl.write("agents=" + str(self.agents) + "\n")
		pl.write("map_file=" + self.map + "\n")
		pl.write("solver=" + self.solver + "\n")
		pl.write("solved=1" + "\n")
		pl.write("soc=" + str(self.socFound) + "\n")
		pl.write("lb_soc=" + str(self.socLB) + "\n")
		pl.write("makespan=" + str(self.mksFound) + "\n")
		pl.write("lb_makespan=" + str(self.mksLB) + "\n")
		pl.write("comp_time=" + str(self.pythonTime + self.clauseBuildTime + self.solverTime) + "\n")
		pl.write("starts=")
		for a in range(self.agents):
			pl.write("(" + str(agents[a].x_start) + "," + str(agents[a].y_start) + "),")
		pl.write("\n")
		pl.write("goals=")
		for a in range(self.agents):
			#if self.delivery:
			#	pl.write("(" + str(agents[a].x_start) + "," + str(agents[a].y_start) + "),")
			#else:
			pl.write("(" + str(agents[a].x_goal) + "," + str(agents[a].y_goal) + "),")
		pl.write("\n")
		pl.write("solution=\n")

		plan = plan[:self.mksFound]

		for t in range(len(plan)):
			pl.write(str(t) + ":")
			for a in range(len(plan[t])):
				if self.rotation:
					x,y = map.getCoords(plan[t][a][0])
					pl.write("(" + str(x) + "," + str(y) + "," + str(plan[t][a][1]) + "),")
				else:
					x,y = map.getCoords(plan[t][a])
					pl.write("(" + str(x) + "," + str(y) + "),")
			pl.write("\n")
	
		return

	def getMKS(self, agents: list, map: GridMap, plan: list) -> int:
		mks = 0
		for a in range(self.agents):
			last = plan[len(plan)-1][a]
			for t in reversed(range(len(plan))):
				if plan[t][a] != last:
					mks = max(mks, t+2)
					continue
		self.mksFound = mks
		return self.mksFound
	
	def getSOC(self, agents: list, map: GridMap, plan: list) -> int:
		soc = 0
		for a in range(self.agents):
			for t in reversed(range(len(plan))):
				if self.rotation:
					x,y = map.getCoords(plan[t][a][0])
				else:
					x,y = map.getCoords(plan[t][a])
				if self.delivery:
					if (x != agents[a].x_start or y != agents[a].y_start):
						soc += t+2
						break
				else:
					if (x != agents[a].x_goal or y != agents[a].y_goal):
						soc += t+2
						break
		self.socFound = soc
		return self.socFound