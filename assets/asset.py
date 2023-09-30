import random
import string

def string_generator(size=3, string=string.ascii_letters + string.digits):    
    return ''.join(random.choice(string) for _ in range(size))
