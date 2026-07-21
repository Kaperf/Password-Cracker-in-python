import string
#List of currently managable algorithms
#Main Class to determine  hash, what hash algorithm, was salt included and if where 
class CrackTarget:
	supportedAlgorithms = {"MD5" : 32, 
	"SHA1": 40,
	 "SHA224": 56,
        "SHA256": 64,
        "SHA384": 96,
        "SHA512": 128,
        "SHA3-224": 56,
        "SHA3-256": 64,
        "SHA3-384": 96,
        "SHA3-512": 128
	}
	def __init__(self,
		hash_value: str, #Hash value of our target meaning that has to be cracked
		algorithm: str,
		salt: str | None = None,
		salt_position: str | None = None
	):
		self.hash_value = hash_value.strip().lower()
		self.algorithm = algorithm.strip().upper()
		self.salt = salt
		self.salt_position = salt_position
	def validate(self) -> None:
		#Checking if hash_value is not empty
		if not self.hash_value:
			raise ValueError("Hash value cannot be empty")
		#Checking if algorithms is listed
		if self.algorithm not in self.supportedAlgorithms:
			raise ValueError(f"Currently not supported {self.algorithm}")
		#Checking if it is really hash_Value
		if  any(character not in string.hexdigits for character in self.hash_value):
			raise ValueError("Hash values can only contain a-f 0-9")
		expected_length = self.supportedAlgorithms[self.algorithm]
		if len(self.hash_value) != expected_length:
			raise ValueError(f"Invalid Hash length. Expected: {expected_length}. Got: {len(self.hash_value)}")
		if self.salt is not None:
			if self.salt_position.lower() not in {"before","after"}:
				raise ValueError("Salt position must be 'before' or 'after'")
			elif self.salt_position is not None:
				raise ValueError("Salt position was provided but salt is missing")
	def normalize_hash(self) -> str:
		return self.hash_value.lower()


#	def gatheringData():
#		hash_value  = string(input("Enter hash to crack"))
#		algorithm = string(input("What algorithm was used"))
#		has_salt = string(input("Was salt added?"))
#		if has_salt.upper == "YES":
#			salt_value = string(input
#			salt_position = string(input("Where was salt added?"))
#		if algorithm.upper =="SHA-2":
#			algorithm == "SHA2"
#		if algorithm.upper == "SHA3" or algorithm.upper == "SHA-3":
#			algorithm == "KECCAK"
