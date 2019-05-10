from matplotlib import pyplot as plt
from matplotlib import animation
from Terrain import Terrain

# Just for fun 
terrain = Terrain()

fig, ax = plt.subplots()
plt.xlim(-1,terrain.width+1)
plt.ylim(-1,terrain.height+1)


# animation function.  This is called sequentially
def animate(i):
    
    print(f"\n------Step {i}------")
    
    terrain.simulate()
    
    print(terrain)
    
    pred_xcoords = []
    pred_ycoords = []
    
    for k,pred in terrain.predators.items():
        pred_xcoords.append(pred.position.y)
        pred_ycoords.append(pred.position.x)        
        
    pray_xcoords = []
    pray_ycoords = []
    
    for k,pray in terrain.prays.items():
        pray_xcoords.append(pray.position.y)
        pray_ycoords.append(pray.position.x)


    plant_available_xcoords = []
    plant_available_ycoords = []
    plant_consumed_xcoords = []
    plant_consumed_ycoords = []

    
    for k,plant in terrain.plants.items():
        if plant.available:
            plant_available_xcoords.append(plant.position.y)
            plant_available_ycoords.append(plant.position.x)
        else:
            plant_consumed_xcoords.append(plant.position.y)
            plant_consumed_ycoords.append(plant.position.x)
    
    
    plant_available_ycoords = [terrain.height - y for y in plant_available_ycoords]
    plant_consumed_ycoords = [terrain.height - y for y in plant_consumed_ycoords]
    pred_ycoords = [terrain.height - y for y in pred_ycoords]
    pray_ycoords = [terrain.height - y for y in pray_ycoords]
    
    if len(terrain.prays) == 0:
        print("no pray is left in the terrain")
    if len(terrain.predators) == 0:
        print("no predator is left in the terrain")
        
    ax.clear()
    plt.xlim(-1,terrain.width+1)
    plt.ylim(-1,terrain.height+1)
    
    return plt.plot(plant_available_xcoords, plant_available_ycoords, 'g.',
                    plant_consumed_xcoords, plant_consumed_ycoords, 'gx',
                    pred_xcoords, pred_ycoords, 'rD', 
                    pray_xcoords, pray_ycoords, 'b^')

# First set up the figure, the axis, and the plot element to be animated       
anim = animation.FuncAnimation(fig, animate, 
                               frames=500, interval=1, blit=False, 
                               repeat=False)

#plt.show()

anim.save('ecosim_classdemo.mp4', fps=1, extra_args=['-vcodec', 'libx264'])
