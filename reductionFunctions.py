class ReductionFunction:
    def __init__(
        self,
        charset: str,
        password_length: int
    ):
    #Validating data
        if not charset:
            raise ValueError("Charset cannot be empty.")

        if password_length <= 0:
            raise ValueError("Password length must be greater than 0.")

        self.charset = charset
        self.password_length = password_length

    def reduce(self, hash_value: str, step: int) -> str:
        #Taking first and last 6 chars from hash
        beginning_of_hash = hash_value[:6]
        end_of_hash = hash_value[-6:]

        beginning_value = int(beginning_of_hash, 16)
        end_value = int(end_of_hash, 16)
        #Custom unique value
        mixed_value = beginning_value ^ end_value
        mixed_value += step
        #Reducing this value by ammount of keyspace
        keyspace = len(self.charset) ** self.password_length
        index = mixed_value % keyspace
        #Reserving space for password
        password = [""] * self.password_length
        #Same algorithm as in brufeforce
        #Working from right to left meaning abc -> ab -> a
        for position in range(self.password_length - 1, -1, -1):
            character_index = index % len(self.charset)
            password[position] = self.charset[character_index]
            index //= len(self.charset)

        return "".join(password)