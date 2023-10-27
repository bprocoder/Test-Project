import random
import string
import datetime


def makecouponcode():
    year = datetime.datetime.now().year
    letters = [
        a + b for a in string.ascii_uppercase for b in string.ascii_uppercase]
    digits = [f"{i:02}" for i in range(100)]
    unique_combination = random.choice(
        digits) + random.choice(letters) + str(year)
    print(unique_combination)
    return unique_combination


code = makecouponcode()
print('Code', 'RAHU'+code)
