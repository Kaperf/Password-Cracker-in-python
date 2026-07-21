from Baseattack import BaseAttack
from math import pow
from itertools import product
from collections.abc import Iterator

class BruteForce(BaseAttack):
    def __init__(
        self,
        tester : CandidateTester,
        options : CrackOptions
    ):
        super().__init__(tester,options)
    
    def run(self) -> Crackresult:
        for length in range(self.options.min_length, self.options.max_length+1):
            for candidate in self.generate_candidates(length):
                if self.should_stop():
                    return self.build_result(found = False,password = None)
                if self.tester.test(candidate):
                    return self.build_result(found = True, password = candidate)
        return self.build_result(found = False, password = None)


    def generate_candidates(self, length : int) -> Iterator[str]:
        #it is working for only 1 length however in run function it is calculated max_length - min_length
        for characters in product(self.options.charset,repeat=length):
            yield "".join(characters)
        # charset ^ minlength + charset ^minlength+1 +... charset^maxlength
    def calculate_keyspace(self) -> int:
        total = 0
        for length in range(
            self.options.min_length,
            self.options.max_length + 1
        ):
            total += math.pow(len(self.options.charset), length)
        return total
    #For easier backup to index all of those values
    def index_to_password(self, index : int, length: int) -> str:
        charset = self.options.charset
        charset_size = len(charset)
        if index < 0:
            raise ValueError("Value of index cannot be 0")
        maximum_index = charset_size ** length
        if index >= maximum_index:
            raise ValueError(f"Index value is too large for password length: {length}")
        #creating a thing for example length=3 : [""] +[""] +[""] 3 placeholders 
        password = [""] * length
        #it is iterating from right to left to adjust everyvalue
        #meaning if we have abc  it is working with abc->  ab->  a
        #Then combining everyvalue we will receive 123
        for position in range(length-1, -1, -1 ):
            character_index = index % charset_size
            password[position] = charset[character_index]
            index //= charset_size ## Division without rests
        return "".join(password)

    def password_to_index(self, password : str) -> int:
        #Function to write for easier backup if bruteforcing would be unexpectedly stopped
        charset = self.options.charset
        charset_size = len(charset)
        #Creating a table with character and its value
        character_indexes = {
        character : index 
        for index, character in enumerate(charset)
        }
        index = 0
        #Standard procedure to check if the given string is correct
        for character in password:
            if character not in character_indexes:
                raise ValueError(f"Character '{character}' not in charset")
            #Formula for index to password
            index = (index * charset_size + character_indexes[character])
        return index