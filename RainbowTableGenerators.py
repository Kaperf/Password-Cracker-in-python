from RainbowTables import RainbowTable
from passwordHasher import PasswordHasher
import secrets
class RainbowTableGenerator:
    def __init__(
        self,
        hasher : PasswordHasher,
        reduction : ReductionFunction,
        chain_length: int ,
        chain_count : int 
        ):
        if chain_length <= 0:
            raise ValueError("Chain length must be greater than 0")
        if chain_count <= 0:
            raise ValueError("Chain count must be greater than 0")
        self.hasher = hasher
        self.reduction = reduction
        self.chain_length = chain_length
        self.chain_count = chain_count
    #Generating said ammount of chains
    def generate(self) -> RainbowTable:
        table = RainbowTable(algorithm = self.hasher.algorithm,password_length= self.reduction.password_length, charset= self.reduction.charset,chain_length= self.chain_length)
        for _ in range(self.chain_count):
            #Taking random number from charset and then generating password
            startingPassword = self.generate_start_password() 
            chain = self.generate_chain(startingPassword)
            table.add_chain(chain)
        remove_duplicates(table)
        return table
    
    #Generating random or defined password
    def generate_start_password(self) -> str:
        #Selecting random choice from charset and also multiplying it for ammount of key_length
        return "".join(secrets.choice(self.reduction.charset) for _ in range(self.reduction.password_length))
    #Creating one chain
    def generate_chain(self, password : str) -> RainbowChain:
        chain = RainbowChain(password,chain_length = self.chain_length)
        chain.generate(hasher = self.hasher, reduction = self.reduction)
        return chain