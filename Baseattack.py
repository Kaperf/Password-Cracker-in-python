from CandidateTester import CandidateTester
from Options import Crackoptions
from Results import CrackResult
from abc import ABC, abstractmethod
#Abstract class for every type of attack
#class (ABC) python interprets it as a abstract class
class BaseAttack(ABC):
	def __init__(self,
	tester: CandidateTester,
	options: Crackoptions,
	stop_requested: bool | None = None
	):
		self.tester = tester
		self.options = options
		self.stop_requested = False
		self.password_found = False
	#Every class that will inherit this have to implement this by its own rules
	@abstractmethod
	def run(self) -> CrackResult:  
		pass
	#Setting flag for stop
	def stop(self) -> None:
		self.stop_requested = True
	#After finding time expiring/found password its should stop
	def should_stop(self) -> bool:
		#If stop was requested
		if self.stop_requested == True:
			return True
		#If password was found
		if self.password_found == True:
			return True
		#If timelimit has been crossed
		if  self.options.time_limit is not None:
			elapsed = self.tester.stats.elapsed_time()
			if elapsed >= self.options.time_limit:
				self.stop_requested = True
				return True
		return False
	
	#Building results
	def build_result(self,
	found: bool,
	password : str | None
	) -> CrackResult:
		return CrackResult(
		found = found,
		attempts = self.tester.stats.attemps,
		password = password,
		elapsed_time = self.tester.stats.elapsed_time(),
		attack_mode = self.options.mode)
