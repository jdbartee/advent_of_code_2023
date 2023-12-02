from src.day_one import DayOne
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title='title', required=True, help='help')
    for day in [DayOne]:
        subparser = subparsers.add_parser(day.command_name)
        day.setup_parser(subparser)
        subparser.set_defaults(run=day.run)
    args = parser.parse_args()
    args.run(args)
        
    
