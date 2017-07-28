from robot.api.deco import keyword
import pasgens


class PasswordGenerationLibrary(object):
    def __init__(self):
        self._password_cache = []

    def generated_passwords(self):
        return self._password_cache

    @keyword('Generate Password ${length:\d+} Characters Long')
    def generate_password(self, length):
        length = int(length)
        self._password_cache.append(pasgens.generate_password(length))

    @keyword('Generate Password ${length:\d+} Characters Long With Seed ${seed:\d+}')
    def generate_password(self, length, seed):
        length = int(length)
        seed = int(seed)
        self._password_cache.append(pasgens.generate_password(length, seed))

    @keyword('Generate ${count:\d+} Passwords Each ${length:\d+} Characters Long')
    def generate_passwords(self, count, length):
        count = int(count)
        length = int(length)
        for i in range(count):
            self._password_cache.append(pasgens.generate_password(length, i))
