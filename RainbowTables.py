from rainbowChain import RainbowChain
import json
from pathlib import Path

class RainbowTable:
    def __init__(self,
    algorithm : str,
    password_length : int,
    charset : str,
    chain_length : int,
    chains : dict[str,str] | None = None
    ):
        if not algorithm:
            raise ValueError("Algorithm cannot be empty")
        if not charset:
            raise ValueError("Ch arset cannot be empty")
        if  password_length <= 0:
            raise ValueError("Password length must be greater than 0")
        if chain_length <= 0:
            raise ValueError("Chain length mu be grater than 0")

        self.algorithm = algorithm.strip().lower()
        self.password_length = password_length
        self.charset = charset
        self.chain_length = chain_length
        if chains is None:
            self.chains = {}
        else: 
            self.chains = chains
    #Adding chain to existing list
    def add_chain(self,chain : RainbowChain) -> None:
        if not chain.end_password:
            raise ValueError("Chain's end password cannot be empty")
        if not chain.start_password:
            raise ValueError("Chain's start password cannot be empty")
        if chain.chain_length != self.chain_length:
            raise ValueError("Chain's lengths doens't match")
        # start_password : end_password mapping one to another
        self.chains[chain.end_password] = chain.start_password
        
    def find_chain_start(self, end_password : str) ->  str | None:
        if not end_password:
            raise ValueError("end_password is empty")
        #Using method to get O(1) time complexity
        return self.chains.get(end_password)

    #Saving all of progres to file for future backup
    def save(self, path : str) -> None:
        if not path:
            raise ValueError("Path doesnt exist")
        file_path = Path(path)
        #Creating custom metadata for easeir saving
        data = {
            "metadata" : {
                "algorithm": self.algorithm,
                "charset" : self.charset,
                "password_length" : self.password_length,
                "chain_length" : self.chain_length
            },
            "chains" : self.chains
        }
        #Opening a file
        with file_path.open(
            "w",
            encoding = "utf-8"
        ) as file:
            json.dump(data, file, indent = 4, ensure_ascii = False)

    def load(self, path : str) -> None:
        #Checking for path and its existences
        if not path:
            raise ValueError("Path doesnt exist")
        file_path = Path(path)
        if not file_path.exists():
            raise ValueError(f"Rainbow table file doesnt exist {path}")
        if not file_path.is_file():
            raise ValueError(f"Path is not a file: {path}")
        #Opening and loading
        with file_path.open("r",encoding="utf-8") as file:
            data = json.load(file)
        if "metadata" not in data:
            raise ValueError("File does not contain table metadata")
        if "chains" not in data:
            raise ValueError("File does not contain table chains")

        metadata = data["metadata"]

        required_metadata = {
            "algorithm",
            "charset",
            "password_length",
            "chain_length"
        }

        if not required_metadata.issubset(metadata):
            raise ValueError(
                "Rainbow table metadata is incomplete."
            )

        if not isinstance(data["chains"], dict):
            raise ValueError(
                "Chains must be stored as a dictionary."
            )

        self.algorithm = metadata["algorithm"]
        self.charset = metadata["charset"]
        self.password_length = metadata["password_length"]
        self.chain_length = metadata["chain_length"]
        self.chains = data["chains"]


            
    def validate_metadata(self,algorithm : str, charset : str, password_length : int) -> bool:
        return (
            self.algorithm.lower() == algorithm.strip().lower()
            and self.charset == charset
            and self.password_length == password_length
        )