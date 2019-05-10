import re
from util import random_choice
from util import euclidean_distance
from Position import Position

class Animal:
    def __init__(self, terrain, id, position=()):
        self.id = id # animal identifier
        self.age = 0 # animal age
        self.age_max = 10 # animal max age
        self.age_spawn_min = 3 # min age animal can spawn offspring
        self.age_spawn_max = self.age_max # max age animal can spawn
        self.spawn_waiting = 0 # countdown time animal can re-spawn
        self.spawn_waiting_time = 3 # total recovery time for re-spawning
        self.hunger = 0 # hunger level (0 means not hungry)
        self.hunger_max = 3 # max hunger level
        self.visual_range=2 # how far the animal can see
        
        # location of animal in a xy-coordinate system
        if len(position) == 0: # random genereate location
            self.position = Position(0, terrain.width-1, 0, terrain.height-1)
        else: # set location to the provided position value (tuple (x,y))
            self.position = Position(0, terrain.width-1, 0, terrain.height-1, 
                position[0], position[1], random_init=terrain.random_sim)  

    
    def starve(self): 
        """
        Args:
            self: the animal object
        Returns:
            Nothing
        Behavior:
            Increment hunger level by one if hunger level is not at max
        """
        
        if self.hunger< self.hunger_max:
            self.hunger+=1           
        

    def eat(self): 
        """
        Args:
            self: the animal object
        Returns:
            Nothing
        Behavior:
            Decrease hunger level by one if hunger level is not 0
        """

        if self.hunger > 0:
            self.hunger = 0             
         
    
    def grow(self): 
        """
        Args:
            self: the animal object
        Returns:
            Nothing
        Behavior:
            Increase age by one if age is not at max
        """

        if self.age < self.age_max:
            self.age += 1 
         
    def die(self): 
        """
        Args:
            self: the animal object
        Returns:
            True if animal dies of age or hunger; otherwise False
        """

        return (self.hunger == self.hunger_max or self.age == self.age_max)
        

    def get_neighbor_positions(self, terrain): 
        """
        Args:
            self: the animal object
            terrain: the object containing all information about the simulation
        Returns:
            A list of available adjacent positions as Position objects
            Suppose the animal's current position is (x,y)
            The adjacent position is (x+i,y+j), where i is in [-1,0,1] and j in [-1,0,1]
            The neighbor positions *exclude* animal's own position (x,y) (i.e., i!=0 or j!=0)
            An available position is defined as a position not occupied by any animal
            An available position can contain a plant
        Hint: 
            You should use terrain.map[x][y] to obtain the identifiers of pray, predator, or
            plant that is in position (x,y). 
            If there is nothing in position x,y, terrain.map[x][y] will return an empty string
        Note: 
            plant ID always starts with the word "plant" followed by a numereic value (e.g., plant0)
            predator ID always starts with the word "pred" followed by a numereic value (e.g., pred0)
            pray ID always starts with the word "pray" followed by a numereic value (e.g., pray0)
            Therefore, using regular expression we can figure out whether terrain.map[x][y] contains
            a plant, a pray, a predator, or empty
        Reminder: 
            if the positions occupied only by plants are considered as *available* neighbor positions
        """
        
        avail_neighbor_positions = []        

        for x in [-1,0,1]:
            if (self.position.x  in [0, terrain.width-1]):
                
                if (0 <= self.position.x + x and self.position.x + x < terrain.width):
                    neighb_x = self.position.x + x 
                else:
                    try:
                        #check to see if neighbor position is out of bounds
                        if (self.position.x + x < 0 or self.position.x + x >= terrain.width):
                            raise ValueError
                                    
                    except ValueError:
                        continue 
                                    
            else:
                neighb_x = self.position.x + x 
                    
            for y in [-1,0,1]:   
                if (self.position.y  in [0, terrain.height-1]):
                    
                    if (0 <= self.position.y + y and self.position.y + y < terrain.height):
                        neighb_y = self.position.y + y 
                    else:
                        try:                            
                            if (self.position.y + y < 0 or self.position.y + y >= terrain.height): 
                                raise ValueError
                            
                        except ValueError:
                            continue 
                else:
                    neighb_y = self.position.y + y 
                
                if (neighb_x != self.position.x) or (neighb_y != self.position.y):  
                    search = re.search(r'[Pp]lant[0-9+]|^$', terrain.map[neighb_x][neighb_y]) 
                    if search:
                        
                        pos = Position(0, terrain.width-1, 0, terrain.height-1, neighb_x, neighb_y, False)                          
                        
                        avail_neighbor_positions.append(pos)                     
                                   
        
        return avail_neighbor_positions    
        
    
    
    def will_spawn(self, terrain): 
        """
        Args:
            self: the animal object
            terrain: the object containing all information about the simulation
        Returns:
            False if animal cannot spawn; otherwise True            
        Behavior:
            Animal will only spawn if ALL 4 conditions are satified:
            (1) at specified age range;
            (2) hunger level lower or equal to 2
            (3) spawn waiting time is 0
            (4) there is at least one available adjacent position around the animal to let it spawn

            If animal does not satisfy (1) and (2), return False
            If animal satisfies (1) and (2) but not (3), decrease spawn_waiting by 1 and returns False
            If animal satisfies (1),(2),(3) but no (4), return False
            If animal satisfies all conditions, set spawn_wating to spawn_waiting_time and return True            
        """

        if (self.age_spawn_min <= self.age <= self.age_spawn_max and self.hunger <= 2):
            if self.spawn_waiting == 0:
                if len(self.get_neighbor_positions(terrain)) > 0: 
                    self.spawn_waiting = self.spawn_waiting_time 
                    return True   
                else:
                    return False
            else:
                self.spawn_waiting -= 1
                return False

        else:
            return False
        
                
        
    def get_spawn_location(self, terrain):        
        avail_neighbor_positions = self.get_neighbor_positions(terrain)        
        spawn_position_index = random_choice(range(len(avail_neighbor_positions)), 
            random_sim=terrain.random_sim)
        spawn_position = avail_neighbor_positions[spawn_position_index]
        spawn_position_tuple = (spawn_position.x, spawn_position.y)   
       
        return spawn_position_tuple
    
    
    # return list of visible neighbors to the current animal
    def inspect(self, terrain):
        visible_neighbors = []
        for i in range(-self.visual_range, self.visual_range+1):
            new_x = self.position.x + i
            if new_x >= 0 and new_x < terrain.width:
                for j in range(-self.visual_range, self.visual_range+1):
                    new_y = self.position.y + j
                    if new_y >= 0 and new_y < terrain.height:
                        if new_x != self.position.x or new_y != self.position.y:
                            if terrain.map[new_x][new_y] == "":
                                visible_neighbors.append(str(new_x)+","+str(new_y))
                            else:
                                visible_neighbors.append(terrain.map[new_x][new_y])

        return visible_neighbors
                    

class Predator(Animal):
    
    def __init__(self, terrain, id, position=(), 
                 age_max=35, age_spawn_min=20, age_spawn_max=32,
                 spawn_waiting_time=6, hunger_max=13, visual_range=10):
        
        Animal.__init__(self, terrain, id, position)
        self.age_max = age_max # above threshold animal dies
        self.age_spawn_min = age_spawn_min
        self.age_spawn_max = age_spawn_max
        self.spawn_waiting_time = spawn_waiting_time
        self.hunger_max = hunger_max
        self.visual_range=visual_range
        
    # predator can move to adjacent cell containing a pray, a plant, or nothing
    # predator cannot move to cell occupied by another predator
    def move(self, terrain, visible_neighbors):
        
        bestNeighbor_type = "none"
        bestNeighbor_position = self.position

        dist_min = 1e5

        avail_positions = [self.position]

        for neighborID in visible_neighbors:

            pray_match = re.search("(pray.*)", neighborID) # pray spot
            plant_match = re.search("(plant.*)", neighborID) # plant spot
            avail_match = re.search("(\d+)\,(\d+)", neighborID) # unoccupied spot

            if pray_match:

                bestNeighbor_type = "pray"
                prayID = pray_match.group(1)
                dist = euclidean_distance(self.position, terrain.prays[prayID].position)

                if dist < dist_min:
                    dist_min = dist
                    bestNeighbor_position = terrain.prays[prayID].position                    
                if dist < 2: 
                    avail_positions.append(terrain.prays[prayID].position)

            elif plant_match:

                plantID = plant_match.group(1)
                dist = euclidean_distance(self.position, terrain.plants[plantID].position)                    
                if dist < 2: 
                    avail_positions.append(terrain.plants[plantID].position)
                    
            elif avail_match:
                
                avail_pos = Position(
                        min_xcoord=0, max_xcoord=terrain.width-1, 
                        min_ycoord=0, max_ycoord=terrain.height-1,
                        x=int(avail_match.group(1)), y=int(avail_match.group(2)), random_init=False)


                dist = euclidean_distance(self.position, avail_pos)

                # record all of the available moves
                # including diagonal move (dist = math.sqrt(2)),
                # horizontal move, and vertical move (dist = 1)
                if dist < 2:
                    avail_positions.append(avail_pos)
                    
        print(f"{self.id}'s bestNeighbor: {bestNeighbor_type}")

        # find the best moves by going through all available moves and choose the move
        # that is closest to the "bestNeighbor_position" as found above
        new_pos = self.position
        min_dist = 1e5                

        if bestNeighbor_type == "pray":
            for candidate_position in avail_positions:
                my_dist = euclidean_distance(candidate_position, bestNeighbor_position)
                if my_dist < min_dist:
                    min_dist = my_dist
                    new_pos = candidate_position
        else: # random pick from the available moves to avoid running circle
            avail_position_index = random_choice(range(len(avail_positions)),
                                                 random_sim=terrain.random_sim)
            new_pos = avail_positions[avail_position_index]
                    
        # take the best next move
        prev_pos = self.position
        self.position = new_pos
        
        return (prev_pos, self.position)        
    

class Pray(Animal):

    def __init__(self, terrain, id, position=(), 
                 age_max=30, age_spawn_min=2,
                 hunger_max=10, spawn_waiting_time=1,
                 visual_range=2):
        
        Animal.__init__(self, terrain, id, position)
        
        self.age_max = age_max # above threshold animal dies
        self.age_spawn_min = age_spawn_min
        self.age_spawn_max = self.age_max
        self.hunger_max = hunger_max
        self.spawn_waiting_time = spawn_waiting_time
        self.visual_range=visual_range

    def move(self, terrain, visible_neighbors):

        predator_nearby = False
        bestNeighbor_type = "none"
        bestNeighbor_ID = self.id

        bestNeighbor_position = self.position

        plant_dist_min = 1e5
        pred_dist_min = 1e5

        avail_positions = [self.position]
        
        if (self.position.x, self.position.y) in terrain.plants_map:
            visible_neighbors.append(terrain.plants_map[(self.position.x, self.position.y)])

        for neighborID in visible_neighbors:

            pred_match = re.search("(pred.*)", neighborID) # pray spot            
            plant_match = re.search("(plant.*)", neighborID) # plant spot
            avail_match = re.search("(\d+)\,(\d+)", neighborID) # unoccupied spot

            if plant_match:                

                plantID = plant_match.group(1)
                dist = euclidean_distance(self.position, terrain.plants[plantID].position)

                if dist < plant_dist_min and terrain.plants[plantID].available:                    
                    plant_dist_min = dist
                    bestNeighbor_position = terrain.plants[plantID].position
                    bestNeighbor_ID=plantID
                    bestNeighbor_type = "plant"
                    
                if dist < 2:                    
                    avail_positions.append(terrain.plants[plantID].position)

            elif pred_match:

                predator_nearby = True
                predID = pred_match.group(1)

                dist = euclidean_distance(self.position, terrain.predators[predID].position)

                if dist < pred_dist_min:
                    pred_dist_min = dist
                    closest_predator_position = terrain.predators[predID].position
                    closest_predID = predID

            elif avail_match:
                
                avail_pos = Position(
                        min_xcoord=0, max_xcoord=terrain.width-1, 
                        min_ycoord=0, max_ycoord=terrain.height-1,
                        x=int(avail_match.group(1)), y=int(avail_match.group(2)), random_init=False)

                dist = euclidean_distance(self.position, avail_pos)

                # record all of the available moves
                # including diagonal move (dist = math.sqrt(2)),
                # horizontal move, and vertical move (dist = 1)
                if dist < 2:
                    avail_positions.append(avail_pos)

        if bestNeighbor_type == "plant" and not predator_nearby:            
                print(f"{self.id} bestNeighbor: {bestNeighbor_ID}")


        # find the best moves by going through all available moves and choose the move
        # that is *farthest* from the predator (if detected by the pray)
        # or closest to the plant (if no predator nearby)
        new_pos = self.position
        min_dist = 1e5
        max_dist_from_predator = 0

        if predator_nearby:
            print(f"{self.id}: {closest_predID} nearby !!!!!!!!!!!!!!!!!!!!!!")
            for candidate_position in avail_positions:
                my_dist = euclidean_distance(candidate_position, closest_predator_position)
                if my_dist > max_dist_from_predator:
                    max_dist_from_predator = my_dist
                    new_pos = candidate_position
                    

        elif bestNeighbor_type == "plant":
            for candidate_position in avail_positions:
                my_dist = euclidean_distance(candidate_position, bestNeighbor_position)
                if my_dist < min_dist:
                    min_dist = my_dist
                    new_pos = candidate_position
        else: # random pick from the available moves to avoid running circle
            avail_position_index = random_choice(range(len(avail_positions)),
                                                 random_sim=terrain.random_sim)
            new_pos = avail_positions[avail_position_index]
                    
        # take the best next move
        prev_pos = self.position
        self.position = new_pos
        
        return (prev_pos, self.position)  

