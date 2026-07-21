from Baseattack import BaseAttack
from itertools import product
from collections.abc import Iterator

class MaskAttack(BaseAttack):
    MASK = {
    "?u" : "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
    "?l" : "abcdefghijklmnopqrstuvwxyz",
    "?d" : "0123456789",
    "?s" : "!@#$%^&*()_+-=~`,./?><:;\"'}{[]}\\",
    }    
    #Mask ?a contains all of the chacters
    MASK["?a"] = (
        MASK["?u"] +MASK["?d"] +MASK["?s"] +MASK["?l"]  
    )
    def __init__(
        self,
        tester : CandidateTester,
        options : CrackOptions,
    ):
        super().__init__(tester,options)
    
    def run(self) -> Crackresult:
        candidates = self.generate_candidates()
        for candidate in candidates:
            if self.should_stop():
                return self.build_result(found = False, password = None)
            if self.tester.test(candidate) :
                return self.build_result(found = True, password = candidate)    
        return self.build_result(found = False, password = None)


    @classmethod
    def parse_mask(cls, mask: str) -> Iterator[str]:
        index = 0
        while index < len(mask):
            #Indexing char to first mask
            character = mask[index]
            #We are checking only for ?x where x is u, l, d, s for example Admin?u we will only check for ?u
            if character == "?":
                #Checking if the last char is not ""
                if index + 1 > len(mask):
                    raise ValueError("Mask cannot end with ?")
            #+2 because otherwise it would have contained ?
                token = mask[index : index + 2]
                if token not in cls.MASK: # cls is same as self but used in classmethods
                    raise ValueError(f"Mask token {token} not supported")
                yield cls.MASK[token]
                index +=2
            #As in above example: Admin -> A -> D etc till we find ?x
            else:
                yield character
                index +=1

    def generate_candidates(self) -> Iterator[str]:
        ChangedToMask = self.parse_mask(self.options.mask)
        #Cartesian product meaning If we have Admin?d -> Admin0, Admin1, ..., Admin9
        for character in product(*ChangedToMask):
            yield "".join(character)
    def calculate_keyspace(self) -> int:
        char_changed_to_mask = self.parse_mask(self.options.mask)
        sum = 1
        for charset in char_changed_to_mask:
            sum *= len(charset)
        return sum