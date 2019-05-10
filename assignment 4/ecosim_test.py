from matplotlib import pyplot as plt
from Terrain import Terrain
from Animal import Predator
from Animal import Pray
from Plant import Plant

print("\n----Question 1 Animal starve ----")
terrain = Terrain(nb_predators=0, nb_prays=0)
pred = Predator(terrain, "pred0")
for step in range(5):
    pred.starve()
    print(f"step{step}: {pred.id} hunger level: {pred.hunger}")
pray = Predator(terrain, "pray0")
for step in range(5):
    pray.starve()
    print(f"step{step}: {pray.id} hunger level: {pray.hunger}")


print("\n----Question 2 Animal eat ----")
terrain = Terrain(nb_predators=0, nb_prays=0)
pred = Predator(terrain, "pred0")
for step in range(5):
    pred.starve()    
    print(f"step{step}: {pred.id} hunger level: {pred.hunger}")
for step in range(2):
    pred.eat()
    print(f"step{step}: {pred.id} hunger level: {pred.hunger}")
pray = Pray(terrain, "pray0")
for step in range(5):
    pray.starve()    
    print(f"step{step}: {pray.id} hunger level: {pray.hunger}")
for step in range(2):
    pray.eat()
    print(f"step{step}: {pray.id} hunger level: {pray.hunger}")
    
    
print("\n----Question 3 Animal grow ----")
terrain = Terrain(nb_predators=0, nb_prays=0)
pred = Predator(terrain, "pred0")
for step in range(5):
    pred.grow()
    print(f"step{step}: {pred.id} age: {pred.age}")
pray = Predator(terrain, "pray0")
for step in range(5):
    pray.grow()
    print(f"step{step}: {pray.id} age: {pray.age}")


print("\n----Question 4 Animal die ----")
terrain = Terrain(nb_predators=0, nb_prays=0)
pred0 = Predator(terrain, "pred0", position=(4,4), age_max=10, hunger_max=5)
pred1 = Predator(terrain, "pred1", position=(3,3), age_max=5, hunger_max=10)
for step in range(5):
    for mypred in [pred0, pred1]:
        mypred.grow()
        mypred.starve()        
        if mypred.die():
            if mypred.hunger == mypred.hunger_max:
                print(f"{mypred.id} died of hunger")
            elif mypred.age == mypred.age_max:
                print(f"{mypred.id} died of age")


print("\n---Question 5 Animal get_neighbor_positions ---")
terrain = Terrain(nb_predators=0, nb_prays=0, nb_plants=0)
terrain.add_predator(Predator(terrain, "pred0", position=(5,5)))
terrain.add_predator(Predator(terrain, "pred1", position=(5,6)))
terrain.add_predator(Predator(terrain, "pred2", position=(5,4)))
terrain.add_pray(Predator(terrain, "pray0", position=(4,5)))
terrain.add_plant(Plant(terrain, "plant0", position=(6,4)))
print(terrain)
print("pred0 at position", terrain.predators["pred0"].position, "has neighbor positions:")
for position in terrain.predators["pred0"].get_neighbor_positions(terrain):
    print(position)

terrain = Terrain(nb_predators=0, nb_prays=0, nb_plants=0)
terrain.add_pray(Pray(terrain, "pray0", position=(0,0)))
print(terrain)
print("pray0 at position", terrain.prays["pray0"].position, "has neighbor positions:")
for position in terrain.prays["pray0"].get_neighbor_positions(terrain):
    print(position)


print("\n---Question 6 Animal will_spawn ---")
terrain = Terrain(nb_predators=0, nb_prays=0)
pred0 = Predator(terrain, "pred0", position=(1,2), age_spawn_min=3, age_spawn_max=7, spawn_waiting_time=2)
pred1 = Predator(terrain, "pred1", position=(5,6), age_spawn_min=3, age_spawn_max=7, spawn_waiting_time=2)
pred1.starve()
pred1.starve()
pred1.starve() # pred1 should never spawn at hunger level 3
for step in range(10):
    
    pred0.grow()
    pred0_spawn_waiting = pred0.spawn_waiting    
    if pred0.will_spawn(terrain):
        print(f"step{step}: {pred0.id} will spawn at age {pred0.age}, hunger {pred0.hunger}, waiting {pred0_spawn_waiting}")
    else:
        print(f"step{step}: {pred0.id} will *not* spawn at age {pred0.age}, hunger {pred0.hunger}, waiting {pred0.spawn_waiting}")
    
    pred1.grow()
    pred1_spawn_waiting = pred1.spawn_waiting
    if pred1.will_spawn(terrain):
        print(f"step{step}: {pred1.id} will spawn at age {pred1.age}, hunger {pred1.hunger}, waiting {pred1_spawn_waiting}")
    else:
        print(f"step{step}: {pred1.id} will *not* spawn at age {pred1.age}, hunger {pred1.hunger}, waiting {pred1.spawn_waiting}")
    

print("\n----Question 7 Plant consumed----")
terrain = Terrain(nb_predators=0, nb_prays=0, nb_plants=0)
plant0 = Plant(terrain, "plant0", position=(2,2), regenerate_time=3)
print(f"Before consumed, plant0.available: {plant0.available}")
print(f"After consumed, plant0.available: {plant0.regenerate_countdown}")
plant0.consumed()
print(f"After consumed, plant0.available: {plant0.available}")
print(f"After consumed, plant0.available: {plant0.regenerate_countdown}")


print("\n----Question 8 Plant regenerate----")
terrain = Terrain(nb_predators=0, nb_prays=0, nb_plants=0)
plant0 = Plant(terrain, "plant0", position=(2,2), regenerate_time=3)
plant0.consumed()
for step in range(4):
    print(f"Step{step}, plant0.available: {plant0.available}", end=', ')
    print(f"plant0.regenerate_countdown: {plant0.regenerate_countdown}")
    plant0.regenerate()


print("\n----Question 9 complete update_prays in Terrain----")
terrain = Terrain(nb_predators=4, nb_prays=1)
print(terrain)
for step in range(10):
    print(f"\n------Step {step}------")
    terrain.update_prays()
    print(terrain)


print("\n----Bonus Question update ecosim statistics ----")
terrain = Terrain()
for i in range(500):
    terrain.simulate()

plt.close()
plt.clf()  # clears figure to generate a new one

plt.plot(terrain.nb_preds_over_time, 'r', label="predators")
plt.plot(terrain.nb_prays_over_time, 'b', label="prays")
plt.plot(terrain.nb_avail_plants_over_time, 'g', label="plants")

plt.xlabel('Time')
plt.ylabel('Number of individuals')
plt.legend(loc="best")

plt.savefig("ecosim.eps")










