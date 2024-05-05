import random
import time
import datetime
import re
import math


# def generate_random_number(minimal, maximal):
#     return random.randint(minimal, maximal)


p= 12345
d = int(re.sub(r'\D', '', str(datetime.datetime.now())))


def generate_random_number(start, end):
    global p
    global d
    
    t = int(time.time() * 1000) 
    t = (t * d + p) & 0x7FFFFFFF
    p = t
    return start + (t % (end - start + 1))