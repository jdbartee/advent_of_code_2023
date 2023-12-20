from src.day_one import DayOne
from src.day_two import DayTwo
from src.day_three import DayThree
from src.day_four import DayFour
from src.day_five import DayFive
from src.day_six import DaySix
from src.day_seven import DaySeven
from src.day_eight import DayEight
from src.day_nine import DayNine
from src.day_ten import DayTen
from src.day_eleven import DayEleven
from src.day_twelve import DayTwelve
from src.day_thirteen import DayThirteen
from src.day_fourteen import DayFourteen
from src.day_fifteen import DayFifteen
from src.day_sixteen import DaySixteen
from src.day_seventeen import DaySeventeen
from src.day_eighteen import DayEighteen
from src.day_nineteen import DayNineteen

from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(title='title', required=True, help='help')
    for day in [DayOne, DayTwo, DayThree, DayFour, DayFive, DaySix, DaySeven, DayEight,
                DayNine, DayTen, DayEleven, DayTwelve, DayThirteen, DayFourteen, DayFifteen,
                DaySixteen,DaySeventeen,DayEighteen, DayNineteen]:
        subparser = subparsers.add_parser(day.command_name)
        day.setup_parser(subparser)
        subparser.set_defaults(run=day.run)
    args = parser.parse_args()
    args.run(args)
        
    
