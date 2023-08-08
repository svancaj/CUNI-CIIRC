from argparse import ArgumentParser

from src import MapLoader
from src import ScenLoader
from src import EncodingPicker

def get_parser() -> ArgumentParser:
	parser = ArgumentParser()

	parser.add_argument(
		"solver",
		default=None,
		type=str,
		help=(
			"The solving method to be used."
		),
	)
	parser.add_argument(
		"-s",
		"--scenario",
		default=None,
		type=str,
		help=(
			"Path to a scenario file."
		),
	)
	parser.add_argument(
		"-m",
		"--map",
		default=None,
		type=str,
		help=(
			"Path to a map file."
		),
	)
	parser.add_argument(
		"-a",
		"--agents",
		default=-1,
		type=int,
		help=(
			"Number of agents to solve. If not specified, all agents in the scenario file are used."
		),
	)
	parser.add_argument(
		"-i",
		"--increment",
		default=-1,
		type=int,
		help=(
			"After a successful call, increase the number of agents by the specified increment. If not specified, do not perform subsequent calls."
		),
	)
	parser.add_argument(
		"-t",
		"--timeout",
		default=60,
		type=int,
		help=(
			"Timeout for the solver."
		),
	)
	parser.add_argument(
		"-p",
		"--print",
		action='store_true',
		help=(
			"Print the found plan."
		),
	)

	return parser

def main(args_list: list = []) -> None:
	
	# parse arguments
	parser = get_parser()
	args = parser.parse_args()

	# get instance
	map_file, agents = ScenLoader.getAgents(args.scenario)
	map = MapLoader.getMap(args.map, map_file)

	# print and solve the desired format
	EncodingPicker.pick(args, agents, map)


if __name__ == "__main__":
	main()