"""
How much money will someone make on average if they get the amount of money
shown on the face of the die (ie roll a 5 get $5). They can roll 2x, but if
they roll the second time, they get the amount shown on the second roll
"""

from random import randint

def start(roll_again_value = 4, num_iter = 1000):
    
    i=0
    all_rolls = []
    while i <= num_iter:
        roll = randint(1,6)
        if roll < roll_again_value:
            roll = randint(1,6)

        all_rolls.append(roll)
        i += 1


    return float(sum(all_rolls))/float(len(all_rolls))       
            

