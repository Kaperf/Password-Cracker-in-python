import hashlib
class PasswordHasher:
	ALGORITHMS = {
        "md5": "md5",
        "sha1": "sha1",
        "sha224": "sha224",
        "sha256": "sha256",
        "sha384": "sha384",
        "sha512": "sha512",
        "sha3-224": "sha3_224",
        "sha3-256": "sha3_256",
        "sha3-384": "sha3_384",
        "sha3-512": "sha3_512"
	}
	#Constructor also checking if algorithm is supported
	def __init__(
	self,
	algorithm : str
	): 
		normalized = algorithm.strip().lower()
		normalized = normalized.replace("_", "-")
		if normalized not in self.ALGORITHMS:
			raise ValueError(f"{algorithm} currently not supported")
		self.algorithm = normalized
	#Encoding, choosing an algorithm, hashing password with haslib
	def hash_password(self,
	password: str, 
	salt: str | None = None, 
	salt_position: str = "after") -> str:
		text_to_hash = password
		if salt is not None:
			text_to_hash = self.combine_with_salt(
			password,
			salt,
			salt_position
			)
		passwordBytes =  text_to_hash.encode("utf-8")
		hashlibalgorithm = self.ALGORITHMS[self.algorithm]
		hashedPassword = hashlib.new(hashlibalgorithm, passwordBytes)
		return hashedPassword.hexdigest()
	#Static method to add salt if needed
	@staticmethod
	def combine_with_salt(
	password: str,
	salt: str,
	salt_position: str
	) -> str:
		#normalizing salt position to be either before or after
		normalized = salt_position.strip().lower()
		if normalized == 'after':
			return password + salt
		if normalized == 'before':
			return salt + password
		raise ValueError("Salt position must be either 'before' or 'after'")
	
