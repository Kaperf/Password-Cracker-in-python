import target
import passwordHasher
import ProgressStats
#Common class for all attacks and  checking the balance
class CandidateTester:
	def __init__(self,
	target: CrackTarget,
	hasher: PasswordHasher,
	stats: ProgressStats
	):
		self.target = target
		self.hasher = hasher
		self.stats = stats
		#checking if algorithms are the same
		if self.target.algorithm.lower() != self.hasher.algorithm.lower():
			raise ValueError("Target and Passwordhasher uses different algorithms")
	
	# Addresing candidate, hashing current candidate, incrementing number of attemps
	def test(self, candidate: str) -> bool:
		self.stats.current_candidate = candidate #addresing
		candidate_hash = self.hasher.hash_password(
		password = candidate, 
		salt = self.target.salt,
		salt_position = self.target.salt_position
		) # adding salt if needed and hashing current candidate
		self.stats.increment() #incrementing
		return self.compare(candidate_hash) #returning result
	
	#Comparing current candidate with hashvalue from target
	def compare(self, candidate_hash: str) -> bool:
		normalized_candidate_hash = candidate_hash.strip().lower()
		normalized_target_hash = self.target.hash_value.strip().lower()
		return normalized_target_hash == normalized_candidate_hash
	
