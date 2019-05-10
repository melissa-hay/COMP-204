import re
from Animal import Pray
from Animal import Predator
from Plant import Plant
from util import get_fixed_positions

class Terrain:
    def __init__(self, terrain_width=25, terrain_height=25,
        nb_predators=1, nb_prays=20, nb_plants=4*49, random_sim=False):

        self.width=terrain_width
        self.height=terrain_height

        self.predator_symbol = "@"
        self.pray_symbol = "&"                
        self.plant_avail_symbol = "."
        self.plant_consumed_symbol = "x"
        self.empty_symbol = " "
        
        # these are used to give unique identifiers 
        # to the new prays and predators
        self.nb_prays_ever_lived = 0 # total number of dead or alive prays
        self.nb_predators_ever_lived = 0 # total number of dead or alive predators
        
        self.nb_prays_over_time=[]
        self.nb_preds_over_time=[]
        self.nb_avail_plants_over_time=[]
        
        self.random_sim = random_sim

        # a 2D list display locations of plants, prays and predators based on the 
        # specified symbols
        self.map = [["" for x in range(self.width)] for y in range(self.height)]
        
        self.plants = {}
        self.plants_map = {}        
        for pos in get_fixed_positions(self.width, self.height, nb_plants):
            self.add_plant(Plant(self, "plant"+str(len(self.plants)), position=pos))

        self.predators = {}
        predator_positions = []
        for pos in get_fixed_positions(self.width, self.height, nb_predators):
            self.add_predator(Predator(self, "pred"+str(self.nb_predators_ever_lived), position=pos))
            predator_positions.append(pos)
            if len(self.predators) == nb_predators:
                break
        
        self.prays = {}
        for pos in get_fixed_positions(self.width, self.height, nb_prays + nb_predators + 4):
            if pos not in predator_positions:
                self.add_pray(Pray(self, "pray"+str(self.nb_prays_ever_lived), position=pos))                
            if len(self.prays) == nb_prays:                
                break
            
    def add_plant(self, plant):
        self.plants[plant.id] = plant
        self.map[plant.position.x][plant.position.y] = plant.id
        self.plants_map[(plant.position.x, plant.position.y)] = plant.id        
        
    def add_pray(self, pray):
        self.prays[pray.id] = pray
        self.map[pray.position.x][pray.position.y] = pray.id
        self.nb_prays_ever_lived += 1

    def add_predator(self, pred):
        self.predators[pred.id] = pred
        self.map[pred.position.x][pred.position.y] = pred.id
        self.nb_predators_ever_lived += 1        
            
    def remove(self, animalID):
        
        pred_match = re.search("pred.*", animalID)
        pray_match = re.search("pray.*", animalID)
        
        if pred_match:
            dead_position = self.predators[animalID].position
            del self.predators[animalID]
        elif pray_match:
            dead_position = self.prays[animalID].position
            del self.prays[animalID]        
            
        x = dead_position.x
        y = dead_position.y
        
        # restore plant symbols on the map 
        # once the agent (predator or pray) moves away from it
        if (x, y) in self.plants_map:
            self.map[x][y] = self.plants_map[(x, y)]
        else:
            self.map[x][y] = ""        
                
    def update_terrain(self, prev_pos, curr_pos, animalID):

        currPos_pray_match = re.search("(pray.*)", self.map[curr_pos.x][curr_pos.y])
        currPos_plant_match = re.search("(plant.*)", self.map[curr_pos.x][curr_pos.y])        
        
        animalID_pred_match = re.search("(pred.*)", animalID)
        animalID_pray_match = re.search("(pray.*)", animalID)
                
        if currPos_pray_match and animalID_pred_match:
            
            prayID = currPos_pray_match.group(1)
            
            print(f"{animalID} killed {prayID} $$$$$$$$$$$$$$$$$$")
                        
            self.predators[animalID].eat()
            
            del self.prays[prayID]
            
        elif (currPos_plant_match or (curr_pos.x,curr_pos.y) in self.plants_map) and animalID_pray_match:

            if currPos_plant_match:
                
                plantID = currPos_plant_match.group(1)

            elif (curr_pos.x,curr_pos.y) in self.plants_map:

                # deal with initial state where a pray is spawned on an available plant
                plantID = self.plants_map[(curr_pos.x,curr_pos.y)]
            
            print(f"{animalID} consumed {plantID}")            
            self.prays[animalID].eat()
            self.plants[plantID].consumed()

        elif animalID_pred_match:
            self.predators[animalID].starve()

        elif animalID_pray_match:
            self.prays[animalID].starve()
        
        # restore plant symbols on the map 
        # once the agent (predator or pray) moves away from it
        if (prev_pos.x, prev_pos.y) in self.plants_map:
            self.map[prev_pos.x][prev_pos.y] = self.plants_map[(prev_pos.x, prev_pos.y)]
        else:
            self.map[prev_pos.x][prev_pos.y] = "" 

        self.map[curr_pos.x][curr_pos.y] = animalID

    def update_predators(self):

        predID_list = [predID for predID in self.predators.keys()]

        for predID in predID_list:
            neighbor_list = self.predators[predID].inspect(self)
            prev_pos,curr_pos = self.predators[predID].move(self, neighbor_list)
            self.update_terrain(prev_pos, curr_pos, predID)                                    

            if self.predators[predID].will_spawn(self):                
                spawn_location = self.predators[predID].get_spawn_location(self)
                pred = Predator(terrain=self, id="pred"+str(self.nb_predators_ever_lived),
                                position=spawn_location)
                self.add_predator(pred)
                print(f"{pred.id} was born")
                    
            self.predators[predID].grow()

        predID_list = [predID for predID in self.predators.keys()]
        
        for predID in predID_list:
            if self.predators[predID].die():
                if self.predators[predID].hunger == self.predators[predID].hunger_max:
                    print(f"{predID} died of hunger")
                else:
                    print(f"{predID} died of age")
                self.remove(predID)

    def update_prays(self): 
        """
        Args: 
            self: terrain object
        Returns:
            Nothing
        Behavoir:
            Update each pray in the following order
                (1) pray inspects to get a list of neighbors within its visual range
                (2) prays moves to get a tuple containing previous and current positions
                (3) terrain update the map according to the prev_pos, curr_pos of the pray
                (4) pray checks whether it will spawn a new off-spring
                    if will_spawn is True, then get the spawn location and add the new pray
                        to the terrain
            Check each pray to see whether it dies
                if it dies:
                    print out one of the two:
                        (1) {prayID} died of hunger
                        (2) {prayID} died of age
                    remove the pray from the terrain
        Hint:
            update_prays is very similar to update_predators
        """
        
        prayID_list = [prayID for prayID in self.prays.keys()]

        for prayID in prayID_list:
            neighbour_list = self.prays[prayID].inspect(self)
            prev_pos,curr_pos = self.prays[prayID].move(self, neighbour_list)
            self.update_terrain(prev_pos, curr_pos, prayID)  
            
            if self.prays[prayID].will_spawn(self):                
                spawn_location = self.prays[prayID].get_spawn_location(self)
                pray = Pray(terrain=self, id="pray"+str(self.nb_prays_ever_lived),
                                position=spawn_location)
                self.add_pray(pray)
                print(f"{pray.id} was born")
                    
            self.prays[prayID].grow()

        prayID_list = [prayID for prayID in self.prays.keys()]
        
        for prayID in prayID_list:
            if self.prays[prayID].die():
                if self.prays[prayID].hunger == self.prays[prayID].hunger_max:
                    print(f"{prayID} died of hunger")
                else:
                    print(f"{prayID} died of age")
                self.remove(prayID)            
        

    def update_plants(self):
        for plantID, plant in self.plants.items():
            plant.regenerate()
            
    # record nb_preds, nb_prays, nb_available_plants as a function of time step
    def update_stats(self): 
        """
            Args:
                self: terrain object containing all information about the simulation
            Returns:
                Nothing
            Behavior:
                Modify three attributes:
                (1) nb_preds_over_time:
                    a list containing the numbers of predators at each simulation step
                (2) nb_prays_over_time:
                    a list containing the numbers of prays at each simulation step
                (3) nb_avail_plants_over_time:
                    a list containing the numbers of *available* plants at each simulation step
        """
                
        plantID_list = [plantID for plantID in self.plants.keys()]
        
        availPlant = 0 #count available plants 
        self.nb_preds_over_time.append(len(self.predators))
        self.nb_prays_over_time.append(len(self.prays))
        
        for plantID in plantID_list:     
            if self.plants[plantID].available:
                availPlant += 1
        self.nb_avail_plants_over_time.append(availPlant)
                
        
    def simulate(self):
        self.update_predators()
        self.update_prays()        
        self.update_plants()
        self.update_stats()    
    
    def __str__(self):
        
        output = "*"
    
        for i in range(self.width):
            output += "*"
        output += "*\n"
            
        for myrow in self.map:
            output += "*"
            for agentID in myrow:
                pred_match = re.search("(pred.*)", agentID)
                pray_match = re.search("(pray.*)", agentID)
                plant_match = re.search("(plant.*)", agentID)
                empty_match = re.search("^$", agentID)
                if pred_match:
                    output += self.predator_symbol
                elif pray_match:
                    output += self.pray_symbol
                elif plant_match:
                    if self.plants[plant_match.group(1)].available:
                        output += self.plant_avail_symbol
                    else:
                        output += self.plant_consumed_symbol
                elif empty_match:
                    output += self.empty_symbol
            output += "*\n"
        
        output += "*"
        for i in range(self.width):
            output += "*"
        output += "*"
        
        return output
            

