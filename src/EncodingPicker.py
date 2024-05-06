import subprocess
from multiprocessing import Process, Queue
import time

from .MapLoader import GridMap
from .ScenLoader import Agent
from .TEG import TEGClassic
from .Logger import Logger
from .picat import PicatPrinter
from .picat import PicatReader

def pick(args, agents: list, map: GridMap) -> int:

	# agents to start with
	starting_agents = len(agents)
	if args.agents != -1:
		if args.agents > starting_agents:
			print("Too many agents specified by -a " + str(args.agents) + ". Only " + str(starting_agents) + " agents exist in " + args.scenario)
			return
		starting_agents = args.agents
	
	# increase by number of agents
	increment = 1
	total_agents = starting_agents
	if args.increment !=-1:
		total_agents = len(agents)
		increment = args.increment

	for current_agents in range(starting_agents, total_agents + 1, increment):
		print ("Solving " + str(current_agents) + " agents from " + args.scenario + " using " + args.solver)

		#####################
		## Delivery models ##
		#####################

		if args.solver == "picat-delivery-split":
			teg = TEGClassic(agents, map)
			log = Logger(args.scenario, map.map_file, args.solver, "mks", current_agents, delivery=True, rotation=True)

			process = Process(target=picatDeliverySplit, args=(args, agents, current_agents, map, teg, log))

			process.start()
			process.join(timeout=args.timeout)
			if process.is_alive():
				process.terminate()
				print("Timeout: No solution found in the given time")
				return -1
			continue

		if args.solver == "picat-delivery-classic":
			teg = TEGClassic(agents, map)
			log = Logger(args.scenario, map.map_file, args.solver, "mks", current_agents, delivery=True)

			process = Process(target=picatDeliveryClassic, args=(args, agents, current_agents, map, teg, log))

			process.start()
			process.join(timeout=args.timeout)
			if process.is_alive():
				process.terminate()
				print("Timeout: No solution found in the given time")
				return -1
			continue

		##########################
		## Classic Picat models ##
		##########################

		if args.solver == "picat-mks":
			teg = TEGClassic(agents, map)
			log = Logger(args.scenario, map.map_file, args.solver, "mks", current_agents, delivery=False, rotation=False)

			process = Process(target=picatMks, args=(args, agents, current_agents, map, teg, log))

			process.start()
			process.join(timeout=args.timeout)
			if process.is_alive():
				process.terminate()
				print("Timeout: No solution found in the given time")
				return -1
			continue

		if args.solver == "picat-soc":
			teg = TEGClassic(agents, map)
			log = Logger(args.scenario, map.map_file, args.solver, "soc", current_agents, delivery=False, rotation=False)

			process = Process(target=picatSoc, args=(args, agents, current_agents, map, teg, log))

			process.start()
			process.join(timeout=args.timeout)
			if process.is_alive():
				process.terminate()
				print("Timeout: No solution found in the given time")
				return -1
			continue

		########################
		## Split Picat models ##
		########################
  
		if args.solver == "picat-soc-split":
			teg = TEGClassic(agents, map)
			log = Logger(args.scenario, map.map_file, args.solver, "soc", current_agents, delivery=False, rotation=True)

			process = Process(target=picatSocSplit, args=(args, agents, current_agents, map, teg, log))

			process.start()
			process.join(timeout=args.timeout)
			if process.is_alive():
				process.terminate()
				print("Timeout: No solution found in the given time")
				return -1
			continue


		if args.solver == "picat-soc-split-all":
			teg = TEGClassic(agents, map)
			log = Logger(args.scenario, map.map_file, args.solver, "soc", current_agents, delivery=False, rotation=True)

			process = Process(target=picatSocSplitAll, args=(args, agents, current_agents, map, teg, log))

			process.start()
			process.join(timeout=args.timeout)
			if process.is_alive():
				process.terminate()
				print("Timeout: No solution found in the given time")
				return -1
			continue

		print("Unknown model", args.solver)
		return -2
	return 0

#####################
#####################

def picatDeliverySplit(args, agents: list, current_agents: int, map: GridMap, teg: TEGClassic, log: Logger) -> None:
	instance_file = "picat_files/delivery_input.pi"
	output_file = "run/model_delivery_split.out"
	plan_file = "plans/model_delivery_split.sol"

	timer_start = time.time()
	PicatPrinter.printInstance(args, agents, current_agents, map, instance_file, "delivery", teg, log)
	log.pythonTime += int((time.time() - timer_start)*1000)

	f = open(output_file, "w")
	subprocess.run(["timeout", str(args.timeout + 2), "picat_files/picat", "picat_files/model_delivery_split.pi", instance_file], stdout=f) 
	f.close()

	plan = PicatReader.readSplit(current_agents, output_file, log)
	log.makeOutput(args, agents, map, plan, plan_file)

def picatDeliveryClassic(args, agents: list, current_agents: int, map: GridMap, teg: TEGClassic, log: Logger) -> None:
	instance_file = "picat_files/delivery_input.pi"
	output_file = "run/model_delivery_classic.out"
	plan_file = "plans/model_delivery_classic.sol"

	timer_start = time.time()
	PicatPrinter.printInstance(args, agents, current_agents, map, instance_file, "delivery", teg, log)
	log.pythonTime += int((time.time() - timer_start)*1000)

	f = open(output_file, "w")
	subprocess.run(["timeout", str(args.timeout + 2), "picat_files/picat", "picat_files/model_delivery_classic.pi", instance_file], stdout=f) 
	f.close()

	plan = PicatReader.readClassic(current_agents, output_file, log)
	log.makeOutput(args, agents, map, plan, plan_file)

def picatMks(args, agents: list, current_agents: int, map: GridMap, teg: TEGClassic, log: Logger) -> None:
	instance_file = "picat_files/mks_input.pi"
	output_file = "run/mks.out"
	plan_file = "plans/mks.sol"

	timer_start = time.time()
	PicatPrinter.printInstance(args, agents, current_agents, map, instance_file, "classic", teg, log)
	log.pythonTime += int((time.time() - timer_start)*1000)

	f = open(output_file, "w")
	subprocess.run(["timeout", str(args.timeout + 2), "picat_files/picat", "picat_files/mks.pi", instance_file], stdout=f) 
	f.close()

	plan = PicatReader.readClassic(current_agents, output_file, log)
	log.makeOutput(args, agents, map, plan, plan_file)

def picatSoc(args, agents: list, current_agents: int, map: GridMap, teg: TEGClassic, log: Logger) -> None:
	instance_file = "picat_files/soc_input.pi"
	output_file = "run/soc.out"
	plan_file = "plans/soc.sol"

	timer_start = time.time()
	PicatPrinter.printInstance(args, agents, current_agents, map, instance_file, "classic", teg, log)
	log.pythonTime += int((time.time() - timer_start)*1000)

	f = open(output_file, "w")
	subprocess.run(["timeout", str(args.timeout + 2), "picat_files/picat", "picat_files/soc.pi", instance_file], stdout=f) 
	f.close()

	plan = PicatReader.readClassic(current_agents, output_file, log)
	log.makeOutput(args, agents, map, plan, plan_file)

def picatSocSplit(args, agents: list, current_agents: int, map: GridMap, teg: TEGClassic, log: Logger) -> None:
	instance_file = "picat_files/soc_split_input.pi"
	output_file = "run/soc_split.out"
	plan_file = "plans/soc_split.sol"

	timer_start = time.time()
	PicatPrinter.printInstance(args, agents, current_agents, map, instance_file, "classic", teg, log)
	log.pythonTime += int((time.time() - timer_start)*1000)

	f = open(output_file, "w")
	subprocess.run(["timeout", str(args.timeout + 2), "picat_files/picat", "picat_files/soc_split.pi", instance_file], stdout=f) 
	f.close()

	plan = PicatReader.readSplit(current_agents, output_file, log)
	log.makeOutput(args, agents, map, plan, plan_file)

def picatSocSplitAll(args, agents: list, current_agents: int, map: GridMap, teg: TEGClassic, log: Logger) -> None:
	instance_file = "picat_files/soc_split_input.pi"
	output_file = "run/soc_split_all.out"
	plan_file = "plans/soc_split"

	timer_start = time.time()
	PicatPrinter.printInstance(args, agents, current_agents, map, instance_file, "classic", teg, log)
	log.pythonTime += int((time.time() - timer_start)*1000)

	f = open(output_file, "w")
	subprocess.run(["timeout", str(args.timeout + 2), "picat_files/picat", "picat_files/soc_split_all.pi", instance_file], stdout=f) 
	f.close()

	plans = PicatReader.readSplitMulti(current_agents, output_file, log)

	plan_nr = 0
	for plan in plans:
		log.makeOutput(args, agents, map, plan, plan_file+str(plan_nr)+".sol")
		plan_nr += 1
