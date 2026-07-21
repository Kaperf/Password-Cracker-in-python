from DictionaryAttack import DictionaryAttack
from BruteForce import BruteForce
from MaskAttack import MaskAttack
from RainbowTableattack import RainbowTableAttack
from passwordHasher import PasswordHasher
from ProgressStats import ProgressStats
from CandidateTester import CandidateTester
class PasswordCracker:
    def __init__(
        self,
        target : CrackTarget,
        options : Crackoptions,
        table : RainbowTable | None = None,
        reduction : ReductionFunction | None = None
    ):
        self.target = target
        self.options = options
        
        self.hasher : PasswordHasher | None = None
        self.tester : CandidateTester | None = None
        self.attack : BaseAttack | None = None

        #Only needed for rainbow tables
        self.table = table
        self.reduction = reduction
    def prepare(self) -> None:
        self.target.validate()
        self.options.validate()

        self.hasher = PasswordHasher(algorithm = self.target.algorithm)
        stats = ProgressStats()
        self.tester = CandidateTester(target  = self.target, hasher = self.hasher, stats = stats)
        self.attack = self.create_attack()

    def create_attack(self) -> BaseAttack:
        if self.tester is None:
            raise RuntimeError(
                "CandidateTester has not been created. Call prepare() first."
            )

        mode = self.options.mode.strip().lower()

        if mode == "dictionary":
            return DictionaryAttack(
                tester=self.tester,
                options=self.options,
                applyLeetSpeak=self.options.use_mutations
            )

        if mode in {"bruteforce", "brute_force"}:
            return BruteForce(
                tester=self.tester,
                options=self.options
            )

        if mode == "mask":
            return MaskAttack(
                tester=self.tester,
                options=self.options
            )

        if mode == "rainbow":
            if self.table is None:
                raise ValueError(
                    "Rainbow table is required for rainbow attack."
                )

            if self.reduction is None:
                raise ValueError(
                    "Reduction function is required for rainbow attack."
                )

            return RainbowTableAttack(
                table=self.table,
                reduction=self.reduction,
                tester=self.tester,
                options=self.options
            )

        raise ValueError(
            f"Unsupported attack mode: {self.options.mode}"
        )
    def run(self) -> CrackResult:
        if self.attack is None:
            self.prepare()
        if self.attack is None:
            raise RuntimeError("Attack could not be prepared.")
        return self.attack.run()
    def stop(self) -> None:
        if self.attack is not None:
            self.attack.stop()