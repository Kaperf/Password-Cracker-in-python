from passwordHasher import PasswordHasher
from reductionFunctions import ReductionFunction
from rainbowChain import RainbowChain
from RainbowTables import RainbowTable


def main() -> None:
    hasher = PasswordHasher(
        algorithm="sha256"
    )

    reduction = ReductionFunction(
        charset="abc",
        password_length=3
    )

    chain = RainbowChain(
        start_password="aaa",
        end_password="",
        chain_length=10
    )

    chain.generate(
        hasher=hasher,
        reduction=reduction
    )

    table = RainbowTable(
        algorithm="sha256",
        charset="abc",
        password_length=3,
        chain_length=10
    )

    table.add_chain(chain)
    table.save("test_rainbow_table.json")

    #Recovering chain to chose hash that we will surealy not find
    reconstructed = list(
        chain.reconstruct(
            hasher=hasher,
            reduction=reduction
        )
    )

    test_password, test_hash = reconstructed[3]

    print("Table saved: test_rainbow_table.json")
    print(f"Test password: {test_password}")
    print(f"Test hash: {test_hash}")
    print(f"Chain start: {chain.start_password}")
    print(f"Chain end: {chain.end_password}")


if __name__ == "__main__":
    main()
