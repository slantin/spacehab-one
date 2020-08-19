"""This assignment is intended to give you practice in expanding your project-based ABM to include novel agent-to-agent interactions
as well as communicated results across scales (via outputs, constructed norms or other metrics)   

You will design and execute a draft analysis to add these interactions and document the results by updating any UML diagrams or OOD templates.  

Using your NetLogo or other language ABM, construct a simple set of social (inter-agent) interactions as an expansion of your existing model.
Keep the agent interactions simple and under control (working code is better than fancy, non-working code!).  
Use multiple simulations to exercise your revised model and present the results in your result. 
Add at least one collective metric (group norms, behavior choice, etc...) to describe the emergent behavior of your system.  

Update your existing OOD/UML/POM description of your model with the new results.  
Does the agent behavior surprise you or is it expected?  
How do individual agents differ in their behavior? 
What elements would you expand or reduce with respect to these results?
"""

#%%
## Simple ABM Model

# The purpose of the model is to 

# Stephen Lantin
# Department of Agricultural & Biological Engineering
# University of Florida

# Created 18:53 EDT, 3 August 2020

# list that collects IDs so 
import itertools
import numpy as np
from random import randint
import matplotlib.pyplot as plt

num_crew = 2
num_recyclers = 1
num_air_recyclers = 1
air_purified_per_tick = 3
num_initial_plants = 1
simulation_end = 100
plant_grow_prob = 0.01
plant_clean_air_req = 5
plant_bad_air_req = 5
plant_clean_water_req = 5
plant_ticks_to_grow = 3
grow_chance = 25 # percent
move_chance = 5 # percent

class hasWater(object):

    def __init__(self):
        self.cleanWater = float(0)
        self.greyWater = float(0)
        self.capacityWater = float(0) #static

    def dirtifyWater(self,value):
        if self.cleanWater >= value:
            self.cleanWater -= value
            self.greyWater += value
        else:
            self.greyWater += self.cleanWater
            self.cleanWater = float(0)

    def toWaterRecycler(self,value):
        # check if there's room for all of the grey water
        # don't call this if you're a water recycler
        # pick a recycler
        #picked_recycler = recyclers
        picked_recycler = recyclers[randint(0,len(recyclers)-1)]
        if (picked_recycler.cleanWater + picked_recycler.greyWater + value) <= picked_recycler.capacityWater:
            picked_recycler.greyWater += value
            self.greyWater -= value
        else:
            print("The water recycler is currently full.")


class hasAir(object):

    def __init__(self):
        self.cleanAir = float(0)
        self.badAir = float(0)
    
    def dirtifyAir(self,value):
        if self.cleanAir >= value:
            self.cleanAir -= value
            self.badAir += value
        else:
            self.badAir += self.cleanAir
            self.cleanAir = float(0)
    
    def toAirRecycler(self,value):
        # air can be compressed and doesn't have a residence time
        # don't call this if you're an air recycler
        # pick a recycler
        picked_recycler = air_recyclers[randint(0,len(air_recyclers)-1)]
        picked_recycler.badAir += value
        self.badAir -= value



class hasWaterAndAir(object):

    def __init__(self):
        self.cleanWater = float(0)
        self.greyWater = float(0)
        self.capacityWater = float(0) #static
        self.cleanAir = float(0)
        self.badAir = float(0)
    
    def dirtifyAir(self,value):
        if self.cleanAir >= value:
            self.cleanAir -= value
            self.badAir += value
        else:
            self.badAir += self.cleanAir
            self.cleanAir = float(0)
    
    def toAirRecycler(self,value):
        # air can be compressed and doesn't have a residence time
        # don't call this if you're an air recycler
        # pick a recycler
        picked_recycler = air_recyclers[randint(0,len(air_recyclers)-1)]
        picked_recycler.badAir += value
        self.badAir -= value


    def dirtifyWater(self,value):
        if self.cleanWater >= value:
            self.cleanWater -= value
            self.greyWater += value
        else:
            self.greyWater += self.cleanWater
            self.cleanWater = float(0)

    def toWaterRecycler(self,value):
        # check if there's room for all of the grey water
        # don't call this if you're a water recycler
        # pick a recycler
        #picked_recycler = recyclers
        picked_recycler = recyclers[randint(0,len(recyclers)-1)]
        if (picked_recycler.cleanWater + picked_recycler.greyWater + value) <= picked_recycler.capacityWater:
            picked_recycler.greyWater += value
            self.greyWater -= value
        else:
            print("The water recycler is currently full.")


class WaterRecycler(hasWater):

    def __init__(self,name):
        super(WaterRecycler,self).__init__()
        self.cleanWater = float(50)
        self.name = name
        self._residenceTime = 3
        self._ticksUntilClean = 0
        self.capacityWater = float(100)
        self.isRecycling = 0
    
    def recycle(self): # can't end and start recycling in the same loop
        if self.isRecycling: # recycle until residence time is done (kind of like a batch reactor)
            self._ticksUntilClean -= 1
            if self._ticksUntilClean == 0:
                self.isRecycling = 0
                # purify water out - new var to be added for grey water in recycle vs. dumped?
                self.cleanWater += self._currentlyRecycling * 0.9 # 90% loop efficiency
                self.greyWater -= self._currentlyRecycling * 0.9
                print(f"Water Recycler {self.name} is done recycling!")
        else: # start recycle
            self._ticksUntilClean = self._residenceTime
            self._currentlyRecycling = self.greyWater # doesn't recycle grey water that is added while recycling
            self.isRecycling = 1
            print(f"Water Recycler {self.name} is starting to recycle!")
            
    def queryWater(self):
        print(f"Water Recycler {self.name}\nGrey Water: {self.greyWater}\nClean Water: {self.cleanWater}\n\n")


class AirRecycler(hasAir):
    # air is assumed to be automatically purified and not stored, unlike water in water recyclers
    def __init__(self,name):
        super(AirRecycler,self).__init__()
        self.name = name
        self.airList = []

    # def purifyAir(self):
    #     self.cleanAir += self.badAir * 0.42
    #     self.badAir -= self.badAir * 0.42 # 42 % efficient
    #     for room in range(len(rooms)-1): # outside doesn't have air
    #         self.airList.append((rooms[room].name,rooms[room].cleanAir))
    #     print(sorted(self.airList)[0][1])


class Room(hasAir):

    def __init__(self,name):
        super(Room,self).__init__()
        self.name = name
        self.cleanAir = float(100)
        self.badAir = float(100)
        self.crewPresent = 0


    def queryAttributes(self):
        print(f"Room {self.name}\n\
            \nClean Air: {self.cleanAir}\
            \nBad Air: {self.badAir}\
            \nThere are {self.crewPresent} crew members present.\n")

class GrowthChamber(Room,hasWater):

    def __init__(self,name):
        super(GrowthChamber,self).__init__(name)
        self.numPlants = 0
        self.maxPlants = 20
        self.cleanWater = float(100)
        self.greyWater = float(0)
        self.cleanAir = float(100)

    def plant(self):
        if self.crewPresent > 0 and (self.numPlants < self.maxPlants):
            plants.append(Plant())
            self.numPlants += 1
    
    
    def queryPlants(self):
        if self.numPlants == 1:
            print(f"There is {self.numPlants} plant in {self.name}.")
        else:
            print(f"There are {self.numPlants} plants in {self.name}.")

    def queryWater(self):
        print(f"Room {self.name}\nClean Water: {self.cleanWater}\n\n")

class Outside(Room):

    def __init__(self,name):
        super(Outside,self).__init__(name)
        self.cleanAir = 0
        self.badAir = 0

class CrewMember(hasWaterAndAir):

    #id_iter = itertools.count()

    def __init__(self,name):
        super(CrewMember,self).__init__()
        #self.id = next(self.id_iter)
        self.name = name
        self.location = rooms[0] # start in cabin, room 0
        self.greyWater = float(10)
        self.badAir = float(10)
        self.new_location = rooms[0]
        rooms[0].crewPresent += 1

    def toilet(self):
        self.toWaterRecycler(self.greyWater)

    def drink(self,value):
        picked_recycler = recyclers[randint(0,len(recyclers)-1)]
        if picked_recycler.cleanWater >= value:
            picked_recycler.cleanWater -= value
            self.greyWater += value
        else:
            print("This water recycler is currently empty.")

    def breathe(self,value):
        self.badAir -= value
        self.location.badAir += value
        self.location.cleanAir -= value

    def moveTo(self):
        while self.new_location == self.location \
        and randint(1,100) <= move_chance:
            self.new_location = rooms[randint(0,len(rooms)-2)] # outside has no air
        self.location.crewPresent -= 1
        self.location = self.new_location
        self.location.crewPresent += 1
        

    def queryAttributes(self):
        print(f"Crew Member {self.name}\nGrey Water: {self.greyWater}\n\n")
        if self.location.name == "Outside":
            print(f"Crew Member {self.name} is {self.location.name}.")
        else:
            print(f"Crew Member {self.name} is in {self.location.name}.")

class Plant(object):
    id_iter = itertools.count()
    # other plant variables are globally defined so that it's easier to change the parameters
    def __init__(self):
        super(Plant,self).__init__()
        self.id = next(self.id_iter)
        self.growthStage = 0
        placement = randint(1,2) # growth chambers are rooms 1 & 2
        self.location = rooms[placement]
        self.location.numPlants += 1
        self.isNotHarvested = 1
        

    def grow(self):
        if (self.location.cleanAir >= plant_clean_air_req) \
        and (self.location.badAir >= plant_bad_air_req) \
        and (self.location.cleanWater >= plant_clean_water_req) \
        and randint(1,100) <= grow_chance \
        and self.isNotHarvested \
        and self.growthStage < plant_ticks_to_grow:
            self.growthStage += 1
        # cleans a small amount of air
        self.location.badAir -= 0.1
        self.location.cleanAir += 0.1

    def harvest(self):
        global harvested_plants
        if (self.growthStage == plant_ticks_to_grow) \
        and self.location.crewPresent > 0 \
        and self.isNotHarvested:
            self.location.numPlants -= 1
            harvested_plants += 1
            self.isNotHarvested = 0
            self.growthStage = "Harvested"


    def checkStatus(self):
        print(f"Plant {self.id} Growth Stage: {self.growthStage}")


    

# initial conditions
crew = [CrewMember(f"{i}") for i in range(num_crew)]

recyclers = [WaterRecycler(f"{i}") for i in range(num_recyclers)]

air_recyclers = [AirRecycler(f"{i}") for i in range(num_air_recyclers)]

rooms = [Room("Cabin"),GrowthChamber("Growth Chamber 1"),GrowthChamber("Growth Chamber 2"),Outside("Outside")]

plants = [Plant() for plant in range(num_initial_plants)]

harvested_plants = 0

# main loop
tick = 0
while tick < simulation_end:
    print(f"Tick {tick}")

    # Unit Test: Toilet
    print("toilet")
    [crewmember.toilet() for crewmember in crew]
    #[crewmember.queryAttributes() for crewmember in crew]
    #[recycler.queryWater() for recycler in recyclers]

    # Unit Test: Drink
    print("drink")
    [crewmember.drink(1) for crewmember in crew]
    #[crewmember.queryAttributes() for crewmember in crew]
    #[recycler.queryWater() for recycler in recyclers]

    # Unit Test: Recycle
    print("recycle")
    [recycler.recycle() for recycler in recyclers]
    #[recycler.queryWater() for recycler in recyclers]
    #[crewmember.queryAttributes() for crewmember in crew]

    # Unit Test: Grow
    print("grow")
    [plant.grow() for plant in plants]
    [room.queryAttributes() for room in rooms]

    # Unit Test: Plant
    print("room functions")
    for room in rooms:
        room.toAirRecycler(room.badAir/10) # cycle 10% of the bad air in a room per tick
        # plant
        if isinstance(room,GrowthChamber):
            room.plant()
            room.queryPlants()
    [plant.checkStatus() for plant in plants]

    # Unit Test: Move
    [crewmember.moveTo() for crewmember in crew]

    # Unit Test: Harvest
    [plant.harvest() for plant in plants]

    # Unit Test: Breathe
    [crewmember.breathe(0.4) for crewmember in crew]


    # water balance according to conservation of mass, checks out
    water_balance = 0 # crew members, rooms, and water recyclers have water
    water_balance = sum([crewmember.greyWater for crewmember in crew]) \
        + sum([crewmember.cleanWater for crewmember in crew]) \
        + sum([room.greyWater for room in rooms[1:3]]) \
        + sum([room.cleanWater for room in rooms[1:3]]) \
        + sum([recycler.greyWater for recycler in recyclers]) \
        + sum([recycler.cleanWater for recycler in recyclers])
    print(f"Water balance: {water_balance}")

    # air balance according to conservation of mass,
    air_balance = 0 # crew members, rooms, and air recyclers have air
    air_balance = sum([crewmember.badAir for crewmember in crew]) \
        + sum([crewmember.cleanAir for crewmember in crew]) \
        + sum([room.badAir for room in rooms[1:3]]) \
        + sum([room.cleanAir for room in rooms[1:3]]) \
        + sum([air_recycler.badAir for air_recycler in air_recyclers]) \
        + sum([air_recycler.cleanAir for air_recycler in air_recyclers])
    print(f"Air balance: {water_balance}")


    # [air_recycler.purifyAir() for air_recycler in air_recyclers]

    tick += 1

print(f"There were {harvested_plants} plants harvested.")
[crewmember.queryAttributes() for crewmember in crew]
[recycler.queryWater() for recycler in recyclers]


# plots

# current environment in the room
# water, air

# plants harvested

# machine usage



# final_wealth = [person.wealth for person in people]
# #print(final_wealth)
# plt.figure(1)
# plt.hist(final_wealth)
# plt.title("Final Wealth Distribution, $")

# final_max_wealth = [person.max_wealth for person in people]
# plt.figure(2)
# plt.hist(final_max_wealth)
# plt.title("Maximum Wealth Distribution, $")

# final_min_wealth = [person.min_wealth for person in people]
# plt.figure(3)
# plt.hist(final_min_wealth)
# plt.title("Minimum Wealth Distribution, $")

# homeowner_final_wealth = []
# nonhomeowner_final_wealth = []
# plt.figure(4)
# for person in people:
#     if person.homeowner == 1:
#         homeowner_final_wealth.append(person.wealth)
#     else:
#         nonhomeowner_final_wealth.append(person.wealth)
# plt.hist(homeowner_final_wealth)
# plt.hist(nonhomeowner_final_wealth)
# plt.title("Final Wealth Distribution, Homeowners vs. Nonhomeowners")

# p1 = Person("John",36)
# print(p1.name)
# print(p1.age)
# p1.myfunc()

# class Ball:
#     def __init__(self, x, y, r):
#         tk.Canvas.create_circle
#         self.x
#         self.y

#     def grow(self):
        


# p1 = Person("John",36)
# print(p1.name)
# print(p1.age)
# p1.myfunc()

# """Move object"""
# Canvas.move()