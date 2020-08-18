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

num_crew = 1
num_recyclers = 1
simulation_end = 10

# class Object(object):

#     def __init__(self):
#         pass
#         #self.value = 250
#         #self.owner = person.id

#     #def appreciate(self):
#         #self.value += self.value*appreciation_per_tick

class hasWater(object):

    def __init__(self):
        self.cleanWater = float(0)
        self.greyWater = float(0)
        self.capacityWater = float(0) #static

    def dirtifyWater(self,value):
        if self.cleanWater >= value:
            self.cleanWater -= value
        else:
            self.cleanWater = float(0)
        self.greyWater += value

    def toWaterRecycler(self,value):
        # check if there's room for all of the grey water
        # don't call this if you're a water recycler
        # pick a recycler
        #picked_recycler = recyclers
        picked_recycler = recyclers[randint(0,len(recyclers)-1)]
        if (picked_recycler.cleanWater + picked_recycler.greyWater + value) <= picked_recycler.capacityWater:
            picked_recycler.greyWater += self.greyWater
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

class CrewMember(hasWater):

    #id_iter = itertools.count()

    def __init__(self,name):
        super(CrewMember,self).__init__()
        #self.id = next(self.id_iter)
        self.name = name
        self.location = "Cabin"
        self.greyWater = 10

    def toilet(self):
        self.toWaterRecycler(self.greyWater)

    def drink(self,value):
        picked_recycler = recyclers[randint(0,len(recyclers)-1)]
        if picked_recycler.cleanWater >= value:
            picked_recycler.cleanWater -= value
            self.greyWater += value
        else:
            print("This water recycler is currently empty.")

    def queryAttributes(self):
        print(f"Crew Member {self.name}\nGrey Water: {self.greyWater}\n\n")
        
    
    

# initial conditions
crew = [CrewMember(f"{i}") for i in range(num_crew)]

recyclers = [WaterRecycler(f"{i}") for i in range(num_recyclers)]

# main loop
tick = 0
while tick < simulation_end:
    print(f"Tick {tick}")

    # Unit Test: Toilet
    print("toilet")
    [crewmember.toilet() for crewmember in crew]
    [crewmember.queryAttributes() for crewmember in crew]
    [recycler.queryWater() for recycler in recyclers]

    # Unit Test: Drink
    print("drink")
    [crewmember.drink(1) for crewmember in crew]
    [crewmember.queryAttributes() for crewmember in crew]
    [recycler.queryWater() for recycler in recyclers]

    # Unit Test: Recycle
    print("recycle")
    [recycler.recycle() for recycler in recyclers]
    [recycler.queryWater() for recycler in recyclers]
    [crewmember.queryAttributes() for crewmember in crew]

    # test residence time
    tick += 1

[crewmember.queryAttributes() for crewmember in crew]
[recycler.queryWater() for recycler in recyclers]


# plots

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