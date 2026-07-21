from passwordHasher import PasswordHasher
from reductionFunctions import ReductionFunction

class RainbowChain():
    def __init__(self,
        start_password : str,
        end_password : str | None,
        chain_length : int | None,
    ):
        self.start_password = start_password
        self.end_password = end_password
        self.chain_length = chain_length
    #Generating every possible key then only memorizing the first and last one for easier backup 
    #If in later function he would have found anything
    #step 0: password -> hash -> reduction -> step 1: ...
    def generate(self,hasher : PasswordHasher, reduction : ReductionFunction) -> None:
        current_password = self.start_password
        for step in range(self.chain_length):
            current_hash = hasher.hash_password(current_password)
            current_password = reduction.reduce(
                hash_value = current_hash,
                step = step
            )
        self.end_password = current_password
    #Reconstructing whole chain. 
    #Mostly same method just but yielding whole thing in the end
    def reconstruct(self,hasher : PasswordHasher, reduction : ReductionFunction) -> Iterator[tuple[str,str]]:
        current_password = self.start_password
        for step in range(self.chain_length):
            current_hash = hasher.hash_password(current_password)
            yield current_password, current_hash
            current_password = reduction.reduce(hash_value = current_hash, step = step)

        