from CLIParser import CLIParser
from PasswordCracker import PasswordCracker
from RainbowTables import RainbowTable
from reductionFunctions import ReductionFunction


def main() -> None:
    parser = CLIParser()

    target, options,table_path = parser.parse()
    table = None
    reduction = None

    if options.mode == "rainbow":
        if table_path is None:
            raise ValueError(
                "--rainbow-table is required in rainbow mode."
            )
        table = RainbowTable(
            algorithm=target.algorithm,
            password_length=1,
            charset="a",
            chain_length=1
        )
        table.load(table_path)

        reduction = ReductionFunction(
            charset=table.charset,
            password_length=table.password_length
        )

    cracker = PasswordCracker(
        target=target,
        options=options,
        table = table,
        reduction= reduction
    )

    result = cracker.run()

    print(result.format_result())


if __name__ == "__main__":
    main()
