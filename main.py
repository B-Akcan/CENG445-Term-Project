from classes.repo import Repo
from classes.car import Car

""" # Repo test
Repo.create("F123", 10, 29, 'green')
Repo.create("123123", 10, 29, 'green')

Repo.attach(0, "user1")
Repo.attach(1, "user1")
Repo.attach(0, "user2")

print("All: ", Repo.list())
print("Attached to user1: ", Repo.listattached("user1"))
Repo.detach(0, "user1")
print("All: ", Repo.list())
print("Attached to user1: ", Repo.listattached("user1"))
Repo.detach(0, "user2")
print("All: ", Repo.list())
print("Attached to user1: ", Repo.listattached("user1"))
Repo.delete(1)
print("All: ", Repo.list())
print("Attached to user1: ", Repo.listattached("user1")) """


""" # Map test
map_instance = Map(10, 10, 64, "green")

for j in range(2, 8):
    map_instance[(1, j)] = Road(1, j, 0)

map_instance[(8, 9)] = Obstacle(8, 9, 0)

map_instance.draw()
print(map_instance.getxy(8, 9)) """

map_instance = Repo.create("F571", 10,10, 64, 'green')
Repo.create("ASDSAD", 23,321, 231, 'yellow')
Repo.list()
ogr = Repo.attach(12345, "onur")
tgr = Repo.attach(12345, "tolga")
Repo.listattached("tolga")
Repo().components.register("Car", Car)
Repo().components.register("Ferrari", Car)
# rt = Repo().components.create("Car") # gives maximum recursion depth exceeded error

""" Repo.create("F571", 10,10, 64, 'green')
Repo.list() # F571 will be listed with an id
ogr = Repo.attach(12345, "onur")
tgr = Repo.attach(12345, "tolga") # these two are the same object
rt = Repo.components.create('Car')
print(rt)
Repo.components.list() # lists the available components
# assume all components call Repo.components.register(type, cls)

ogr[(1,1)] = rt
rt.rotation = 0
for j in range(2,8):
  ogr[(1,j)] = Repo.components.create('straight')
  ogr[(1,j)].rotation = 0
dt = Repo.components.create('turn90')
dt.rotation = 1
ogr[(1,8)] = dt
for i in range(2,8):
  ogr[(i,1)] = Repo.components.create('straight')
  ogr[(i,8)] = Repo.components.create('straight')
  ogr[(i,1)].rotation = 1
  ogr[(i,8)].rotation = 1
rt = Repo.components.create('turn90')
ogr[(8,1)] = rt
rt.rotation = 3
for j in range(2,8):
  ogr[(8,j)] = Repo.components.create('straight')
  ogr[(8,j)].rotation = 0
dt = Repo.components.create('turn90')
dt.rotation = 2
ogr[(8,8)] = dt
ogr[(8,3)] = Repo.components.create('booster')
ogr[(8,9)] = Repo.components.create('rock')
ogr[(8,9)] = Repo.components.create('rock')
ogr[(8,9)] = Repo.components.create('rock')
ogr[(0,8)] = Repo.components.create('rock')
ogr[(1,0)] = Repo.components.create('rock')
ogr[(7,1)] = Repo.components.create('fuel')
frr = ogr.components.create('Ferrari')
frr.driver = "Alonso"
print(frr.mode, frr.pos, frr.topspeed, frr.topfuel)
4
ogr.draw()
cv = ogr.view(500,500,200,200)
cv.draw()
frr.start()
frr.tick()
frr.accel()
frr.left()
frr.tick()
frr.right()
frr.accell()
frr.tick()
frr.stop()
cv.draw()
ogr.draw() """