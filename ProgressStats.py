import time
class ProgressStats:
	def __init__(
	self,
	attemps: int = 0,
	start_time: float | None = None,
	total_candidates: int | None = None,
	current_candidate: str | None = None
	):
		self.attemps = attemps
		if start_time is None:
			self.start_time = time.time()
		else:
			self.start_time = start_time
		self.total_candidates = total_candidates
		self.current_candidate = current_candidate
	#Incrementing everytime attack didnt workout
	def increment(self) -> None:
		self.attemps += 1
	#Just time that has already elapsed
	def elapsed_time(self) -> float:
		return time.time() - self.start_time
	#Speed of Hashing
	def hash_rate(self) -> float:
		time = self.elapsed_time()
		if time <= 0: 
			return 0.0
		return self.attemps / time
	#Progress that has been already done
	def progress_percentage(self) -> float | None:
		if self.total_candidates is None:
			return None
		if self.total_candidates <= 0:
			return 0.0
		progress = float(self.attemps) / float(self.total_candidates)
		return progress
	#Remaining time of attack
	def  estimated_remaining_time(self) -> float | None:
		if self.total_candidates is None:
			return None
		if self.attemps <= 0:
			return None
		rate = self.hash_rate()
		if rate <= 0:
			return None
		remaining_candidates = self.total_candidates - self.attemps
		if remaining_candidates <= 0:
			return 0.0
		return remaining_candidates / rate
