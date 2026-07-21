from RainbowTableGenerators import RainbowTableGenerator
from Baseattack import BaseAttack
class RainbowTableAttack(BaseAttack):
    def __init__(self,
    table: RainbowTable,
    reduction : ReductionFunction,
    tester: CandidateTester,
	options: Crackoptions
    ):
        super().__init__(tester = tester, options = options) # Czy tutaj tester jest potrzebny?
        self.table = table
        self.reduction = reduction
    #Main class managing whole operation
    # endpoint -> reconstructin -> if password exists returning
    def run(self) -> CrackResult:
        target_hash = self.tester.target.hash_value
        if self.table.algorithm.lower() != self.tester.target.algorithm.lower():
            raise ValueError("Algorithms doesn't match")
        if self.table.charset != self.options.charset:
            raise ValueError("Charsets doesn't match")
        if self.table.password_length != self.reduction.password_length:
            raise ValueError("Passwords length's  doesn't match")

        for start_step in range(self.table.chain_length -1, -1, -1):
            if self.should_stop():
                return self.build_result(found = False, password = None)
            endpoint = self.calculate_possible_endpoint(target_hash= target_hash, start_step = start_step)
            start_password = self.search_endpoint(endpoint)
            if start_password is None:
                continue
            password = self.reconstruct_and_veryfify(start_password= start_password, target_hash = target_hash)
            if password is not None:
                    return self.build_result(found = True, password = password)
        return self.build_result(found = False, password = None)

    #Method for checking if possible hash is on the first position of chain
    def calculate_possible_endpoint(self, target_hash : str, start_step : int) -> str | None:
        if not 0 <= start_step < self.table.chain_length:
            raise ValueError("Invalid starting step")
        
        current_hash = target_hash
        current_password = ""

        for step in range(start_step,self.table.chain_length):
            current_password = self.reduction.reduce(hash_value= current_hash, step = step)
            #After last reduction we have the endpoint
            if step < self.table.chain_length -1:
                current_hash = self.tester.hasher.hash_password(current_password)
                self.tester.stats.increment()
        return current_password
            
    #Just searching up endpoint
    def search_endpoint(self, endpoint : str) -> str | None:
        return self.table.find_chain_start(endpoint)

    #Receiving starting chain
    #Next reconstructing password->hash->comparision->reduction
    #If hash = target_hash -> return password
    def reconstruct_and_veryfify(self, start_password : str, target_hash : str)-> str | None:
        current_password = start_password
        normalized_target = target_hash.strip().lower()
        for step in range(self.table.chain_length):
            self.tester.stats.current_candidate = current_password
            current_hash = self.tester.hasher.hash_password(current_password)
            self.tester.stats.increment()
            if current_hash.strip().lower() == normalized_target:
                return current_password
            current_password = self.reduction.reduce(hash_value = current_hash, step = step)
        

        chain = RainbowChain(start_password = start_password, chain_length = self.options.chain_length)
        tableToVerify = chain.reconstruct(reduction = self.reduction, hasher = self.tester.hasher)
        if self.table.chain == tableToVerify:
            return start_password
        else:
            return False