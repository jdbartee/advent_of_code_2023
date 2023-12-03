from src.day_one import DayOne
from src.day_two import DayTwo
from src.day_three import DayThree

from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title='title', required=True, help='help')
    for day in [DayOne, DayTwo, DayThree]:
        subparser = subparsers.add_parser(day.command_name)
        day.setup_parser(subparser)
        subparser.set_defaults(run=day.run)
    args = parser.parse_args()
    args.run(args)
        
    
