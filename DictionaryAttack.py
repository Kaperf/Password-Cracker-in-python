from Baseattack import BaseAttack
from collections.abc import Iterator
class DictionaryAttack(BaseAttack):
	#Constructor BaseAttack but also do user want to applyLeetSpeak. It can be costly both memory and proccesing wise
	def __init__(
	self,
	tester : CandidateTester,
	options : CrackOptions,
	applyLeetSpeak: bool = False
	):
		super().__init__(tester,options)
		self.applyLeetSpeak = applyLeetSpeak 
	#Main function responsible for finding right password if found
	def run(self) -> Crackresult:
		if self.options.wordlist_path is None:
			raise ValueError("Wordlist path is required")
		with open(
		self.options.wordlist_path,
		"r",
		encoding = "utf-8",
		errors = "ignore"
		) as file:
			for word in self.read_words(file):
					for candidate in self.generate_candidates(word):
				#Case where time  has expired or something else has happened
						if self.should_stop():
							return self.build_result(found = False, password = None)
				#The candidate has been found
						if self.tester.test(candidate):
							return self.build_result(found = True, password = candidate)
		#File didnt include password
		return self.build_result(found = False, password = None)
		
			
	#To simplify and minimize ammount of proccesing function generate_candidate will help
	def generate_candidates(self,word : str) -> Iterator[str]:
		yield from self.generate_variants(word)
		if self.applyLeetSpeak:
			yield from self.apply_leetspeak(word)

		# generated = set()
		# for variant in  self.generate_variants(word):
		# 	if variant not in generated:
		# 		generated.add(variant)
		# 		yield variant
		# 	if self.applyLeetSpeak:
		# 		if leet_variant not in generated:
		# 			generated.add(leet_variant)
		# 			yield leet_variant
	def read_words(self, file: file) -> Iterator[str]:
		for line  in file:
			word = self.normalize_words(line)
			if word:
				yield word
		
	@staticmethod
	def normalize_words(word : str) -> str:
		return word.strip()
	#Iterator returning everyvalue that was given by variants
	@staticmethod
	def generate_variants(word : str) -> Iterator[str]:
		forms = {
		word,
		word.capitalize(),
		word.upper()
		}
		#To save resorces ammount of suffixes has been reduced
		#If needed just expand list here
		suffixes = ("","1","_","12","123","__")
		for form in forms:
			for suffix in suffixes:
				yield form+suffix
	@staticmethod
	def apply_leetspeak(word : str) -> Iterator[str]:
		replacements = {
		"a" : "@",
		"A" : "@",
		"e" : "3",
		"E" : "3",
		"i" : "1",
		"I" : "1",
		"o" : "0",
		"O" : "0",
		"s" : "5",
		"S" : "5"
		}
		generated = {word}
		yield word
		#variants with one change
		for original, replacement in replacements.items():
			variant = word.replace(original,replacement)
			if variant not in generated:
				generated.add(variant)
				yield variant
		#Variant will all changes applied
		full_variant = "".join(replacements.get(character, character)
		for character in word
		)
		if full_variant not in generated:
			yield full_variant
