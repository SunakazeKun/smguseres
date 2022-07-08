import argparse
from smguseres import UseResourceGenerator

game_path = "D:/Modding/Super Mario Galaxy/SMG2/files"
builders = [
    # Takes three arguments. Game files path, Galaxy name and number of scenarios.
    # Number of scenarios does not include Green Stars and Hidden Stars.
    UseResourceGenerator(game_path, "IslandFleetGalaxy", 3),
    UseResourceGenerator(game_path, "YosshiHomeGalaxy", 3),
    UseResourceGenerator(game_path, "DigMineGalaxy", 3),
    UseResourceGenerator(game_path, "MokumokuValleyGalaxy", 2),
    UseResourceGenerator(game_path, "AbekobeGalaxy", 2),
    UseResourceGenerator(game_path, "RedBlueExGalaxy", 2)
]

def generate(args):
    for builder in builders:
        builder.write_analyzed()

def clear(args):
    for builder in builders:
        builder.write_dummy()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="")
    subs = parser.add_subparsers(dest="command", help="Command")
    subs.required = True

    clear_parser = subs.add_parser("clear", description="Create dummy UseResource archives.")
    clear_parser.set_defaults(func=clear)

    generate_parser = subs.add_parser("generate", description="Generate UseResource archives from logs.")
    generate_parser.set_defaults(func=generate)

    args = parser.parse_args()
    args.func(args)
