from ..MapLoader import GridMap
from ..ScenLoader import Agent
from ..TEG import TEGClassic
from ..Logger import Logger

def printInstance(args, agents: list, agents_to_print: int, map: GridMap, file: str, type: str, teg: TEGClassic, log: Logger) -> None:
	# print instance
	input = open(file, "w")

	# header
	input.write("getProblemInstance() = PI =>\n")
	input.write("	PI = $problem(\n	[")

	# agents
	for a in range(agents_to_print):
		last = ""
		if a + 1 == agents_to_print:
			last = "]"
		start = map.map[agents[a].y_start][agents[a].x_start] + 1
		goal = map.map[agents[a].y_goal][agents[a].x_goal] + 1

		if type == "delivery":
			input.write("$agent(" + str(a + 1) + "," + str(start) + "," + str(goal) + "," + str(start) + ")" + last + ",")
		if type == "classic":
			input.write("$agent(" + str(a + 1) + "," + str(start) + ",0," + str(goal) + ")" + last + ",")

	# grid map
	input.write("\n	[")
	for v in range(map.numVertices):
		last = ","
		if v + 1 == map.numVertices:
			last = "],"
		input.write("$vertex(" + str(v + 1) +",[")

		neib = map.getNeighboursIDs(v)
		for nV in range(len(neib)):
			comma = ","
			if nV + 1 == len(neib):
				comma = ""
			input.write(str(neib[nV] + 1) + comma)
		input.write("])" + last)
	
	#TEG
	input.write("\n	[")
	for a in range(agents_to_print):
		last = ","
		if a + 1 == agents_to_print:
			last = "]"
		input.write("$distance(" + str(a + 1) +",[")

		from_start = teg.getDistancesFromStart(a)
		for v in range(len(from_start)):
			comma = ","
			if v + 1 == len(from_start):
				comma = ""
			input.write(str(from_start[v]) + comma)
		input.write("],[")

		from_goal = teg.getDistancesFromGoal(a)
		for v in range(len(from_goal)):
			comma = ","
			if v + 1 == len(from_goal):
				comma = ""
			input.write(str(from_goal[v]) + comma)
		input.write("])" + last)

	# LBs
	classic_mks_LB = teg.getMksLb(agents_to_print)
	classic_soc_LB = teg.getSoCLb(agents_to_print)
	delivery_mks_LB = 2 * classic_mks_LB - 1
	delivery_soc_LB = 2 * classic_soc_LB - agents_to_print

	if type == "delivery":
		input.write(",\n	" + str(delivery_mks_LB) + ",\n")
		input.write("	" + str(delivery_soc_LB) + ").")

		log.mksLB = delivery_mks_LB
		log.socLB = delivery_soc_LB
	if type == "classic":
		input.write(",\n	" + str(classic_mks_LB) + ",\n")
		input.write("	" + str(classic_soc_LB) + ").")

		log.mksLB = classic_mks_LB
		log.socLB = classic_soc_LB

	input.close()