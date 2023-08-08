from ..MapLoader import GridMap
from ..ScenLoader import Agent
from ..Logger import Logger

def readSplit(agents: int, file: str, log: Logger) -> list:
	with open(file, 'r') as reader:
		plan = []
		reading_plan = False
		reading_build_time = False
		reading_solve_time = False
		while (True):
			line = reader.readline()
			if (not line):
				break

			if line.__contains__("plan"):
				reading_plan = True
				reading_build_time = False
				reading_solve_time = False
				continue
			if line.__contains__("building"):
				reading_plan = False
				reading_build_time = True
				reading_solve_time = False
				continue
			if line.__contains__("solving"):
				reading_plan = False
				reading_build_time = False
				reading_solve_time = True
				continue
			if line.__contains__("vars"):
				words = line.split()
				log.vars = int(words[1])
				continue
			if line.__contains__("clauses"):
				words = line.split()
				log.clauses = int(words[1])
				continue

			if reading_plan:
				timestep = []
				words = line.split()
				for a in range(agents):
					timestep.append((int(words[2*a])-1,int(words[2*a+1])-1))
				plan.append(timestep)
			
			if reading_build_time:
				words = line.split()
				log.clauseBuildTime += int(float(words[2])*1000)
				reading_build_time = False

			if reading_solve_time:
				words = line.split()
				log.solverTime += int(float(words[2])*1000)
				reading_solve_time = False

	return plan

def readClassic(agents: int, file: str, log: Logger) -> list:
	with open(file, 'r') as reader:
		plan = []
		reading_plan = False
		reading_build_time = False
		reading_solve_time = False
		while (True):
			line = reader.readline()
			if (not line):
				break

			if line.__contains__("plan"):
				reading_plan = True
				reading_build_time = False
				reading_solve_time = False
				continue
			if line.__contains__("building"):
				reading_plan = False
				reading_build_time = True
				reading_solve_time = False
				continue
			if line.__contains__("solving"):
				reading_plan = False
				reading_build_time = False
				reading_solve_time = True
				continue
			if line.__contains__("vars"):
				words = line.split()
				log.vars = int(words[1])
				continue
			if line.__contains__("clauses"):
				words = line.split()
				log.clauses = int(words[1])
				continue

			if reading_plan:
				words = line.split()
				plan.append([int(x) - 1 for x in words])
			
			if reading_build_time:
				words = line.split()
				log.clauseBuildTime += int(float(words[2])*1000)
				reading_build_time = False

			if reading_solve_time:
				words = line.split()
				log.solverTime += int(float(words[2])*1000)
				reading_solve_time = False

	return plan