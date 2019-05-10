import random
import math

def random_choice(choices, random_sim=True):
    """
        Input: 
            choices: a range 
        Ouput:
            randomly chosen number from choices
    """
    mychoice = 0

    if random_sim:
        mychoice = random.choice(choices)
    else:
        mychoice = list(choices)[-1]
    
    # random selection
    return mychoice

# distribute plants in the four evenly distributed quandrants
def get_fixed_positions(height, width, nb_samples):
    quadrants = (((0, height//2 - 1), (0, width//2 - 1)),
                ((0, height//2 - 1), (width//2, width-1)),
                ((height//2, height-1), (0, width//2 - 1)),
                ((height//2, height-1), (width//2, width-1)))
    
    max_per_quadrant = max(1, nb_samples//4)
    
    positions = []
    
    for bound in quadrants:
        mycount = 0 
        for y in range(bound[0][0], bound[0][1]):
            mycount2=0
            for x in range(bound[1][0], bound[1][1]):
                positions.append((min(y+3,height-1), min(x+3,width-1)))
                mycount2 += 1
                mycount += 1
                if mycount2 >= max(1,max_per_quadrant//7) or mycount == max_per_quadrant:
                    break
            if mycount == max_per_quadrant:
                break
    return positions


def euclidean_distance(position1, position2):
    return math.sqrt((position1.x - position2.x)**2 + (position1.y - position2.y)**2)

