import argparse

from target import CrackTarget
from Options import Crackoptions


class CLIParser:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            prog="password-cracker",
            description="Password hash cracking tool",
            epilog="Program made by Kaperf"
        )

        self._configure_arguments()

    def _configure_arguments(self) -> None:
        self.parser.add_argument(
            "--hash",
            dest="hash_value",
            required=True,
            help="Target hash value"
        )

        self.parser.add_argument(
            "--algorithm",
            required=True,
            choices=[
                "md5",
                "sha1",
                "sha224",
                "sha256",
                "sha384",
                "sha512",
                "sha3-224",
                "sha3-256",
                "sha3-384",
                "sha3-512"
            ],
            help="Hashing algorithm"
        )
        self.parser.add_argument(
            "--rainbow-table",
            dest="rainbow_table_path",
            default=None,
            help="Path to the rainbow table file"
        )
        self.parser.add_argument(
            "--mode",
            required=True,
            choices=[
                "dictionary",
                "bruteforce",
                "mask",
                "rainbow"
            ],
            help="Attack mode"
        )

        self.parser.add_argument(
            "--min-length",
            type=int,
            default=1,
            help="Minimum password length"
        )

        self.parser.add_argument(
            "--max-length",
            type=int,
            default=8,
            help="Maximum password length"
        )

        self.parser.add_argument(
            "--charset",
            default="abcdefghijklmnopqrstuvwxyz",
            help="Characters used during the attack"
        )

        self.parser.add_argument(
            "--wordlist",
            dest="wordlist_path",
            default=None,
            help="Path to a wordlist file"
        )

        self.parser.add_argument(
            "--mask",
            default=None,
            help="Password mask, for example ?u?l?l?d"
        )

        self.parser.add_argument(
            "--processes",
            dest="threads",
            type=int,
            default=1,
            help="Number of worker processes"
        )

        self.parser.add_argument(
            "--time-limit",
            type=float,
            default=None,
            help="Maximum attack time in seconds"
        )

        self.parser.add_argument(
            "--mutations",
            dest="use_mutations",
            action="store_true",
            help="Enable dictionary mutations"
        )

        self.parser.add_argument(
            "--salt",
            default=None,
            help="Optional salt"
        )

        self.parser.add_argument(
            "--salt-position",
            choices=["before", "after"],
            default="after",
            help="Salt position relative to the password"
        )
        # self.parser.add_argument(
        #     "--chain-length",
        #     type=int,
        #     default=1000
        # )

        # self.parser.add_argument(
        #     "--chain-count",
        #     type=int,
        #     default=5000
        # )

        # self.parser.add_argument(
        #     "--password-length",
        #     type=int,
        #     default=4
        # )

        # self.parser.add_argument(
        #     "--rainbow-output",
        #     default="rainbow_table.json"
        # )

    def parse(self) -> tuple[CrackTarget, Crackoptions, str | None]:
        arguments = self.parser.parse_args()

        target = self.create_target(arguments)
        options = self.create_options(arguments)

        return target, options, arguments.rainbow_table_path

    @staticmethod
    def create_target(arguments: argparse.Namespace) -> CrackTarget:
        return CrackTarget(
            hash_value=arguments.hash_value,
            algorithm=arguments.algorithm,
            salt=arguments.salt,
            salt_position=arguments.salt_position
        )

    @staticmethod
    def create_options(arguments: argparse.Namespace) -> Crackoptions:
        return Crackoptions(
            mode=arguments.mode,
            min_length=arguments.min_length,
            max_length=arguments.max_length,
            charset=arguments.charset,
            wordlist_path=arguments.wordlist_path,
            mask=arguments.mask,
            threads=arguments.threads,
            time_limit=arguments.time_limit,
            use_mutations=arguments.use_mutations
        )