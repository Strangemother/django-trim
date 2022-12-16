import string
import random

def rand_str(length=6):
    choices = random.choices(string.ascii_uppercase + string.digits, k=length)
    return ''.join(choices)
