class CrackResult:
	def __init__(
	self,
	found: bool,
	attempts: int,
	password: str | None,
	elapsed_time: float,
	attack_mode: str
	):
		self.found = found
		self.attempts = attempts
		self.password = password
		self.elapsed_time = elapsed_time
		self.hash_rate = 0.0
		self.attack_mode = attack_mode
	#Calculating hash rate
	def calculate_hash_rate(self) -> float:
		if self.elapsed_time <= 0:
			self.hash_rate = 0.0
			return self.hash_rate
		self.hash_rate = float(self.attempts) / self.elapsed_time
		return self.hash_rate
	#printing format result
	def format_result(self) -> str:
		self.calculate_hash_rate()
		if self.found:
			result_message = f"Password has been found {self.password}"
		else:
			result_message = "Password has not been found"
		return(
        		f"{result_message}\n"
           		f"Attack mode: {self.attack_mode}\n"
            		f"Attempts: {self.attempts}\n"
            		f"Elapsed time: {self.elapsed_time:.2f} seconds\n"
            		f"Hash rate: {self.hash_rate:.2f} hashes/second"
        	)
