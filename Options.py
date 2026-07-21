from pathlib import Path
#Class to recognize what attack will be performed
class Crackoptions:
	supportedMods = {
	"bruteforce",
	"dictionary",
	"mask",
	"rainbow"
	}
	def __init__(self,
		mode: str,
		min_length: int,
		max_length: int,
		charset: str,
		wordlist_path: str | None,
		mask: str | None,
		threads: int,
		time_limit: float | None,
		use_mutations: bool
		):
		self.mode = mode
		self.min_length = min_length
		self.max_length = max_length
		self.charset = charset
		self.wordlist_path = wordlist_path
		self.mask = mask
		self.threads = threads
		self.time_limit = time_limit
		self.use_mutations = use_mutations
	#Checking if all parametrs are being correct toward specific attack
	def validate(self) -> None:
		if self.mode not in self.supportedMods:
			raise ValueError(f"{self.mode} is not supported")
		if self.min_length <= 0:
			raise ValueError("Minimum length cannot be less than 0")
		if self.max_length <= 0:
			raise ValueError("Maximum length cannot be less than 0")
		if self.min_length > self.max_length:
			raise ValueError("Minimum length cannot be bigger than maximum")
		if self.threads <= 0:
			raise ValueError("Threads must be bigger than 0")
		if self.time_limit is not None and self.time_limit <= 0:
			raise ValueError("Time limit has to be positivive integer")
		if self.mode == "bruteforce":
			if not self.charset:
				raise ValueError("Wordlist must be implemented in brute-force mode")
		if self.mode == "dictionary":
			if not self.wordlist_path:
				raise ValueError("There must be a path in dictionary mode")
			wordlist = Path(self.wordlist_path)
			if not wordlist.exists():
				raise ValueError(f"File {wordlist} doesnt exist")
			if not wordlist.is_file():
				raise ValueError(f"Wordlist path is not a file: {self.wordlist_path}")
		if self.mode == "mask":
			if not self.mask:
				raise ValueError("There must be a mask in mask mode")
