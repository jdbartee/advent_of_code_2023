from pathlib import Path
from argparse import ArgumentParser, Namespace

class Solution:
    command_name = '0'

    def __init__(self) -> None:
        self.input_data = ""

    def set_data(self, data_path: Path):
        with data_path.open() as fh:
            self.input_data = fh.read()

    def part_one(self):
        return ""
    
    def part_two(self):
        return ""
    
    @classmethod
    def setup_parser(cls, parser: ArgumentParser):
        parser.add_argument("data_file", type=Path)
        return parser
    
    @classmethod
    def run(cls, args: Namespace):
        this = cls()
        this.set_data(args.data_file)
        print("Part 1:")
        print(this.part_one())
        print("Part 2")
        print(this.part_two())